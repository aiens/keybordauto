#!/bin/bash
# 键盘自动化软件启动脚本（推荐版本）

echo "🚀 键盘自动化软件启动器"
echo "=========================="
echo ""

# 检查可执行文件是否存在
if [ -f "KeyboardAutomation" ]; then
    echo "✅ 找到可执行文件版本（推荐）"
    echo "正在启动..."
    chmod +x KeyboardAutomation
    ./KeyboardAutomation
elif [ -d "KeyboardAutomation.app" ]; then
    echo "⚠️  使用应用包版本（可能不稳定）"
    echo "如果出现问题，请使用可执行文件版本"
    open KeyboardAutomation.app
else
    echo "❌ 未找到应用程序文件"
    echo "请确保在正确的目录中运行此脚本"
    exit 1
fi

echo ""
echo "📋 使用说明:"
echo "1. 如果是首次运行，需要设置系统权限"
echo "2. 系统偏好设置 > 安全性与隐私 > 隐私 > 辅助功能"
echo "3. 添加应用程序到允许列表"
echo "4. 详细说明请查看'安装说明.md'"
echo ""
echo "🆘 如果遇到问题:"
echo "- 查看'应用包问题解决方案.md'"
echo "- 尝试重新设置权限"
echo "- 重启系统后再试"
