# DeepSeek 流式响应配置问题

## 🔴 可能的原因

### 1. **DeepSeek API 本身不支持真正的流式（最可能）**
DeepSeek 的某些模型（如 `deepseek-v4-flash`）在 LangChain 中可能不能真正流式返回。整个响应是一次性生成然后返回的。

### 2. **LangChain 的 ChatOpenAI 包装问题**
LangChain 的 `stream()` 方法可能没有正确处理 DeepSeek 的响应格式。

### 3. **FastAPI 缓冲问题**
即使 LLM 支持流式，FastAPI 也可能缓冲响应。

## ✅ 解决方案

### 方案 A：直接检测 DeepSeek 是否真的支持流式
```bash
# 运行诊断脚本
export DEEPSEEK_TOKEN="your_token"
python backend/test_deepseek_stream.py
```

**如果输出 "Only 1 chunk received"** → DeepSeek 不支持流式 → 需要换方案

### 方案 B：使用 OpenAI 的原生 API 而不是 LangChain（推荐）

如果 DeepSeek 确实支持流式但 LangChain 没正确处理，直接调用 API：

```python
# rag_core.py 修改
import os
from openai import OpenAI

class RagEngine:
    def __init__(self):
        # ... 其他初始化 ...
        
        # 使用原生 OpenAI 客户端
        self.client = OpenAI(
            api_key=os.environ.get("DEEPSEEK_TOKEN"),
            base_url="https://api.deepseek.com"
        )
    
    def query(self, question: str):
        # ... 获取 context ...
        
        final_prompt = self.prompt_template.format(context=context_text, question=question)
        
        # 直接使用原生流式 API
        with self.client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "user", "content": final_prompt}],
            stream=True,
            temperature=0.2
        ) as response:
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
```

### 方案 C：如果 DeepSeek 根本不支持流式

改用支持真正流式的 LLM：

**选项 1：OpenAI GPT**
```python
self.llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    api_key=os.environ.get("OPENAI_API_KEY"),
)
```

**选项 2：Ollama（本地 LLM，完全免费）**
```python
from langchain_community.llms import Ollama

self.llm = Ollama(model="llama2")  # 完全本地化，支持流式
```

**选项 3：Claude（通过 LangChain）**
```python
from langchain_anthropic import ChatAnthropic

self.llm = ChatAnthropic(model="claude-3-haiku-20240307")
```

## 🧪 诊断步骤

### 步骤 1：检测 DeepSeek 流式支持
```bash
python backend/test_deepseek_stream.py
```

### 步骤 2：检查结果

**结果 A：多个 chunk（streaming 正常）**
```
📊 Chunks received: 25
✅ True streaming detected!
```
→ 问题不在 DeepSeek，可能是网络缓冲或 Streamlit 问题

**结果 B：只有 1 chunk（不支持流式）**
```
📊 Chunks received: 1
⚠️  WARNING: Only 1 chunk received!
```
→ DeepSeek 在 LangChain 中不支持流式，需要换方案

## 🔧 推荐解决方案优先级

| 方案 | 优先级 | 优点 | 缺点 |
|------|--------|------|------|
| 使用原生 OpenAI API | ⭐⭐⭐ | 绕过 LangChain，直接用 DeepSeek 原生流式 API | 需要改代码 |
| 换成 Ollama（本地） | ⭐⭐⭐ | 完全免费、本地化、真正支持流式 | 需要 CPU/GPU |
| 换成 OpenAI GPT | ⭐⭐ | 肯定支持流式 | 要付费 |
| 换成 Claude | ⭐⭐ | 肯定支持流式 | 要付费 |
| 保持现状但禁用流式 | ⭐ | 无需改动 | 用户体验差 |

## 📝 快速修复（使用原生 OpenAI API）

### 步骤 1：安装最新的 OpenAI 库
```bash
pip install --upgrade openai
```

### 步骤 2：修改 rag_core.py

```python
import os
from openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
import json
import tiktoken

class RagEngine:
    def __init__(self):
        self.token_api = os.environ.get("DEEPSEEK_TOKEN")
        if not self.token_api:
            print("⚠️ Warning: DEEPSEEK_TOKEN environment variable not found!")
        
        print("🔄 [RagEngine] Loading Embedding model (BAAI/bge-small-zh-v1.5)...")
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            model_kwargs={'device': 'cpu'}
        )
        
        print("📂 [RagEngine] Connecting to local database at ./chroma_db ...")
        self.vector_store = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embedding_model
        )
        
        # ✨ 使用原生 OpenAI 客户端而不是 LangChain 包装
        print("🤖 [RagEngine] Establishing connection to LLM (deepseek-v4-flash)...")
        self.client = OpenAI(
            api_key=self.token_api,
            base_url="https://api.deepseek.com"
        )
        
        self.rag_prompt_template = """You are a helpful and strict corporate HR assistant. 
Use the following pieces of retrieved attendance policies to answer the user's question. 
If you don't know the answer or if the provided policy doesn't contain enough information, say that you cannot find the explicit answer in the policy. Do not try to make up an answer.

Retrieved Attendance Policies (Context):
----------------------------------
{context}
----------------------------------

User's Question: {question}

Your Professional Answer:"""
        
        print("✅ [RagEngine] Initialization completed. Core engine ready!")

    @staticmethod
    def _tokenizer_len(text: str) -> int:
        """Calculate token count for text splitting constraint."""
        tokenizer = tiktoken.get_encoding("cl100k_base")
        tokens = tokenizer.encode(text, disallowed_special=())
        return len(tokens)

    def query(self, question: str):
        """
        Streamed Knowledge Base Query Processing with Source Tracking
        Uses native OpenAI API for true streaming support
        """
        print(f"🔍 [RagEngine] Processing query with Chroma: '{question}'...")
        # 1. Retrieve top 5 similar documents from Chroma
        results = self.vector_store.similarity_search(question, k=5)

        # 2. Extract unique sources and contents for metadata referencing
        sources_info = []
        for i, doc in enumerate(results):
            sources_info.append({
                "chunk_id": i + 1,
                "source": doc.metadata.get('source', 'Unknown'),
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            })

        # 3. Yield the source information as the very first data packet in the stream
        yield f"[SOURCES]:{json.dumps(sources_info)}\n"

        # 4. Construct context with chunk metadata headers for the LLM prompt
        context_text = "\n\n".join([
            f"---[Chunk {i+1} ]---\n"
            f"Source File: {doc.metadata.get('source', 'Unknown')}\n"
            f"Content: \n{doc.page_content}"
            for i, doc in enumerate(results)
        ])

        print("🧠 [RagEngine] Invoking LLM via native streaming API...")
        # 5. Format prompt and yield tokens sequentially using native API
        final_prompt = self.rag_prompt_template.format(context=context_text, question=question)
        
        # 使用原生 API 的流式功能（比 LangChain 的包装更直接可靠）
        with self.client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "user", "content": final_prompt}],
            stream=True,
            temperature=0.2
        ) as response:
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

    def upload_document(self, file_path: str):
        """Read, chunk, and append new document embeddings into the vector store."""
        print(f"📑 [RagEngine] Reading file for incremental ingestion: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
            length_function=self._tokenizer_len,
            separators=["\n\n", "\n", "。", "！", "？", "，", " "]
        )

        filename = os.path.basename(file_path)
        docs = text_splitter.create_documents([raw_text], metadatas=[{"source": filename}])
        print(f"📝 Chunking complete. Generated {len(docs)} text segments.")

        self.vector_store.add_documents(docs)
        print(f"🎉 Success! '{filename}' has been appended to the vector database.")
```

### 步骤 3：更新依赖
```bash
pip install openai langchain langchain-community langchain-openai chromadb sentence-transformers tiktoken
```

## ✅ 测试修复后的流式

```bash
# 确保后端运行中
export DEEPSEEK_TOKEN="your_token"
uvicorn backend.main:app --reload

# 测试
python backend/test_streaming.py
```

**预期结果：**
- 文字应该逐字出现
- 每个 chunk 之间有小的时间差
- 不是一下子全部显示

---

## 📊 对比表

| 配置 | 效果 | 问题 |
|------|------|------|
| LangChain + DeepSeek | ❌ 一次性返回 | LangChain 包装不支持 DeepSeek 流式 |
| 原生 OpenAI API + DeepSeek | ✅ 真正流式 | 需要改代码 |
| Ollama 本地 | ✅ 真正流式 | 需要本地运行 |

建议你先运行 `test_deepseek_stream.py` 确认问题所在！
