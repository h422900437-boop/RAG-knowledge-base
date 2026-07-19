# 🖥️ 本地 LLM 使用指南（无需 API 密钥）

如果你没有 DeepSeek API 密钥，可以使用 **Ollama** - 一个免费的本地 LLM 框架。完全离线，无需任何付费。

## 📊 对比表

| 特性 | DeepSeek (云) | Ollama (本地) |
|------|---------------|--------------|
| **成本** | 按用量付费 | 免费 |
| **速度** | 依赖网络 | 本地极快 |
| **隐私** | 数据上传到云 | 完全离线 |
| **质量** | 高精度 | 中等精度 |
| **需求** | API 密钥 | 本地运行 |
| **适合场景** | 生产环境 | 开发、演示、内部使用 |

## 🚀 快速开始（3 步）

### 步骤 1：安装 Ollama

访问 https://ollama.ai 下载并安装 Ollama（支持 Mac、Linux、Windows）

**Mac 用户：**
```bash
# 使用 Homebrew 安装（推荐）
brew install ollama

# 或直接下载 DMG 文件
# https://ollama.ai/download
```

### 步骤 2：下载 LLM 模型

```bash
# 下载 llama2 模型（推荐，～3GB）
ollama pull llama2

# 或其他模型：
ollama pull mistral          # 更快
ollama pull neural-chat      # 针对对话优化
ollama pull openchat         # 开源高质量
```

**首次下载会比较慢（取决于网络速度），后续使用会很快。**

### 步骤 3：启动应用

```bash
# 确保 Ollama 后台运行
ollama serve

# 然后在另一个终端启动 RAG 应用
export LLM_MODE="ollama"
uvicorn backend.main:app --reload
```

## 📝 详细配置

### 方式 1：环境变量配置（推荐）

```bash
# 选择本地 LLM
export LLM_MODE="ollama"

# 或选择云 LLM
export LLM_MODE="deepseek"
export DEEPSEEK_TOKEN="your_api_key"

# 启动应用
uvicorn backend.main:app --reload
```

### 方式 2：修改 config.py

编辑 `config.py`：

```python
# 改这一行
LLM_MODE = "ollama"  # 或 "deepseek"

# 可选：修改模型
OLLAMA_MODEL = "llama2"  # 或 "mistral"、"neural-chat"
```

## 🧠 选择合适的模型

### llama2（推荐入门）
```bash
ollama pull llama2
```
- 模型大小：3.8GB
- 速度：中等
- 质量：中等
- 适合：学习、演示、测试

### mistral（推荐快速）
```bash
ollama pull mistral
```
- 模型大小：3.8GB
- 速度：快
- 质量：中等
- 适合：对话、快速响应

### neural-chat（推荐对话）
```bash
ollama pull neural-chat
```
- 模型大小：3.9GB
- 速度：中等
- 质量：好
- 适合：自然对话、HR 问答

### openchat（推荐高质量）
```bash
ollama pull openchat
```
- 模型大小：3.8GB
- 速度：快
- 质量：很好
- 适合：严肃用途、生产环境

## 🔄 切换模型

### 更改 Ollama 模型

编辑 `config.py`：
```python
OLLAMA_MODEL = "neural-chat"  # 改为你想用的模型
```

重启应用即可。

## ⚙️ Ollama 命令参考

```bash
# 列出已下载的模型
ollama list

# 删除模型释放空间
ollama rm llama2

# 查看模型详情
ollama show llama2

# 直接用 Ollama 测试（不用 RAG 应用）
ollama run llama2

# 查看 Ollama 日志
ollama logs
```

## 🧪 测试配置

运行这个脚本验证配置是否正确：

```bash
python config.py
```

**输出示例：**
```
============================================================
📋 RAG Configuration Check
============================================================

LLM Mode: OLLAMA
Status: ⚠️  Manual setup required
Model: llama2
Message: Using local LLM (Ollama). Make sure Ollama is running.
Setup: https://ollama.ai

Vector DB: ./chroma_db
Embedding: BAAI/bge-small-zh-v1.5
============================================================
```

## 🐛 常见问题

### Q1：Ollama 无法连接
**症状：** 错误 `Could not connect to Ollama`

**解决：**
```bash
# 确保 Ollama 服务在运行
ollama serve

# 检查是否在 localhost:11434
curl http://localhost:11434/api/tags
```

### Q2：模型下载很慢
**症状：** `ollama pull xxx` 卡住

**解决：**
- 检查网络连接
- 尝试更小的模型（mistral 3.8GB vs llama2 3.8GB）
- 在夜间下载（网络可能更快）

### Q3：运行时内存不足
**症状：** 应用崩溃或卡顿

**解决：**
- 关闭其他应用释放内存
- 使用更小的模型（mistral）
- 增加虚拟内存

### Q4：Ollama 模型目录在哪
**Mac：**
```bash
ls ~/.ollama/models/
```

**Linux：**
```bash
ls ~/.ollama/models/
```

**Windows：**
```bash
%USERPROFILE%\.ollama\models\
```

## 📊 性能对比

| 操作 | DeepSeek | Ollama (llama2) |
|------|----------|-----------------|
| 首次启动 | 1s | 5s（加载模型）|
| 回答问题 | 3-5s | 5-15s |
| 网络依赖 | 是 | 否 |
| 隐私保护 | 否 | 是 |
| API 成本 | ¥0.5-5 元/百万 tokens | 免费 |

## 🎯 何时使用哪个

### 使用 **DeepSeek**（云）
- ✅ 需要最高质量的回答
- ✅ 生产环境
- ✅ 大规模应用
- ✅ 不想占用本地 GPU/CPU

### 使用 **Ollama**（本地）
- ✅ 没有 API 密钥
- ✅ 隐私很重要
- ✅ 想要离线使用
- ✅ 学习和演示
- ✅ 网络不稳定

## 🔄 动态切换

应用支持在运行时切换 LLM：

```bash
# 前台运行 llama2
export LLM_MODE="ollama" && uvicorn backend.main:app

# 按 Ctrl+C 停止

# 切换到 DeepSeek
export LLM_MODE="deepseek" && export DEEPSEEK_TOKEN="..." && uvicorn backend.main:app
```

## 💡 优化建议

### 加速 Ollama 回答

编辑 `config.py`，设置更小的返回长度：

```python
LLM_MAX_TOKENS = 256  # 限制回答长度（加速）
```

### 使用 GPU 加速（如果有 GPU）

Ollama 会自动检测和使用 GPU（NVIDIA、AMD、Apple Silicon）。

验证：
```bash
ollama ps  # 显示正在运行的模型及其使用的资源
```

## 📚 更多资源

- **Ollama 官网：** https://ollama.ai
- **模型列表：** https://ollama.ai/library
- **GitHub：** https://github.com/jmorganca/ollama
- **文档：** https://github.com/jmorganca/ollama/tree/main/docs

## ✅ 完整检查清单

- [ ] 已安装 Ollama
- [ ] 已下载至少一个模型（`ollama list`）
- [ ] Ollama 后台运行中（`ollama serve`）
- [ ] 环境变量设置正确（`echo $LLM_MODE`）
- [ ] config.py 配置正确
- [ ] 应用启动成功（`python config.py` 无错误）
- [ ] 能成功提问并获得回答

---

**现在你可以完全离线使用 RAG 系统了！无需任何 API 密钥！** 🎉
