#!/usr/bin/env python3
"""
Automatic dependency installer for RAG Knowledge Base
Run this script to install all required packages
"""

import subprocess
import sys
import os

# List of all required packages
PACKAGES = [
    # Core LangChain & LLM
    "langchain>=0.1.0",
    "langchain-community>=0.0.0",
    "langchain-openai>=0.0.0",
    "langchain-text-splitters>=0.0.0",

    # Vector Database & Embeddings
    "chromadb>=0.4.0",
    "sentence-transformers>=2.2.0",

    # LLM & API
    "openai>=1.0.0",
    "tiktoken>=0.5.0",

    # Document Processing (Multimodal)
    "pypdf>=3.0.0",
    "python-docx>=0.8.0",
    "openpyxl>=3.0.0",

    # Web Framework
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "starlette>=0.27.0",

    # Frontend
    "streamlit>=1.28.0",

    # Utilities
    "pydantic>=2.0.0",
    "requests>=2.31.0",
]

def print_header(text):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def run_command(cmd):
    """Run a shell command and return success status."""
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        return False

def main():
    print_header("🚀 RAG Knowledge Base - Dependency Installer")

    # Check Python version
    print(f"📌 Python version: {sys.version}")
    print(f"📌 Python executable: {sys.executable}")

    if sys.version_info < (3, 9):
        print("❌ Error: Python 3.9+ required!")
        sys.exit(1)

    # Upgrade pip
    print("\n📦 Upgrading pip...")
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
    if not run_command(cmd):
        print("⚠️  Warning: pip upgrade failed, continuing anyway...")

    # Install all packages
    print_header("📥 Installing packages")
    print(f"Total packages to install: {len(PACKAGES)}\n")

    failed_packages = []
    installed_count = 0

    for package in PACKAGES:
        package_name = package.split(">=")[0].split("==")[0]
        print(f"  Installing {package_name}...", end=" ", flush=True)

        cmd = [sys.executable, "-m", "pip", "install", package, "-q"]
        if run_command(cmd):
            print("✅")
            installed_count += 1
        else:
            print("❌")
            failed_packages.append(package)

    # Summary
    print_header("📊 Installation Summary")
    print(f"✅ Successfully installed: {installed_count}/{len(PACKAGES)}")

    if failed_packages:
        print(f"\n❌ Failed packages ({len(failed_packages)}):")
        for pkg in failed_packages:
            print(f"   - {pkg}")
    else:
        print("\n🎉 All packages installed successfully!")

    # Verify critical packages
    print_header("🔍 Verifying critical packages")

    critical_packages = {
        'pypdf': 'PDF extraction',
        'docx': 'Word extraction (python-docx)',
        'openpyxl': 'Excel extraction',
        'langchain': 'LangChain core',
        'chromadb': 'Vector database',
        'openai': 'OpenAI API',
        'fastapi': 'FastAPI',
        'streamlit': 'Streamlit',
    }

    all_ok = True
    for package, description in critical_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {package:<25} - {description}")
        except ImportError:
            print(f"  ❌ {package:<25} - {description}")
            all_ok = False

    # Final message
    print_header("🎯 Next Steps")

    if all_ok:
        print("✅ All dependencies are installed!")
        print("\nYou can now start the application:")
        print("  1. Backend:  uvicorn backend.main:app --reload")
        print("  2. Frontend: streamlit run frontend/app.py")
    else:
        print("⚠️  Some packages are missing.")
        print("Try running this script again or install manually:")
        print(f"  pip install {' '.join(PACKAGES)}")

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
