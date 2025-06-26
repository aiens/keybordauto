#!/bin/bash
# 云服务器快速打包脚本

echo "🌩️  键盘自动化软件 - 云服务器打包设置"
echo "============================================"

# 检测操作系统
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    PLATFORM="windows"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
else
    PLATFORM="unknown"
fi

echo "检测到平台: $PLATFORM"

# Windows设置
setup_windows() {
    echo "设置Windows环境..."
    
    # 检查Python
    if ! command -v python &> /dev/null; then
        echo "❌ 未找到Python，请先安装Python 3.8+"
        echo "下载地址: https://www.python.org/downloads/"
        exit 1
    fi
    
    # 安装依赖
    echo "安装Python依赖..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    # 构建应用
    echo "构建Windows应用..."
    python create_icon.py
    python build_app.py
    python create_release.py
    
    echo "✅ Windows版本构建完成！"
    echo "输出文件: releases/KeyboardAutomation-*-windows-*.zip"
}

# Linux设置
setup_linux() {
    echo "设置Linux环境..."
    
    # 更新包管理器
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3 python3-pip python3-tk python3-dev libx11-dev
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-pip python3-tkinter python3-devel libX11-devel
    elif command -v pacman &> /dev/null; then
        sudo pacman -S python python-pip tk libx11
    else
        echo "❌ 不支持的Linux发行版"
        exit 1
    fi
    
    # 安装Python依赖
    echo "安装Python依赖..."
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    
    # 构建应用
    echo "构建Linux应用..."
    python3 create_icon.py
    python3 build_app.py
    python3 create_release.py
    
    echo "✅ Linux版本构建完成！"
    echo "输出文件: releases/KeyboardAutomation-*-linux-*.tar.gz"
}

# macOS设置
setup_macos() {
    echo "设置macOS环境..."
    
    # 检查Homebrew
    if ! command -v brew &> /dev/null; then
        echo "安装Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # 安装Python
    brew install python@3.9
    
    # 安装依赖
    echo "安装Python依赖..."
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    
    # 构建应用
    echo "构建macOS应用..."
    python3 create_icon.py
    python3 build_app.py
    python3 create_release.py
    
    echo "✅ macOS版本构建完成！"
    echo "输出文件: releases/KeyboardAutomation-*-macos-*.tar.gz"
}

# 主逻辑
case $PLATFORM in
    "windows")
        setup_windows
        ;;
    "linux")
        setup_linux
        ;;
    "macos")
        setup_macos
        ;;
    *)
        echo "❌ 不支持的平台: $PLATFORM"
        exit 1
        ;;
esac

echo ""
echo "🎉 构建完成！"
echo "📁 输出目录: releases/"
echo "📦 可以将releases目录中的文件分发给用户"
echo ""
echo "📋 云服务器推荐:"
echo "- 阿里云ECS (中国)"
echo "- AWS EC2 (国际)"
echo "- 腾讯云CVM (中国)"
echo "- DigitalOcean (国际)"
echo ""
echo "💡 提示: 可以使用GitHub Actions自动化这个过程"
