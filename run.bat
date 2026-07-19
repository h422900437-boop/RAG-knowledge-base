@echo off
REM RAG Knowledge Base - One-Click Run Script for Windows
REM Usage: run.bat [option]

setlocal enabledelayedexpansion

:: 颜色定义
set "BLUE=[94m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "NC=[0m"

:: 打印帮助信息
if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="setup" goto setup
if "%1"=="start" goto start_all
if "%1"=="backend" goto backend
if "%1"=="frontend" goto frontend
if "%1"=="test" goto test
if "%1"=="clean" goto clean

echo %RED%错误: 未知命令 %1%NC%
goto help

:help
echo.
echo ═══════════════════════════════════════════════════════
echo    🤖 Corporate AI HR Assistant (RAG System)
echo ═══════════════════════════════════════════════════════
echo.
echo 使用方法:
echo   run.bat [选项]
echo.
echo 选项:
echo   setup        - 首次安装（创建虚拟环境、安装依赖）
echo   start        - 启动应用（后端 + 前端）
echo   backend      - 只启动后端 (FastAPI)
echo   frontend     - 只启动前端 (Streamlit)
echo   test         - 运行测试
echo   clean        - 清理临时文件和缓存
echo   help         - 显示此帮助信息
echo.
echo 快速开始:
echo   1. run.bat setup       # 首次运行
echo   2. run.bat start       # 启动应用
echo.
goto end

:check_python
if not exist ".venv" (
    echo.
    echo %YELLOW%检查 Python 版本...%NC%
    python --version >nul 2>&1
    if errorlevel 1 (
        echo %RED%❌ 未找到 Python 3%NC%
        echo 请访问 https://www.python.org 安装 Python 3.9+
        exit /b 1
    )
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo %GREEN%✅ Python 版本: !PYTHON_VERSION!%NC%
)
goto end

:setup_venv
if exist ".venv" (
    echo %BLUE%虚拟环境已存在，跳过创建%NC%
) else (
    echo %YELLOW%创建虚拟环境...%NC%
    python -m venv .venv
    echo %GREEN%✅ 虚拟环境创建成功%NC%
)
goto end

:activate_venv
if not exist ".venv\Scripts\activate.bat" (
    echo %RED%❌ 虚拟环境不存在，请先运行: run.bat setup%NC%
    exit /b 1
)
call .venv\Scripts\activate.bat
goto end

:install_dependencies
echo %YELLOW%安装依赖包...%NC%
python -m pip install --upgrade pip

if exist "requirement.txt" (
    pip install -r requirement.txt
    echo %GREEN%✅ 依赖安装成功%NC%
) else (
    echo %RED%❌ 找不到 requirement.txt%NC%
    exit /b 1
)
goto end

:setup
echo.
echo ════════════════════════════════════════════════════════
echo    🚀 首次设置 - Setup
echo ════════════════════════════════════════════════════════
echo.

call :check_python
call :setup_venv
call :activate_venv
call :install_dependencies

echo.
echo ════════════════════════════════════════════════════════
echo %GREEN%✅ 设置完成！%NC%
echo ════════════════════════════════════════════════════════
echo.
echo 下一步:
echo   %BLUE%run.bat start%NC%       # 启动应用
echo.
goto end

:start_backend
echo %BLUE%启动后端服务 (FastAPI)...%NC%
echo %YELLOW%后端运行地址: http://127.0.0.1:8000%NC%
echo.
echo %YELLOW%按 Ctrl+C 停止后端%NC%
echo.

call :activate_venv
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
goto end

:start_frontend
echo %BLUE%启动前端应用 (Streamlit)...%NC%
echo %YELLOW%前端运行地址: http://localhost:8501%NC%
echo.
echo %YELLOW%按 Ctrl+C 停止前端%NC%
echo.

call :activate_venv
streamlit run frontend/app.py
goto end

:start_all
echo.
echo ════════════════════════════════════════════════════════
echo    🚀 启动应用
echo ════════════════════════════════════════════════════════
echo.

echo %YELLOW%检查配置...%NC%

REM 检查 LLM 模式
if not defined LLM_MODE (
    echo %YELLOW%⚠️  LLM_MODE 未设置，默认使用 'deepseek'%NC%
    echo %YELLOW%   如需使用本地 LLM，运行: set LLM_MODE=ollama%NC%
    set LLM_MODE=deepseek
) else (
    echo %GREEN%✅ LLM_MODE: !LLM_MODE!%NC%
)

REM 如果使用 DeepSeek，检查 API 密钥
if "!LLM_MODE!"=="deepseek" (
    if not defined DEEPSEEK_TOKEN (
        echo %RED%❌ 未设置 DEEPSEEK_TOKEN%NC%
        echo %YELLOW%请运行:%NC%
        echo   %BLUE%set DEEPSEEK_TOKEN=your_api_key%NC%
        echo %YELLOW%然后重新运行此脚本%NC%
        exit /b 1
    ) else (
        echo %GREEN%✅ DEEPSEEK_TOKEN 已设置%NC%
    )
)

echo.
echo ════════════════════════════════════════════════════════
echo %BLUE%需要在两个终端分别运行:%NC%
echo ════════════════════════════════════════════════════════
echo.
echo %GREEN%终端 1 (后端):%NC%
echo   %YELLOW%run.bat backend%NC%
echo.
echo %GREEN%终端 2 (前端):%NC%
echo   %YELLOW%run.bat frontend%NC%
echo.
echo %BLUE%然后访问:%NC%
echo   🌐 %YELLOW%http://localhost:8501%NC%
echo.
goto end

:test
echo.
echo ════════════════════════════════════════════════════════
echo    🧪 运行测试
echo ════════════════════════════════════════════════════════

call :activate_venv

echo.
echo %YELLOW%1️⃣  测试多模态提取...%NC%
python backend/test_multimodal.py

echo.
echo %GREEN%✅ 测试完成%NC%
goto end

:clean
echo %YELLOW%清理临时文件...%NC%

REM 清理 Python 缓存
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" rmdir /s /q "%%d" 2>nul
)

del /s /q "*.pyc" >nul 2>&1

echo %GREEN%✅ 清理完成%NC%
goto end

:end
endlocal
