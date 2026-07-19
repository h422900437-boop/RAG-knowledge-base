# 🚀 RAG 知识库 - 快速安装指南

## 📋 环境要求
- Python 3.9+
- pip 21.0+
- 虚拟环境已创建（.venv）

## 🔧 安装步骤

### 步骤 1：进入项目目录
```bash
cd /Users/huangguowei/Desktop/RAG-knowledge-base
```

### 步骤 2：激活虚拟环境
```bash
source .venv/bin/activate
```

### 步骤 3：更新 pip（重要！）
```bash
pip install --upgrade pip
```

### 步骤 4：安装所有依赖
```bash
pip install -r requirement.txt
```

**如果上面的命令失败，分步安装：**

```bash
# Core dependencies
pip install langchain langchain-community langchain-openai

# Text processing
pip install langchain-text-splitters tiktoken

# Vector database
pip install chromadb sentence-transformers

# LLM API
pip install openai

# Multimodal support (最重要！)
pip install pypdf python-docx openpyxl

# Web frameworks
pip install fastapi uvicorn streamlit

# Utils
pip install pydantic requests
```

### 步骤 5：验证安装（可选）
```bash
python -c "
import pypdf, docx, openpyxl, langchain, chromadb, openai, fastapi, streamlit
print('✅ All dependencies installed successfully!')
"
```

## 🎯 常见问题

### 问题 1：pip install 超时
**解决方案：**
```bash
pip install -r requirement.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 问题 2：某个包安装失败
单独安装该包：
```bash
pip install 包名 --upgrade
```

### 问题 3：Permission denied 错误
```bash
pip install --user -r requirement.txt
# 或
pip install -r requirement.txt --break-system-packages
```

### 问题 4：虚拟环境损坏
重建虚拟环境：
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirement.txt
```

## 📦 dependency 说明

### 核心 LangChain
| 包 | 版本 | 用途 |
|---|------|------|
| langchain | >=0.1.0 | LLM orchestration |
| langchain-community | >=0.0.0 | Community integrations |
| langchain-openai | >=0.0.0 | OpenAI integration |
| langchain-text-splitters | >=0.0.0 | Text chunking |

### 向量数据库 & 嵌入
| 包 | 版本 | 用途 |
|---|------|------|
| chromadb | >=0.4.0 | Vector database |
| sentence-transformers | >=2.2.0 | Embedding model |
| tiktoken | >=0.5.0 | Token counting |

### LLM & API
| 包 | 版本 | 用途 |
|---|------|------|
| openai | >=1.0.0 | OpenAI API client |

### 文档处理（多模态）
| 包 | 版本 | 用途 |
|---|------|------|
| pypdf | >=3.0.0 | PDF 文本提取 |
| python-docx | >=0.8.0 | Word 文本提取 |
| openpyxl | >=3.0.0 | Excel 表格提取 |

### Web 框架
| 包 | 版本 | 用途 |
|---|------|------|
| fastapi | >=0.104.0 | 后端 API 框架 |
| uvicorn | >=0.24.0 | ASGI 服务器 |
| streamlit | >=1.28.0 | 前端框架 |

## 🚀 启动应用

### 终端 1：启动后端
```bash
export DEEPSEEK_TOKEN="your_deepseek_api_key"
uvicorn backend.main:app --reload --port 8000
```

**预期输出：**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
🚀 [Lifespan] Initializing RagEngine and loading vector store...
✅ [RagEngine] Initialization completed. Core engine ready!
```

### 终端 2：启动前端
```bash
streamlit run frontend/app.py
```

**预期输出：**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### 访问应用
打开浏览器：http://localhost:8501

## ✅ 完成清单

- [ ] 进入项目目录
- [ ] 激活虚拟环境
- [ ] 升级 pip
- [ ] 安装所有依赖
- [ ] 验证依赖安装
- [ ] 设置 DEEPSEEK_TOKEN
- [ ] 启动后端服务
- [ ] 启动前端应用
- [ ] 在浏览器打开应用

## 📝 requirement.txt 内容

```
# Core LangChain & LLM
langchain>=0.1.0
langchain-community>=0.0.0
langchain-openai>=0.0.0
langchain-text-splitters>=0.0.0

# Vector Database & Embeddings
chromadb>=0.4.0
sentence-transformers>=2.2.0

# LLM & API
openai>=1.0.0
tiktoken>=0.5.0

# Document Processing (Multimodal)
pypdf>=3.0.0
python-docx>=0.8.0
openpyxl>=3.0.0

# Web Framework
fastapi>=0.104.0
uvicorn>=0.24.0
starlette>=0.27.0

# Frontend
streamlit>=1.28.0

# Utilities
pydantic>=2.0.0
requests>=2.31.0
```

## 🆘 需要帮助？

如果还有问题，收集以下信息：
1. Python 版本：`python --version`
2. pip 版本：`pip --version`
3. 错误信息的完整输出
4. 你的操作系统

然后联系开发者！
