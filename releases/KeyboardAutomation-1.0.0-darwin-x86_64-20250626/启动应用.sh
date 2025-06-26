#!/bin/bash
# macOS 启动脚本

echo "启动键盘自动化软件..."
echo "如果是首次运行，请按照提示设置权限"
echo ""

# 检查应用程序是否存在
if [ ! -d "KeyboardAutomation.app" ]; then
    echo "❌ 未找到 KeyboardAutomation.app"
    echo "请确保在正确的目录中运行此脚本"
    exit 1
fi

# 启动应用程序
open KeyboardAutomation.app

echo "✅ 应用程序已启动"
echo "如果遇到权限问题，请查看使用指南.md"
