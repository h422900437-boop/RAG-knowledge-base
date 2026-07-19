#!/bin/bash

# Installation script for RAG Knowledge Base dependencies

echo "🚀 Installing RAG Knowledge Base Dependencies"
echo "=============================================="

cd /Users/huangguowei/Desktop/RAG-knowledge-base

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "📥 Installing all dependencies from requirement.txt..."
pip install -r requirement.txt

echo ""
echo "✅ Dependency installation complete!"

echo ""
echo "🔍 Verifying critical dependencies..."
python -c "
import sys
packages = {
    'pypdf': 'PDF extraction',
    'docx': 'Word extraction (python-docx)',
    'openpyxl': 'Excel extraction',
    'langchain': 'LangChain core',
    'chromadb': 'Vector database',
    'sentence_transformers': 'Embedding model',
    'openai': 'OpenAI API client',
    'fastapi': 'FastAPI',
    'streamlit': 'Streamlit',
}

print()
all_ok = True
for package, description in packages.items():
    try:
        __import__(package)
        print(f'✅ {package:<25} - {description}')
    except ImportError:
        print(f'❌ {package:<25} - {description}')
        all_ok = False

print()
if all_ok:
    print('✅ All dependencies verified!')
else:
    print('⚠️  Some dependencies are missing. Try running pip install again.')
"

echo ""
echo "🎉 Setup complete! You can now start the application:"
echo "   1. Backend:  uvicorn backend.main:app --reload"
echo "   2. Frontend: streamlit run frontend/app.py"
