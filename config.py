# config.py
"""
Configuration for RAG system
Choose between cloud LLM (DeepSeek) or local LLM (Ollama)
"""

import os

# =============================================
# LLM Configuration
# =============================================

# Set to "deepseek" for cloud LLM or "ollama" for local LLM
LLM_MODE = os.environ.get("LLM_MODE", "deepseek").lower()

# Validate mode
if LLM_MODE not in ["deepseek", "ollama"]:
    print(f"⚠️  Invalid LLM_MODE: {LLM_MODE}")
    print("   Available: 'deepseek' or 'ollama'")
    print("   Setting to 'deepseek'")
    LLM_MODE = "deepseek"

# DeepSeek Configuration
DEEPSEEK_TOKEN = os.environ.get("DEEPSEEK_TOKEN", "")
DEEPSEEK_MODEL = "deepseek-v4-flash"
DEEPSEEK_API_BASE = "https://api.deepseek.com"

# Ollama Configuration (Local LLM)
OLLAMA_MODEL = "llama2"  # or "mistral", "neural-chat", etc.
OLLAMA_HOST = "http://localhost:11434"

# =============================================
# Vector Database Configuration
# =============================================

CHROMA_DB_PATH = "./chroma_db"
EMBEDDING_MODEL = "BAAI/bge-small-zh-v1.5"

# =============================================
# RAG Configuration
# =============================================

# Number of similar documents to retrieve
SIMILARITY_SEARCH_K = 5

# Text chunking parameters
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

# LLM parameters
LLM_TEMPERATURE = 0.2
LLM_MAX_TOKENS = None  # None = use default

# =============================================
# API Configuration
# =============================================

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 8000

# =============================================
# Helper Functions
# =============================================

def get_llm_info():
    """Get current LLM configuration info."""
    if LLM_MODE == "deepseek":
        if not DEEPSEEK_TOKEN:
            return {
                "mode": "deepseek",
                "status": "❌ Not configured",
                "message": "DeepSeek API key not found. Set DEEPSEEK_TOKEN environment variable.",
                "setup_url": "https://platform.deepseek.com"
            }
        return {
            "mode": "deepseek",
            "status": "✅ Configured",
            "model": DEEPSEEK_MODEL,
            "message": "Using cloud LLM (DeepSeek)"
        }
    else:
        return {
            "mode": "ollama",
            "status": "⚠️  Manual setup required",
            "model": OLLAMA_MODEL,
            "message": "Using local LLM (Ollama). Make sure Ollama is running.",
            "setup_url": "https://ollama.ai"
        }

def validate_config():
    """Validate configuration and print status."""
    print("\n" + "="*60)
    print("📋 RAG Configuration Check")
    print("="*60)

    llm_info = get_llm_info()
    print(f"\nLLM Mode: {llm_info['mode'].upper()}")
    print(f"Status: {llm_info['status']}")
    if "model" in llm_info:
        print(f"Model: {llm_info['model']}")
    print(f"Message: {llm_info['message']}")

    if llm_info.get("setup_url"):
        print(f"Setup: {llm_info['setup_url']}")

    print(f"\nVector DB: {CHROMA_DB_PATH}")
    print(f"Embedding: {EMBEDDING_MODEL}")
    print("="*60 + "\n")

if __name__ == "__main__":
    validate_config()
