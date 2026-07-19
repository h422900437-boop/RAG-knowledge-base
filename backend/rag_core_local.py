# backend/rag_core_local.py
"""
RAG Engine with local LLM support (Ollama)
Alternative to cloud-based LLM APIs for users without API keys
"""

import os
import tiktoken
import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate


class RagEngineLocal:
    """
    RAG Engine using local LLM (Ollama)
    For users without API keys - completely free and offline
    """

    def __init__(self, use_local=True):
        """
        Initialize RAG engine with optional local LLM support.

        Args:
            use_local: If True, use local Ollama LLM. If False, use DeepSeek API.
        """
        self.use_local = use_local
        self.token_api = os.environ.get("DEEPSEEK_TOKEN")

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

        # Initialize LLM based on availability
        if use_local:
            self._init_local_llm()
        else:
            self._init_deepseek_llm()

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

    def _init_local_llm(self):
        """Initialize local Ollama LLM."""
        try:
            from langchain_community.llms import Ollama
            print("🤖 [RagEngine] Initializing local LLM (Ollama)...")
            self.client = None  # Not used for local
            self.llm = Ollama(model="llama2", temperature=0.2)
            self.is_local = True
            print("✅ [RagEngine] Using local Ollama LLM (llama2)")
        except ImportError:
            print("❌ Ollama client not found. Please install: pip install ollama")
            print("   Or download Ollama from: https://ollama.ai")
            raise

    def _init_deepseek_llm(self):
        """Initialize DeepSeek cloud LLM."""
        if not self.token_api:
            print("⚠️ Warning: DEEPSEEK_TOKEN environment variable not found!")
            print("   Set it with: export DEEPSEEK_TOKEN='your_token'")
            raise ValueError("DeepSeek API key required")

        from openai import OpenAI
        print("🤖 [RagEngine] Establishing connection to LLM (deepseek-v4-flash)...")
        self.client = OpenAI(
            api_key=self.token_api,
            base_url="https://api.deepseek.com"
        )
        self.is_local = False
        print("✅ [RagEngine] Using DeepSeek v4-flash LLM")

    @staticmethod
    def _tokenizer_len(text: str) -> int:
        """Calculate token count for text splitting constraint."""
        tokenizer = tiktoken.get_encoding("cl100k_base")
        tokens = tokenizer.encode(text, disallowed_special=())
        return len(tokens)

    def query(self, question: str):
        """
        Streamed Knowledge Base Query Processing with Source Tracking.
        Works with both cloud and local LLMs.
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

        print("🧠 [RagEngine] Invoking LLM...")
        # 5. Format prompt and yield tokens sequentially
        final_prompt = self.rag_prompt_template.format(context=context_text, question=question)

        if self.is_local:
            # Use local LLM (Ollama)
            print("   Using local LLM (Ollama)")
            try:
                response = self.llm.invoke(final_prompt)
                # For local LLM, return full response (no streaming by default)
                yield response
            except Exception as e:
                yield f"Error from local LLM: {str(e)}"
        else:
            # Use cloud LLM (DeepSeek)
            print("   Using cloud LLM (DeepSeek)")
            try:
                with self.client.chat.completions.create(
                    model="deepseek-v4-flash",
                    messages=[{"role": "user", "content": final_prompt}],
                    stream=True,
                    temperature=0.2
                ) as response:
                    for chunk in response:
                        if chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content
            except Exception as e:
                yield f"Error from DeepSeek LLM: {str(e)}"

    def upload_document(self, text: str = None, file_path: str = None, source_filename: str = None, metadata: dict = None):
        """
        Read, chunk, and append new document embeddings into the vector store.

        Args:
            text: Pre-extracted text content (preferred for multimodal support)
            file_path: Path to read text from (legacy, if text not provided)
            source_filename: Original filename for metadata
            metadata: Additional metadata about the document (file_type, pages, etc.)
        """
        # Support both old (file_path) and new (text) API for backward compatibility
        if text is None:
            if file_path is None:
                raise ValueError("Either 'text' or 'file_path' must be provided")
            print(f"📑 [RagEngine] Reading file for incremental ingestion: {file_path}")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {file_path}")
            source_filename = os.path.basename(file_path)

        if not text.strip():
            raise ValueError("Document text is empty after extraction")

        if metadata is None:
            metadata = {}

        # Prepare document metadata
        doc_metadata = {
            "source": source_filename or "unknown",
            "file_type": metadata.get("file_type", "unknown"),
        }

        # Add optional metadata if available
        if "total_pages" in metadata:
            doc_metadata["total_pages"] = metadata["total_pages"]
        if "sheets" in metadata:
            doc_metadata["sheets"] = metadata["sheets"]
        if "tables" in metadata:
            doc_metadata["tables"] = metadata["tables"]
        if "paragraphs" in metadata:
            doc_metadata["paragraphs"] = metadata["paragraphs"]

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
            length_function=self._tokenizer_len,
            separators=["\n\n", "\n", "。", "！", "？", "，", " "]
        )

        docs = text_splitter.create_documents([text], metadatas=[doc_metadata])
        print(f"📝 [RagEngine] Chunking complete. Generated {len(docs)} text segments.")

        self.vector_store.add_documents(docs)
        print(f"🎉 [RagEngine] Success! '{source_filename or file_path}' has been appended to the vector database.")
