#!/bin/bash

# RAG Knowledge Base - One-Click Run Script
# 使用方法: bash run.sh

set -e  # 错误时立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印帮助信息
print_help() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}   🤖 Corporate AI HR Assistant (RAG System)${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo "使用方法:"
    echo "  bash run.sh [选项]"
    echo ""
    echo "选项:"
    echo "  setup        - 首次安装（创建虚拟环境、安装依赖）"
    echo "  start        - 启动应用（后端 + 前端）"
    echo "  backend      - 只启动后端 (FastAPI)"
    echo "  frontend     - 只启动前端 (Streamlit)"
    echo "  test         - 运行测试"
    echo "  clean        - 清理临时文件和缓存"
    echo "  help         - 显示此帮助信息"
    echo ""
    echo "快速开始:"
    echo "  1. bash run.sh setup       # 首次运行"
    echo "  2. bash run.sh start       # 启动应用"
    echo ""
}

# 检查 Python 版本
check_python() {
    echo -e "${YELLOW}检查 Python 版本...${NC}"
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ 未找到 Python 3${NC}"
        echo "请访问 https://www.python.org 安装 Python 3.9+"
        exit 1
    fi

    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo -e "${GREEN}✅ Python 版本: $python_version${NC}"
}

# 创建虚拟环境
setup_venv() {
    echo -e "${YELLOW}创建虚拟环境...${NC}"
    if [ -d ".venv" ]; then
        echo -e "${BLUE}虚拟环境已存在，跳过创建${NC}"
    else
        python3 -m venv .venv
        echo -e "${GREEN}✅ 虚拟环境创建成功${NC}"
    fi
}

# 激活虚拟环境
activate_venv() {
    if [ ! -d ".venv" ]; then
        echo -e "${RED}❌ 虚拟环境不存在，请先运行: bash run.sh setup${NC}"
        exit 1
    fi
    source .venv/bin/activate
}

# 安装依赖
install_dependencies() {
    echo -e "${YELLOW}安装依赖包...${NC}"
    pip install --upgrade pip

    if [ -f "requirement.txt" ]; then
        pip install -r requirement.txt
        echo -e "${GREEN}✅ 依赖安装成功${NC}"
    else
        echo -e "${RED}❌ 找不到 requirement.txt${NC}"
        exit 1
    fi
}

# 首次设置
setup() {
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}    🚀 首次设置 - Setup${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"

    check_python
    setup_venv
    activate_venv
    install_dependencies

    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ 设置完成！${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "下一步:"
    echo -e "  ${BLUE}bash run.sh start${NC}       # 启动应用"
    echo ""
}

# 启动后端
start_backend() {
    echo -e "${BLUE}启动后端服务 (FastAPI)...${NC}"
    echo -e "${YELLOW}后端运行地址: http://127.0.0.1:8000${NC}"
    echo ""
    echo -e "${YELLOW}按 Ctrl+C 停止后端${NC}"
    echo ""

    activate_venv
    uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
}

# 启动前端
start_frontend() {
    echo -e "${BLUE}启动前端应用 (Streamlit)...${NC}"
    echo -e "${YELLOW}前端运行地址: http://localhost:8501${NC}"
    echo ""
    echo -e "${YELLOW}按 Ctrl+C 停止前端${NC}"
    echo ""

    activate_venv
    streamlit run frontend/app.py
}

# 同时启动前端和后端（需要两个终端）
start_all() {
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}    🚀 启动应用${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
    echo ""

    # 检查环境变量
    echo -e "${YELLOW}检查配置...${NC}"

    # 检查 LLM 模式
    if [ -z "$LLM_MODE" ]; then
        echo -e "${YELLOW}⚠️  LLM_MODE 未设置，默认使用 'deepseek'${NC}"
        echo -e "${YELLOW}   如需使用本地 LLM，运行: export LLM_MODE=ollama${NC}"
        export LLM_MODE="deepseek"
    else
        echo -e "${GREEN}✅ LLM_MODE: $LLM_MODE${NC}"
    fi

    # 如果使用 DeepSeek，检查 API 密钥
    if [ "$LLM_MODE" = "deepseek" ]; then
        if [ -z "$DEEPSEEK_TOKEN" ]; then
            echo -e "${RED}❌ 未设置 DEEPSEEK_TOKEN${NC}"
            echo -e "${YELLOW}请运行:${NC}"
            echo -e "  ${BLUE}export DEEPSEEK_TOKEN='your_api_key'${NC}"
            echo -e "${YELLOW}然后重新运行此脚本${NC}"
            exit 1
        else
            echo -e "${GREEN}✅ DEEPSEEK_TOKEN 已设置${NC}"
        fi
    fi

    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}需要在两个终端分别运行:${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${GREEN}终端 1 (后端):${NC}"
    echo -e "  ${YELLOW}bash run.sh backend${NC}"
    echo ""
    echo -e "${GREEN}终端 2 (前端):${NC}"
    echo -e "  ${YELLOW}bash run.sh frontend${NC}"
    echo ""
    echo -e "${BLUE}然后访问:${NC}"
    echo -e "  🌐 ${YELLOW}http://localhost:8501${NC}"
    echo ""
}

# 运行测试
run_tests() {
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}    🧪 运行测试${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"

    activate_venv

    echo ""
    echo -e "${YELLOW}1️⃣  测试 DeepSeek 流式 API...${NC}"
    if [ -z "$DEEPSEEK_TOKEN" ]; then
        echo -e "${RED}⚠️  跳过（未设置 DEEPSEEK_TOKEN）${NC}"
    else
        python backend/test_deepseek_stream.py
    fi

    echo ""
    echo -e "${YELLOW}2️⃣  测试多模态提取...${NC}"
    python backend/test_multimodal.py

    echo ""
    echo -e "${GREEN}✅ 测试完成${NC}"
}

# 清理临时文件
cleanup() {
    echo -e "${YELLOW}清理临时文件...${NC}"

    # 清理 Python 缓存
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

    # 清理 Streamlit 缓存
    rm -rf ~/.streamlit/cache 2>/dev/null || true

    echo -e "${GREEN}✅ 清理完成${NC}"
}

# 主程序
main() {
    case "${1:-help}" in
        setup)
            setup
            ;;
        start)
            start_all
            ;;
        backend)
            start_backend
            ;;
        frontend)
            start_frontend
            ;;
        test)
            run_tests
            ;;
        clean)
            cleanup
            ;;
        help)
            print_help
            ;;
        *)
            echo -e "${RED}未知命令: $1${NC}"
            print_help
            exit 1
            ;;
    esac
}

# 运行主程序
main "$@"
