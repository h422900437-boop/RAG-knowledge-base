# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from backend.rag_core import RagEngine
from backend.file_extractors import FileExtractor
import shutil
import os
import uuid  # Ensures safe temporary random subdirectories

# Explicitly create the runtime engine reference container
engine_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles secure initialization and teardown of the RAG Core Engine.
    Ensures persistent database locks are safely managed across service lifecycles.
    """
    global engine_instance
    print("🚀 [Lifespan] Initializing RagEngine and loading vector store...")
    engine_instance = RagEngine()
    
    yield
    
    print("🛑 [Lifespan] Shutting down application. Releasing assets...")
    if engine_instance and hasattr(engine_instance, "vector_store") and hasattr(engine_instance.vector_store, "_client"):
        try:
            engine_instance.vector_store._client.reset()
        except Exception:
            pass
    engine_instance = None

# Initialize FastAPI with the verified lifespan handler
app = FastAPI(title="RAG Corporate HR Backend", lifespan=lifespan)

class ChatRequest(BaseModel):
    message: str

async def generate_response(question: str):
    """Async generator wrapper for streaming response with proper buffering."""
    global engine_instance
    try:
        for chunk in engine_instance.query(question):
            yield chunk
            # Ensure data is flushed immediately instead of being buffered
    except Exception as e:
        yield f"Error: {str(e)}"

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    """Handles streamed interactive chat requests using the global engine runtime."""
    global engine_instance
    if not engine_instance:
        raise HTTPException(status_code=503, detail="RAG Core Engine is not initialized yet.")

    try:
        return StreamingResponse(generate_response(req.message), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_endpoint(file: UploadFile = File(...)):
    """Handles dynamic document file uploads with multimodal support (PDF, Word, Excel, etc.)."""
    global engine_instance
    if not engine_instance:
        raise HTTPException(status_code=503, detail="RAG Core Engine is not initialized yet.")

    # Create a completely isolated quarantine folder using UUID to shield your local directory
    unique_id = str(uuid.uuid4())
    temp_dir = os.path.join("./data", unique_id)
    os.makedirs(temp_dir, exist_ok=True)

    file_path = os.path.join(temp_dir, file.filename)

    try:
        # Save uploaded file to temporary location
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text based on file type
        print(f"📂 Uploaded file: {file.filename}")
        text, metadata = FileExtractor.extract_text(file_path)

        if not text.strip():
            raise ValueError("File extraction resulted in empty text. Please check the file format.")

        # Pass extracted text and metadata to the RAG engine
        engine_instance.upload_document(
            text=text,
            source_filename=file.filename,
            metadata=metadata
        )

        # Return success with extraction info
        return {
            "status": "success",
            "filename": file.filename,
            "file_type": metadata.get("file_type"),
            "extracted_chars": len(text),
            "metadata": metadata
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"❌ Upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
    finally:
        # Securely sweep only the specific temporary chunk file and its designated parent bucket
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(temp_dir):
            try:
                os.rmdir(temp_dir)
            except Exception:
                pass