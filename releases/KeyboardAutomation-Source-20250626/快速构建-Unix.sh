#!/bin/bash
echo "键盘自动化软件 - Unix快速启动"
echo "=============================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "安装依赖包..."
pip3 install -r requirements.txt

echo "创建图标..."
python3 create_icon.py

echo "构建应用程序..."
python3 build_app.py

echo "创建发布包..."
python3 create_release.py

echo "✅ 构建完成！"
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "应用程序位于: dist/KeyboardAutomation.app"
else
    echo "可执行文件位于: dist/KeyboardAutomation"
fi
echo "发布包位于: releases/"
