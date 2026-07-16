import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# 导入你写好的 RagEngine 类
from rag_core import RagEngine

app = FastAPI(
    title="RAGent Link Backend", 
    description="FastAPI backend for RAG Knowledge Base System",
    version="1.0"
)

# 解决跨域问题（允许前端 Streamlit 顺利访问接口）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保存放上传临时文件的 data 文件夹存在于根目录下
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "../data")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 初始化你的 RAG 引擎
# 注意：RagEngine 内部默认会去 '../chroma_db' 找向量数据库
# 当我们在 backend/main.py 中运行该服务时，相对路径 '../chroma_db' 刚好能正确指向根目录下的 chroma_db
rag_engine = RagEngine()


# 定义请求体的数据结构
class ChatRequest(BaseModel):
    message: str


# --- 接口 1: 上传文档并进行向量化 ---
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    接收前端上传的文件，保存到本地临时 data 目录，并触发 RagEngine 进行切片和向量化。
    """
    try:
        # 1. 保存文件到本地 data 目录
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. 调用你的 RagEngine 的动态上传方法
        rag_engine.upload_document(file_path)
        
        return {
            "status": "success",
            "message": f"File '{file.filename}' successfully ingested and vectorized into Chroma DB."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")


# --- 接口 2: 普通问答接口 (一次性返回全部回答) ---
@app.post("/chat")
async def chat(request: ChatRequest):
    """
    接收用户提问，调用 RagEngine 进行知识库检索和 LLM 普通生成，直接返回完整文本。
    """
    try:
        # 直接调用你的 query 方法
        answer_text = rag_engine.query(request.message)
        return {"answer": answer_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


# --- 接口 3: 流式问答接口 (Streaming Chat - 用于前端打字机效果) ---
@app.post("/chat_stream")
async def chat_stream(request: ChatRequest):
    """
    接收用户提问，使用 RagEngine 中的向量库和 Prompt 模板，
    但改用 llm.stream 配合 FastAPI StreamingResponse 实现流式逐字输出。
    """
    def generate_llm_stream(question: str):
        try:
            print(f"🔍 [Streaming] Chroma is searching context for: '{question}'...")
            # 1. 使用你实例中的 vector_store 检索 top-5 切片
            results = rag_engine.vector_store.similarity_search(question, k=5)  
            
            # 2. 组装上下文
            context_text = "\n\n".join([
                f"---[Chunk {i+1} ]---\n"
                f"Source File: {doc.metadata.get('source', 'Unknown')}\n"
                f"Content: \n{doc.page_content}"
                for i, doc in enumerate(results)
            ])
            
            # 3. 组装 Prompt 
            final_prompt = rag_engine.prompt_template.format(context=context_text, question=question)
            
            # 4. 调用大模型的流式 API，实时 yield 吐出字符
            print("[Streaming] LLM is streaming back the tokens...")
            for chunk in rag_engine.llm.stream(final_prompt):
                yield chunk.content
                
        except Exception as e:
            yield f"Error in stream generation: {str(e)}"

    # 返回流式响应，媒体类型设为 text/event-stream 保持连接
    return StreamingResponse(generate_llm_stream(request.message), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    # 在 127.0.0.1:8000 端口启动服务
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)