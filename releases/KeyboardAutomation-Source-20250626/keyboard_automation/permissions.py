"""
权限管理模块
处理不同平台的权限检测、提示和设置
"""

import os
import sys
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Tuple, Optional
import webbrowser


class PermissionManager:
    """权限管理器"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.is_admin = self._check_admin_privileges()
    
    def _check_admin_privileges(self) -> bool:
        """检查是否有管理员权限"""
        try:
            if self.system == 'windows':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            elif self.system == 'darwin':
                # macOS 不需要管理员权限，但需要辅助功能权限
                return True
            else:
                return os.geteuid() == 0
        except Exception:
            return False
    
    def check_accessibility_permission(self) -> Tuple[bool, str]:
        """
        检查辅助功能权限
        
        Returns:
            Tuple[bool, str]: (是否有权限, 状态消息)
        """
        if self.system == 'darwin':
            return self._check_macos_accessibility()
        elif self.system == 'windows':
            return self._check_windows_accessibility()
        else:
            return self._check_linux_accessibility()
    
    def _check_macos_accessibility(self) -> Tuple[bool, str]:
        """检查macOS辅助功能权限"""
        try:
            # 使用更轻量级的方法检查权限
            import subprocess
            import os

            # 检查是否在应用包中运行
            bundle_path = os.environ.get('RESOURCEPATH')
            is_app_bundle = bundle_path is not None

            if is_app_bundle:
                # 在应用包中，使用系统API检查
                try:
                    result = subprocess.run([
                        'osascript', '-e',
                        'tell application "System Events" to get name of first process'
                    ], capture_output=True, text=True, timeout=5)

                    if result.returncode == 0:
                        return True, "辅助功能权限已授权"
                    else:
                        return False, "需要授权辅助功能权限"
                except subprocess.TimeoutExpired:
                    return False, "权限检查超时，可能需要授权"
                except Exception:
                    return False, "需要授权辅助功能权限"
            else:
                # 在命令行中，使用pynput测试
                from pynput import keyboard

                # 创建一个测试监听器
                def on_press(key):
                    pass

                listener = keyboard.Listener(on_press=on_press)
                listener.start()
                listener.stop()

                return True, "辅助功能权限已授权"

        except Exception as e:
            error_msg = str(e).lower()
            if "not trusted" in error_msg or "accessibility" in error_msg:
                return False, "需要授权辅助功能权限"
            else:
                return False, f"需要授权辅助功能权限"
    
    def _check_windows_accessibility(self) -> Tuple[bool, str]:
        """检查Windows权限"""
        try:
            # Windows通常不需要特殊权限，但可能被杀毒软件阻止
            import pyautogui
            pyautogui.position()  # 测试基本功能
            return True, "权限检查通过"
        except Exception as e:
            return False, f"权限检查失败: {e}"
    
    def _check_linux_accessibility(self) -> Tuple[bool, str]:
        """检查Linux权限"""
        try:
            # 检查X11权限
            display = os.environ.get('DISPLAY')
            if not display:
                return False, "需要X11显示权限"
            
            import pyautogui
            pyautogui.position()
            return True, "权限检查通过"
        except Exception as e:
            return False, f"权限检查失败: {e}"
    
    def show_permission_dialog(self, parent=None) -> bool:
        """
        显示权限设置对话框
        
        Args:
            parent: 父窗口
            
        Returns:
            bool: 用户是否选择继续
        """
        has_permission, message = self.check_accessibility_permission()
        
        if has_permission:
            return True
        
        dialog = PermissionDialog(parent, self.system, message)
        return dialog.result
    
    def open_system_preferences(self):
        """打开系统权限设置"""
        if self.system == 'darwin':
            self._open_macos_preferences()
        elif self.system == 'windows':
            self._open_windows_preferences()
        else:
            self._open_linux_preferences()
    
    def _open_macos_preferences(self):
        """打开macOS系统偏好设置"""
        try:
            # 打开辅助功能设置
            subprocess.run([
                'open', 
                'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'
            ])
        except Exception as e:
            print(f"无法打开系统偏好设置: {e}")
            # 备用方案：打开系统偏好设置主页
            try:
                subprocess.run(['open', '/System/Applications/System Preferences.app'])
            except Exception:
                pass
    
    def _open_windows_preferences(self):
        """打开Windows设置"""
        try:
            # 打开Windows设置
            subprocess.run(['ms-settings:privacy-general'], shell=True)
        except Exception:
            try:
                # 备用方案：打开控制面板
                subprocess.run(['control'], shell=True)
            except Exception as e:
                print(f"无法打开系统设置: {e}")
    
    def _open_linux_preferences(self):
        """打开Linux设置"""
        try:
            # 尝试不同的设置应用
            for cmd in ['gnome-control-center', 'systemsettings5', 'unity-control-center']:
                try:
                    subprocess.run([cmd], check=True)
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
        except Exception as e:
            print(f"无法打开系统设置: {e}")


class PermissionDialog:
    """权限设置对话框"""
    
    def __init__(self, parent, system: str, message: str):
        self.result = False
        self.system = system
        self.message = message
        
        # 创建对话框
        self.dialog = tk.Toplevel(parent) if parent else tk.Tk()
        self.dialog.title("权限设置")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        if parent:
            self.dialog.transient(parent)
            self.dialog.grab_set()
            # 居中显示
            self.dialog.geometry("+%d+%d" % (
                parent.winfo_rootx() + 50, 
                parent.winfo_rooty() + 50
            ))
        
        self.create_widgets()
        self.dialog.wait_window()
    
    def create_widgets(self):
        """创建对话框组件"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame, 
            text="⚠️ 需要系统权限", 
            font=('TkDefaultFont', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # 消息
        message_label = ttk.Label(
            main_frame, 
            text=self.message,
            font=('TkDefaultFont', 12)
        )
        message_label.pack(pady=(0, 20))
        
        # 说明文本
        instructions = self._get_instructions()
        
        # 创建滚动文本框
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        text_widget = tk.Text(
            text_frame, 
            wrap=tk.WORD, 
            height=12,
            font=('TkDefaultFont', 10)
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.insert(tk.END, instructions)
        text_widget.configure(state=tk.DISABLED)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # 打开设置按钮
        ttk.Button(
            button_frame, 
            text="打开系统设置", 
            command=self.open_settings
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 帮助按钮
        ttk.Button(
            button_frame, 
            text="在线帮助", 
            command=self.open_help
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # 继续按钮
        ttk.Button(
            button_frame, 
            text="我已设置完成", 
            command=self.continue_clicked
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        # 退出按钮
        ttk.Button(
            button_frame, 
            text="退出程序", 
            command=self.exit_clicked
        ).pack(side=tk.RIGHT)
    
    def _get_instructions(self) -> str:
        """获取平台特定的设置说明"""
        if self.system == 'darwin':
            return """macOS 权限设置步骤：

1. 点击下方"打开系统设置"按钮，或手动打开"系统偏好设置"

2. 进入"安全性与隐私" > "隐私"选项卡

3. 在左侧列表中找到"辅助功能"

4. 点击左下角的锁图标，输入管理员密码解锁

5. 在右侧应用列表中找到"KeyboardAutomation"或"Terminal"

6. 勾选对应的复选框以授权访问

7. 如果列表中没有应用，点击"+"按钮手动添加

8. 重新启动本应用程序

注意：
- 某些版本的macOS可能需要重启应用才能生效
- 如果仍然无法使用，请尝试移除后重新添加应用
- 确保应用程序没有被其他安全软件阻止"""

        elif self.system == 'windows':
            return """Windows 权限设置步骤：

1. 确保以管理员身份运行程序（右键 > 以管理员身份运行）

2. 如果Windows Defender或其他杀毒软件弹出警告：
   - 选择"允许"或"信任"
   - 将程序添加到白名单

3. 如果程序被阻止运行：
   - 右键程序文件 > 属性 > 解除锁定
   - 或在Windows安全中心添加排除项

4. 某些企业版Windows可能需要组策略设置

5. 确保没有其他安全软件阻止程序运行

注意：
- 本程序是安全的键盘自动化工具
- 杀毒软件可能会误报，这是正常现象
- 如有疑虑，可以查看源代码或联系技术支持"""

        else:
            return """Linux 权限设置步骤：

1. 确保运行在X11环境下（不支持Wayland）

2. 检查DISPLAY环境变量是否设置正确

3. 如果使用SSH连接，需要启用X11转发：
   ssh -X username@hostname

4. 某些发行版可能需要安装额外包：
   - Ubuntu/Debian: sudo apt install python3-tk python3-dev
   - CentOS/RHEL: sudo yum install tkinter python3-devel
   - Arch: sudo pacman -S tk python

5. 检查用户是否在input组中：
   sudo usermod -a -G input $USER

6. 重新登录或重启系统

注意：
- 不同Linux发行版的设置可能有所不同
- 某些桌面环境可能有额外的安全限制"""
    
    def open_settings(self):
        """打开系统设置"""
        permission_manager = PermissionManager()
        permission_manager.open_system_preferences()
    
    def open_help(self):
        """打开在线帮助"""
        help_urls = {
            'darwin': 'https://support.apple.com/guide/mac-help/allow-accessibility-apps-to-access-your-mac-mh43185/mac',
            'windows': 'https://support.microsoft.com/windows/windows-security-4fc0ebbc-79fe-4d95-8b54-2d4ac37b2f29',
            'linux': 'https://wiki.archlinux.org/title/Xorg'
        }
        
        url = help_urls.get(self.system, 'https://github.com')
        webbrowser.open(url)
    
    def continue_clicked(self):
        """继续按钮点击"""
        self.result = True
        self.dialog.destroy()
    
    def exit_clicked(self):
        """退出按钮点击"""
        self.result = False
        self.dialog.destroy()


def check_and_request_permissions(parent=None) -> bool:
    """
    检查并请求必要权限

    Args:
        parent: 父窗口

    Returns:
        bool: 是否获得权限或用户选择继续
    """
    import os

    permission_manager = PermissionManager()

    # 检查是否在应用包中运行
    is_app_bundle = os.environ.get('RESOURCEPATH') is not None

    if is_app_bundle:
        # 在应用包中，只检查权限，不显示对话框
        has_permission, _ = permission_manager.check_accessibility_permission()
        return True  # 总是允许继续，让GUI中的权限检查来处理
    else:
        # 在命令行中，显示权限对话框
        return permission_manager.show_permission_dialog(parent)
