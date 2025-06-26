@echo off
REM Windows 应用构建脚本

echo 开始构建 Windows 应用程序...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found, please install Python 3.8+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖
echo 检查依赖包...
python -c "import pyautogui, pynput, PIL" 2>nul
if errorlevel 1 (
    echo 安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

REM 创建图标
echo 创建应用图标...
python create_icon.py
if errorlevel 1 (
    echo [WARNING] Icon creation failed, continuing build...
)

REM 构建应用
echo 构建应用程序...
python build_app.py
if errorlevel 1 (
    echo [ERROR] Application build failed
    pause
    exit /b 1
)

REM 创建发布包
echo 创建发布包...
python create_release.py
if errorlevel 1 (
    echo [WARNING] Release package creation failed
)

echo.
echo [SUCCESS] Build completed!
echo Application location: dist\KeyboardAutomation.exe
echo Release packages: releases\
echo.
echo Usage instructions:
echo 1. Double-click to run KeyboardAutomation.exe
echo 2. Windows may show security warning, choose "Run anyway"
echo 3. Some antivirus may flag it, please add to whitelist
echo 4. Recommend running as administrator for full functionality
echo.

pause
