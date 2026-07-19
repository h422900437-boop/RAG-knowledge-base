# 🚀 快速开始指南

**5 分钟让应用跑起来！**

---

## 📋 前置要求

- Python 3.9+
- Git
- 选择其中一个 LLM：
  - 🌐 **DeepSeek API**（需要 API 密钥）
  - 💻 **Ollama**（完全免费，离线）

---

## ⚡ 最快开始（仅 3 步）

### 第 1 步：Clone 项目

```bash
git clone https://github.com/h422900437/RAG-knowledge-base.git
cd RAG-knowledge-base
```

### 第 2 步：一键安装

**Mac/Linux:**
```bash
bash run.sh setup
```

**Windows:**
```bash
run.bat setup
```

### 第 3 步：启动应用

**Mac/Linux:**
```bash
# 后端（一个终端）
bash run.sh backend

# 前端（另一个终端）
bash run.sh frontend
```

**Windows:**
```bash
# 后端（一个终端）
run.bat backend

# 前端（另一个终端）
run.bat frontend
```

**打开浏览器访问：** http://localhost:8501

---

## 🤔 选择你的 LLM

### 选项 A：使用 DeepSeek（云 LLM，推荐）

**优点：** 回答质量最高，速度快
**缺点：** 需要 API 密钥，需要付费

**步骤：**

1. 获取 API 密钥
   - 访问 https://platform.deepseek.com
   - 注册并创建 API 密钥

2. 设置环境变量
   ```bash
   # Mac/Linux
   export DEEPSEEK_TOKEN="sk-xxx..."
   
   # Windows
   set DEEPSEEK_TOKEN=sk-xxx...
   ```

3. 启动应用
   ```bash
   bash run.sh start      # Mac/Linux
   run.bat start          # Windows
   ```

---

### 选项 B：使用 Ollama（本地 LLM，免费）

**优点：** 完全免费，无需 API 密钥，完全离线
**缺点：** 需要本地运行，回答质量一般

**步骤：**

1. 安装 Ollama
   - 访问 https://ollama.ai
   - 下载并安装

2. 下载模型
   ```bash
   ollama pull llama2
   # 或其他模型：mistral, neural-chat, openchat
   ```

3. 启动 Ollama
   ```bash
   ollama serve
   ```

4. 设置 LLM 模式并启动应用
   ```bash
   # Mac/Linux
   export LLM_MODE="ollama"
   bash run.sh start
   
   # Windows
   set LLM_MODE=ollama
   run.bat start
   ```

---

## 🎯 命令参考

### run.sh (Mac/Linux)

```bash
bash run.sh setup       # 首次安装
bash run.sh start       # 启动应用（需要 2 个终端）
bash run.sh backend     # 只启动后端
bash run.sh frontend    # 只启动前端
bash run.sh test        # 运行测试
bash run.sh clean       # 清理缓存
bash run.sh help        # 显示帮助
```

### run.bat (Windows)

```bash
run.bat setup           # 首次安装
run.bat start           # 启动应用（需要 2 个窗口）
run.bat backend         # 只启动后端
run.bat frontend        # 只启动前端
run.bat test            # 运行测试
run.bat clean           # 清理缓存
run.bat help            # 显示帮助
```

---

## 📍 访问应用

启动后，打开浏览器访问：

- **前端应用：** http://localhost:8501
- **后端 API：** http://127.0.0.1:8000
- **API 文档：** http://127.0.0.1:8000/docs

---

## 📚 上传文档并提问

1. **左侧面板** → 点击 "Choose a document"
2. **选择文件** → 支持 PDF、Word、Excel、TXT
3. **点击 "🚀 Confirm Ingestion"** → 等待上传完成
4. **下方输入框** → 输入问题
5. **查看回答** → 包含来源文档引用

---

## ⚠️ 常见问题

### Q1：Python 版本太低
**错误：** `Python 3.9+ required`

**解决：**
```bash
python3 --version
# 如果 < 3.9，请升级 Python
# https://www.python.org
```

### Q2：依赖安装失败
**错误：** `pip install 失败`

**解决：**
```bash
# 升级 pip
python -m pip install --upgrade pip

# 重新安装
pip install -r requirement.txt
```

### Q3：DeepSeek 无法连接
**错误：** `Connection failed to DeepSeek API`

**解决：**
- 检查 DEEPSEEK_TOKEN 是否正确设置
- 检查网络连接
- 访问 https://platform.deepseek.com 确认 API 可用

### Q4：Ollama 无法连接
**错误：** `Cannot connect to Ollama`

**解决：**
```bash
# 确保 Ollama 后台运行
ollama serve

# 检查是否在 localhost:11434
curl http://localhost:11434/api/tags
```

### Q5：Streamlit 连接超时
**错误：** `Connection timeout`

**解决：**
- 确保后端正在运行
- 在另一个终端运行 `bash run.sh backend`
- 等待 15 秒后重新刷新浏览器

---

## 🧪 测试安装

安装完成后，可以运行测试验证：

```bash
bash run.sh test        # Mac/Linux
run.bat test            # Windows
```

---

## 📖 更多帮助

- **安装详解** → 看 [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **LLM 选择** → 看 [CHOOSE_LLM.md](CHOOSE_LLM.md)
- **Ollama 教程** → 看 [LOCAL_LLM_GUIDE.md](LOCAL_LLM_GUIDE.md)
- **GitHub 发布** → 看 [GITHUB_GUIDE.md](GITHUB_GUIDE.md)

---

## 🎉 开始使用！

现在你可以：
1. ✅ 上传 PDF、Word、Excel 等文档
2. ✅ 用 AI 提问和获得基于文档的回答
3. ✅ 查看 AI 引用的源文档
4. ✅ 完全离线或使用云 API

**祝你使用愉快！** 🚀

---

## 💬 需要帮助？

- 提交 Issue：https://github.com/h422900437/RAG-knowledge-base/issues
- 查看文档：看本项目的各个 MD 文件
- 联系开发者：kowai

---

**项目地址：** https://github.com/h422900437/RAG-knowledge-base

**⭐ 如果觉得有用，请给个 Star！**
