# backend/rag_core.py
import os
import tiktoken
import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

class RagEngine:
    """
    RAG Core Computational Engine
    Encapsulates vector database management and LLM generation.
    """
    
    def __init__(self):
        """Initialize models, vector store connections, and prompt templates."""
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
        
        print("🤖 [RagEngine] Establishing connection to LLM (deepseek-v4-flash)...")
        self.llm = ChatOpenAI(
            model_name="deepseek-v4-flash",
            temperature=0.2,
            openai_api_key=self.token_api,
            openai_api_base="https://api.deepseek.com",
        )
        
        rag_prompt_template = """You are a helpful and strict corporate HR assistant. 
Use the following pieces of retrieved attendance policies to answer the user's question. 
If you don't know the answer or if the provided policy doesn't contain enough information, say that you cannot find the explicit answer in the policy. Do not try to make up an answer.

Retrieved Attendance Policies (Context):
----------------------------------
{context}
----------------------------------

User's Question: {question}

Your Professional Answer:"""

        self.prompt_template = PromptTemplate(
            template=rag_prompt_template,
            input_variables=["context", "question"]
        )
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
        Yields source metadata first, then streams LLM text tokens.
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

        print("🧠 [RagEngine] Invoking LLM via stream protocol...")
        # 5. Format prompt and yield tokens sequentially
        final_prompt = self.prompt_template.format(context=context_text, question=question)
        
        for chunk in self.llm.stream(final_prompt):
            if chunk.content:
                yield chunk.content

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