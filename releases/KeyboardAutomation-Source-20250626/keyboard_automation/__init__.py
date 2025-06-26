"""
键盘自动化软件包
提供键盘按键自动化功能，支持自定义按键、频率、次数、随机化和组合按键操作。
"""

__version__ = "1.0.0"
__author__ = "KeyboardSys"

from .engine import KeyboardEngine
from .config import ConfigManager
from .gui import KeyboardGUI
from .permissions import PermissionManager, check_and_request_permissions

__all__ = ['KeyboardEngine', 'ConfigManager', 'KeyboardGUI', 'PermissionManager', 'check_and_request_permissions']
