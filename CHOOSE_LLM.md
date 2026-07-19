# 🤔 选择你的 LLM - 快速指南

不确定应该用 DeepSeek 还是 Ollama？按照这个指南选择。

## ⚡ 30 秒快速判断

**问 1：你有 DeepSeek API 密钥吗？**
- 是 → 用 **DeepSeek**
- 否 → 用 **Ollama**

**问 2（可选）：你想要最高的回答质量吗？**
- 是 → 用 **DeepSeek**
- 否 → 用 **Ollama**

## 📋 详细对比

### DeepSeek（云 LLM）

```
✅ 优点
- 回答质量最高（最新的大模型）
- 响应速度快（云端计算）
- 不占用本地资源
- 支持最新的 AI 功能

❌ 缺点
- 需要 API 密钥（需付费）
- 需要网络连接
- 数据发送到云端（隐私考虑）
- 成本：¥0.5-5 元 / 百万 tokens

💰 成本估算
- 小规模使用（<1M tokens/月）：¥5-50
- 中等使用（1-10M tokens/月）：¥50-500
- 大规模使用（>10M tokens/月）：联系商务
```

**适合：** 生产环境、对回答质量要求高

### Ollama（本地 LLM）

```
✅ 优点
- 完全免费
- 无需 API 密钥
- 完全离线，隐私保护
- 本地运行，数据不外传
- 无网络依赖，随时可用

❌ 缺点
- 回答质量一般（非最新大模型）
- 需要本地 GPU/CPU（占用资源）
- 响应速度较慢（本地计算）
- 模型下载比较大（3-7GB）

💻 硬件需求
- CPU：4+ 核心
- RAM：8GB+ 推荐
- 磁盘：20GB+ （用于模型）
- GPU：可选（有 GPU 会快 10 倍）
```

**适合：** 开发、演示、内部使用、隐私敏感的应用

## 🎯 场景选择

### 场景 1：公司内部 HR 系统
```
推荐：Ollama
原因：
✅ 隐私安全（数据不上云）
✅ 成本无（免费）
✅ HR 政策 Q&A 不需要最高质量
✅ 员工数据敏感
```

### 场景 2：生产环境 SaaS 服务
```
推荐：DeepSeek
原因：
✅ 回答质量最优
✅ 云端扩展性好
✅ 用户体验最佳
✅ 可以按用量付费
```

### 场景 3：个人学习/演示
```
推荐：Ollama
原因：
✅ 完全免费
✅ 无需 API 密钥
✅ 不用担心成本
```

### 场景 4：初创公司
```
推荐：Ollama（早期）→ DeepSeek（规模化）
原因：
✅ 早期节省成本
✅ 规模化后优化体验
```

## 🚀 快速开始

### 使用 DeepSeek

```bash
# 1. 获取 API 密钥
# 访问 https://platform.deepseek.com
# 创建 API 密钥并复制

# 2. 设置环境变量
export DEEPSEEK_TOKEN="sk-xxx..."
export LLM_MODE="deepseek"

# 3. 启动应用
uvicorn backend.main:app --reload
streamlit run frontend/app.py
```

**需要帮助？** 看 README.md 的快速开始部分

### 使用 Ollama

```bash
# 1. 安装 Ollama
# https://ollama.ai → 下载并安装

# 2. 下载模型
ollama pull llama2  # 或 mistral、neural-chat 等

# 3. 启动 Ollama
ollama serve

# 4. 设置环境变量（新终端）
export LLM_MODE="ollama"

# 5. 启动应用
uvicorn backend.main:app --reload
streamlit run frontend/app.py
```

**需要帮助？** 看 LOCAL_LLM_GUIDE.md 的详细教程

## 📊 成本对比（按月）

假设：每天 100 次问答，每次平均 1000 tokens

| 场景 | DeepSeek | Ollama |
|------|----------|--------|
| 1 个月 | ¥15 | ¥0 |
| 3 个月 | ¥45 | ¥0 |
| 6 个月 | ¥90 | ¥0 |
| 1 年 | ¥180 | ¥0 |

**结论：** 如果不考虑质量，Ollama 可以节省大量成本！

## 🔄 后期切换

好消息：你可以随时切换！

```bash
# 从 Ollama 切换到 DeepSeek
export LLM_MODE="deepseek"
export DEEPSEEK_TOKEN="sk-..."

# 从 DeepSeek 切换到 Ollama
export LLM_MODE="ollama"
# 取消设置 DEEPSEEK_TOKEN
unset DEEPSEEK_TOKEN
```

应用会自动使用新的 LLM。

## ❓ 常见问题

### Q：两个都试试可以吗？
**答：** 可以！先用 Ollama 免费试试，如果满意就用。如果觉得质量不够，再升级到 DeepSeek。

### Q：Ollama 回答不好怎么办？
**答：** 尝试其他模型：
- llama2（当前）
- mistral（更快）
- neural-chat（更适合对话）
- openchat（质量最好）

### Q：可以同时运行两个吗？
**答：** 可以，但会占用双倍资源。通常不建议。

### Q：我应该选哪个？
**答：** 如果还是不确定：
1. **先选 Ollama**（免费试试）
2. 如果满意就一直用
3. 如果质量不够，升级到 DeepSeek

## 📞 决策树

```
        你有 API 密钥吗？
        /            \
       是             否
      /                \
  用 DeepSeek         用 Ollama
      |                  |
   最高质量           免费使用
   需要付费           完全离线
   在线服务           本地运行
```

## ✅ 完成检查

- [ ] 选择了 LLM（DeepSeek 或 Ollama）
- [ ] 完成了相关的设置
- [ ] 应用成功启动
- [ ] 能够提问并获得回答

---

**还有疑问？**
- DeepSeek 问题 → 看 README.md
- Ollama 问题 → 看 LOCAL_LLM_GUIDE.md
- 技术问题 → GitHub Issues

**选好了？开始使用吧！** 🚀
