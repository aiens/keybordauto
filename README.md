# 键盘自动化软件

一个功能强大的键盘自动化工具，支持自定义按键、频率、次数、随机化和组合按键操作。

## 功能特性

- 🎯 **自定义按键**: 支持所有键盘按键的自定义配置
- ⏱️ **灵活频率**: 可设置按键间隔时间和执行次数
- 🎲 **随机化**: 支持随机按键顺序和随机时间间隔
- 🔗 **组合按键**: 支持Ctrl+C、Alt+Tab等组合键操作
- 📋 **多配置**: 可保存和管理多套按键配置方案
- 🖥️ **图形界面**: 直观易用的GUI界面
- 🛡️ **安全控制**: 紧急停止功能，防止误操作

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py
```

## 项目结构

```
keyboardsys/
├── main.py              # 主程序入口
├── keyboard_automation/ # 核心模块
│   ├── __init__.py
│   ├── engine.py        # 键盘自动化引擎
│   ├── config.py        # 配置管理
│   └── gui.py           # 图形界面
├── configs/             # 配置文件目录
├── requirements.txt     # 依赖包列表
└── README.md           # 项目说明
```

## 📦 应用程序打包

### 快速打包
```bash
# 自动打包（推荐）
python3 build_app.py

# 创建发布包
python3 create_release.py
```

### 平台特定打包
```bash
# macOS
./build_macos.sh

# Windows
build_windows.bat

# Linux
./build_linux.sh
```

### 打包输出
- **macOS**: `dist/KeyboardAutomation.app`
- **Windows**: `dist/KeyboardAutomation.exe`
- **Linux**: `dist/KeyboardAutomation`

## 🔐 权限管理

软件内置智能权限管理系统：
- ✅ 自动检测系统权限状态
- ✅ 提供详细的权限设置指导
- ✅ 一键打开系统权限设置
- ✅ 实时权限状态显示

### macOS权限设置
1. 系统偏好设置 > 安全性与隐私 > 隐私 > 辅助功能
2. 添加应用程序到允许列表
3. 确保勾选对应的复选框

### Windows权限设置
1. 以管理员身份运行程序
2. 允许防火墙访问（如果询问）
3. 将程序添加到杀毒软件白名单

## 注意事项

- 使用前请确保了解相关法律法规
- 建议在测试环境中先试用
- 可通过ESC键或GUI界面停止自动化操作
- 打包后的应用程序包含完整运行时，体积较大属正常现象
