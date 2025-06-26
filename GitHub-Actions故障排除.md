# GitHub Actions 故障排除指南

## 🔍 已修复的问题

### 1. ❌ `actions/upload-artifact: v3` 已弃用
**错误**: `This request has been automatically failed because it uses a deprecated version of actions/upload-artifact: v3`

**解决方案**: ✅ 已更新到 `actions/upload-artifact@v4`

### 2. ❌ 构建策略取消问题
**错误**: `The strategy configuration was canceled because "build.ubuntu-latest_linux_build" failed`

**解决方案**: ✅ 添加 `fail-fast: false` 配置

### 3. ❌ Linux GUI构建问题
**错误**: Linux环境下GUI应用构建失败

**解决方案**: ✅ 添加虚拟显示器 (Xvfb)

## 📋 新的GitHub Actions配置

### 主配置文件: `.github/workflows/build.yml`
- ✅ 使用最新版本的Actions
- ✅ 支持并行构建，互不影响
- ✅ 改进的错误处理
- ✅ 更详细的构建日志

### 简化配置文件: `.github/workflows/build-simple.yml`
- ✅ 分离的构建任务
- ✅ 更清晰的步骤划分
- ✅ 详细的发布说明

## 🚀 使用方法

### 方法1: 推送到GitHub仓库
```bash
# 1. 初始化Git仓库（如果还没有）
git init

# 2. 添加所有文件
git add .

# 3. 提交更改
git commit -m "Add keyboard automation software with GitHub Actions"

# 4. 添加远程仓库
git remote add origin https://github.com/yourusername/keyboard-automation.git

# 5. 推送到GitHub
git push -u origin main
```

### 方法2: 手动触发构建
1. 进入GitHub仓库页面
2. 点击 "Actions" 选项卡
3. 选择 "Simple Cross-Platform Build"
4. 点击 "Run workflow"

## 📦 构建输出

成功构建后，你将在GitHub Releases页面看到：

### Windows版本
- `KeyboardAutomation-*-windows-*.zip`
- 包含: `KeyboardAutomation.exe` + 启动脚本 + 文档

### macOS版本
- `KeyboardAutomation-*-macos-*.tar.gz`
- 包含: `KeyboardAutomation.app` + 启动脚本 + 文档

### Linux版本
- `KeyboardAutomation-*-linux-*.tar.gz`
- 包含: `KeyboardAutomation` + 启动脚本 + 文档

## 🔧 常见问题解决

### Q1: 构建失败怎么办？
1. 检查Actions页面的详细日志
2. 确认所有必要文件都已提交
3. 检查Python依赖是否正确

### Q2: 权限问题
确保GitHub仓库有以下权限：
- Actions: Read and write
- Contents: Read and write
- Metadata: Read

### Q3: 发布失败
检查是否有 `GITHUB_TOKEN` 权限：
1. 仓库设置 > Actions > General
2. Workflow permissions > Read and write permissions

### Q4: Linux构建失败
常见原因：
- 缺少系统依赖
- GUI相关问题
- 已通过虚拟显示器解决

## 📊 构建状态监控

### 查看构建状态
1. 进入GitHub仓库
2. 点击Actions选项卡
3. 查看最新的workflow运行状态

### 构建徽章
在README.md中添加构建状态徽章：
```markdown
![Build Status](https://github.com/yourusername/keyboard-automation/workflows/Simple%20Cross-Platform%20Build/badge.svg)
```

## 🎯 最佳实践

### 1. 分支策略
- `main/master`: 稳定版本，触发发布
- `develop`: 开发版本，仅构建测试
- `feature/*`: 功能分支，仅构建测试

### 2. 版本管理
- 使用Git标签管理版本
- 自动生成版本号
- 语义化版本控制

### 3. 构建优化
- 缓存Python依赖
- 并行构建不同平台
- 增量构建

## 🆘 紧急备用方案

如果GitHub Actions仍然有问题，可以使用以下备用方案：

### 1. 本地构建 + 手动上传
```bash
# 在各平台本地构建
python build_app.py
python create_release.py

# 手动上传到GitHub Releases
```

### 2. 云服务器构建
```bash
# 使用云服务器
./cloud_build_setup.sh
```

### 3. 源代码包分发
```bash
# 创建源代码包
python create_source_package.py

# 用户自行构建
```

## 📞 技术支持

如果遇到其他问题：
1. 检查GitHub Actions文档
2. 查看构建日志的详细错误信息
3. 使用源代码包作为备用方案
4. 考虑使用云服务器手动构建

---

**总结**: 已修复所有已知的GitHub Actions问题，现在应该可以正常进行跨平台自动构建了。如果还有问题，请使用备用方案确保软件的正常分发。
