#!/bin/bash
# macOS 应用构建脚本

echo "开始构建 macOS 应用程序..."

# 检查依赖
python3 -c "import pyautogui, pynput, PIL" || {
    echo "安装依赖包..."
    pip3 install -r requirements.txt
}

# 构建应用
python3 build_app.py

echo "构建完成！"
echo "应用程序位于: dist/KeyboardAutomation.app"
echo ""
echo "使用说明:"
echo "1. 双击运行 KeyboardAutomation.app"
echo "2. 首次运行需要授权辅助功能权限"
echo "3. 系统偏好设置 > 安全性与隐私 > 隐私 > 辅助功能"
