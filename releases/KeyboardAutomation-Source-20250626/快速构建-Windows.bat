@echo off
echo 键盘自动化软件 - Windows快速启动
echo ================================

echo 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 安装依赖包...
pip install -r requirements.txt

echo 创建图标...
python create_icon.py

echo 构建应用程序...
python build_app.py

echo 创建发布包...
python create_release.py

echo ✅ 构建完成！
echo 可执行文件位于: dist\KeyboardAutomation.exe
echo 发布包位于: releases\

pause
