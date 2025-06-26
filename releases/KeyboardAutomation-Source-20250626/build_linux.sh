#!/bin/bash
# Linux 应用构建脚本

echo "开始构建 Linux 应用程序..."
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "Arch: sudo pacman -S python python-pip"
    exit 1
fi

# 检查系统依赖
echo "检查系统依赖..."
missing_deps=()

if ! dpkg -l | grep -q python3-tk 2>/dev/null && ! rpm -q python3-tkinter 2>/dev/null; then
    missing_deps+=("python3-tk/python3-tkinter")
fi

if ! dpkg -l | grep -q python3-dev 2>/dev/null && ! rpm -q python3-devel 2>/dev/null; then
    missing_deps+=("python3-dev/python3-devel")
fi

if [ ${#missing_deps[@]} -gt 0 ]; then
    echo "⚠️ 缺少系统依赖: ${missing_deps[*]}"
    echo "请安装缺少的依赖包："
    echo "Ubuntu/Debian: sudo apt install python3-tk python3-dev"
    echo "CentOS/RHEL: sudo yum install python3-tkinter python3-devel"
    echo "Arch: sudo pacman -S tk python"
    echo ""
    read -p "是否继续构建？(y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查Python依赖
echo "检查Python依赖..."
python3 -c "import pyautogui, pynput, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "安装Python依赖包..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

# 创建图标
echo "创建应用图标..."
python3 create_icon.py
if [ $? -ne 0 ]; then
    echo "⚠️ 图标创建失败，继续构建..."
fi

# 构建应用
echo "构建应用程序..."
python3 build_app.py
if [ $? -ne 0 ]; then
    echo "❌ 应用构建失败"
    exit 1
fi

# 设置执行权限
if [ -f "dist/KeyboardAutomation" ]; then
    chmod +x dist/KeyboardAutomation
    echo "✓ 已设置执行权限"
fi

# 创建发布包
echo "创建发布包..."
python3 create_release.py
if [ $? -ne 0 ]; then
    echo "⚠️ 发布包创建失败"
fi

echo ""
echo "✅ 构建完成！"
echo "应用程序位于: dist/KeyboardAutomation"
echo "发布包位于: releases/"
echo ""
echo "使用说明:"
echo "1. 运行: ./dist/KeyboardAutomation"
echo "2. 确保运行在X11环境下（不支持Wayland）"
echo "3. 可能需要设置DISPLAY环境变量"
echo "4. 某些发行版可能需要额外的权限设置"
echo ""

# 提供测试选项
read -p "是否现在测试应用程序？(y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "启动应用程序进行测试..."
    ./dist/KeyboardAutomation
fi
