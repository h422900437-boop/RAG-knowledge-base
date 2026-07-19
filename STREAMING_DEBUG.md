# 流式响应 (Streaming) 调试指南

## 🔴 原始问题

1. **FastAPI 端点使用同步函数** - `StreamingResponse` 在同步函数中不稳定
2. **缺少缓冲刷新机制** - 数据可能被缓冲，导致客户端无法实时接收
3. **Streamlit 流式显示逻辑不完善** - 未处理网络延迟和编码问题

## ✅ 已应用的修复

### 1. **Backend (main.py)**
```python
# ❌ 之前：同步函数
@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    data_stream = engine_instance.query(req.message)
    return StreamingResponse(data_stream, media_type="text/plain")

# ✅ 之后：异步函数 + 异步生成器
async def generate_response(question: str):
    """Async generator wrapper for streaming response"""
    for chunk in engine_instance.query(question):
        yield chunk

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    return StreamingResponse(generate_response(req.message), media_type="text/event-stream")
```

**改进点：**
- 使用 `async` 函数确保真正的异步流式处理
- 改用 `text/event-stream` MIME 类型（更适合流式传输）
- 异步包装确保生成器可以被正确处理

### 2. **RAG Core (rag_core.py)**
- 确保每个 yield 都包含换行符 `\n`
- 这样客户端可以按行读取流数据
- 避免 LLM 返回的文本被缓冲

### 3. **Frontend (app.py)**
```python
# ✅ 改进：
- 使用 timeout=300 防止长时间查询超时
- 添加详细的错误处理（ConnectionError、Timeout）
- 改进了流数据的处理逻辑
- 使用 cleaned_chunk 而非 chunk 确保格式正确
```

## 🧪 测试方法

### 方法 1：CLI 测试脚本
```bash
# 启动后端
cd /Users/huangguowei/Desktop/RAG-knowledge-base
export DEEPSEEK_TOKEN="your_token_here"
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# 另一个终端运行测试
python backend/test_streaming.py
```

**预期输出：**
```
🧪 Testing Streaming Chat Endpoint...

📝 Question: If an employee hasn't gone to work for six consecutive days, what will happen?

============================================================
🔄 Streaming Response:

✅ Sources received:
   - Chunk 1: company_policies.txt

根据公司政策，如果员工连续6个工作日无故缺勤...
(文字逐字出现，而不是一次性全部显示)

============================================================
✅ Streaming completed in 3.45 seconds
📊 Response length: 234 characters
📌 Sources received: Yes
```

### 方法 2：完整应用测试
```bash
# 终端1：启动后端
export DEEPSEEK_TOKEN="your_token_here"
uvicorn backend.main:app --reload

# 终端2：启动前端
cd /Users/huangguowei/Desktop/RAG-knowledge-base
streamlit run frontend/app.py
```

**预期表现：**
- 输入问题后，AI 回答应该**逐字出现**（流式效果）
- 而不是等待全部完成后一次性显示
- 下方应该显示源文档引用

## 🔧 常见问题排查

### 问题：文字还是一下子全显示，没有流式效果

**排查步骤：**

1. **检查后端是否正确返回流**
   ```bash
   curl -X POST http://127.0.0.1:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"test question"}' \
     --no-buffer -N
   ```
   如果看到文字逐字出现，说明后端正常。

2. **检查 Streamlit 版本**
   ```bash
   pip show streamlit
   ```
   需要 `streamlit >= 1.18.0` 以支持 `st.write_stream()`

3. **检查网络缓冲**
   - FastAPI 默认有缓冲，可以添加 `Content-Length` 禁用：
   ```python
   return StreamingResponse(
       generate_response(req.message),
       media_type="text/event-stream",
       headers={"X-Accel-Buffering": "no"}
   )
   ```

### 问题：收不到源信息 (Sources)

**排查：**
1. 检查 `[SOURCES]` 是否正确从后端发送
2. 在测试脚本中查看完整输出
3. 确认 JSON 格式正确

### 问题：请求超时

**原因可能：**
1. LLM 调用超时（DeepSeek API 问题）
2. 网络问题
3. 向量搜索耗时过长

**解决：**
```python
# 增加超时时间
timeout=300  # 5分钟
```

## 📊 流式响应工作原理

```
用户输入问题
    ↓
FastAPI 接收请求 (async)
    ↓
生成器开始流式生成数据 (yield)
    ↓
[SOURCES]:json 首先发送 ← Streamlit 拦截并存储
    ↓
LLM 文本流逐字发送 ← Streamlit 实时显示
    ↓
Streamlit st.write_stream() 实时渲染文字
    ↓
聊天气泡显示流式内容
```

## 🎯 性能优化建议

1. **启用 Chroma 缓存**：避免重复搜索
2. **使用更小的 embedding 模型**：加快相似度搜索
3. **限制 K 值**：`similarity_search(question, k=3)` 而不是 k=5
4. **启用响应缓存**：对重复问题进行缓存

## 📝 更新清单

- ✅ main.py - 改为异步端点
- ✅ rag_core.py - 确保换行符
- ✅ app.py - 改进流式处理和错误处理
- ✅ test_streaming.py - 创建测试脚本
- ✅ STREAMING_DEBUG.md - 本调试指南
