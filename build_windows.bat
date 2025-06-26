@echo off
REM Windows 应用构建脚本

echo 开始构建 Windows 应用程序...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
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
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

REM 创建图标
echo 创建应用图标...
python create_icon.py
if errorlevel 1 (
    echo ⚠️ 图标创建失败，继续构建...
)

REM 构建应用
echo 构建应用程序...
python build_app.py
if errorlevel 1 (
    echo ❌ 应用构建失败
    pause
    exit /b 1
)

REM 创建发布包
echo 创建发布包...
python create_release.py
if errorlevel 1 (
    echo ⚠️ 发布包创建失败
)

echo.
echo ✅ 构建完成！
echo 应用程序位于: dist\KeyboardAutomation.exe
echo 发布包位于: releases\
echo.
echo 使用说明:
echo 1. 双击运行 KeyboardAutomation.exe
echo 2. Windows 可能会显示安全警告，选择"仍要运行"
echo 3. 某些杀毒软件可能会误报，请添加到白名单
echo 4. 建议以管理员身份运行以获得完整功能
echo.

pause
