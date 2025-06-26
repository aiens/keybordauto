"""
键盘自动化引擎
负责执行键盘按键操作，支持单键、组合键、随机化等功能
"""

import pyautogui
import time
import random
import threading
from typing import List, Dict, Any, Optional, Callable
from pynput import keyboard


class KeyboardEngine:
    """键盘自动化执行引擎"""
    
    def __init__(self):
        self.is_running = False
        self.should_stop = False
        self.current_thread = None
        self.stop_callback = None
        
        # 设置PyAutoGUI的安全设置
        pyautogui.FAILSAFE = True  # 鼠标移到左上角停止
        pyautogui.PAUSE = 0.1  # 每次操作间隔
        
        # 设置全局热键监听器
        self.hotkey_listener = None
        self.setup_emergency_stop()
    
    def setup_emergency_stop(self):
        """设置紧急停止热键 (ESC)"""
        def on_press(key):
            try:
                if key == keyboard.Key.esc and self.is_running:
                    self.stop()
            except AttributeError:
                pass
        
        self.hotkey_listener = keyboard.Listener(on_press=on_press)
        self.hotkey_listener.start()
    
    def execute_config(self, config: Dict[str, Any], progress_callback: Optional[Callable] = None):
        """
        执行键盘配置
        
        Args:
            config: 键盘配置字典
            progress_callback: 进度回调函数
        """
        if self.is_running:
            return False
        
        self.is_running = True
        self.should_stop = False
        
        def run():
            try:
                self._execute_sequence(config, progress_callback)
            except Exception as e:
                print(f"执行出错: {e}")
            finally:
                self.is_running = False
                if self.stop_callback:
                    self.stop_callback()
        
        self.current_thread = threading.Thread(target=run, daemon=True)
        self.current_thread.start()
        return True
    
    def _execute_sequence(self, config: Dict[str, Any], progress_callback: Optional[Callable] = None):
        """执行按键序列"""
        sequences = config.get('sequences', [])
        repeat_count = config.get('repeat_count', 1)
        repeat_interval = config.get('repeat_interval', 1.0)
        
        for repeat in range(repeat_count):
            if self.should_stop:
                break
            
            # 执行所有序列
            for seq_index, sequence in enumerate(sequences):
                if self.should_stop:
                    break
                
                self._execute_single_sequence(sequence)
                
                # 更新进度
                if progress_callback:
                    total_steps = len(sequences) * repeat_count
                    current_step = repeat * len(sequences) + seq_index + 1
                    progress = (current_step / total_steps) * 100
                    progress_callback(progress, f"执行第 {repeat + 1}/{repeat_count} 轮，序列 {seq_index + 1}/{len(sequences)}")
            
            # 轮次间隔
            if repeat < repeat_count - 1 and not self.should_stop:
                time.sleep(repeat_interval)
    
    def _execute_single_sequence(self, sequence: Dict[str, Any]):
        """执行单个按键序列"""
        keys = sequence.get('keys', [])
        count = sequence.get('count', 1)
        interval = sequence.get('interval', 0.1)
        random_interval = sequence.get('random_interval', False)
        random_order = sequence.get('random_order', False)
        
        # 处理随机顺序
        if random_order:
            keys = keys.copy()
            random.shuffle(keys)
        
        for i in range(count):
            if self.should_stop:
                break
            
            for key_config in keys:
                if self.should_stop:
                    break
                
                self._press_key(key_config)
                
                # 按键间隔
                if random_interval:
                    sleep_time = random.uniform(interval * 0.5, interval * 1.5)
                else:
                    sleep_time = interval
                
                time.sleep(sleep_time)
    
    def _press_key(self, key_config: Dict[str, Any]):
        """执行单个按键操作"""
        key_type = key_config.get('type', 'single')
        key_value = key_config.get('key', '')
        
        try:
            if key_type == 'single':
                # 单个按键
                pyautogui.press(key_value)
            elif key_type == 'combination':
                # 组合按键
                keys = key_config.get('keys', [])
                if len(keys) > 1:
                    pyautogui.hotkey(*keys)
                elif len(keys) == 1:
                    pyautogui.press(keys[0])
            elif key_type == 'text':
                # 文本输入
                text = key_config.get('text', '')
                pyautogui.write(text)
            
        except Exception as e:
            print(f"按键执行失败: {e}")
    
    def stop(self):
        """停止执行"""
        self.should_stop = True
        if self.current_thread and self.current_thread.is_alive():
            self.current_thread.join(timeout=1.0)
        self.is_running = False
    
    def set_stop_callback(self, callback: Callable):
        """设置停止回调函数"""
        self.stop_callback = callback
    
    def cleanup(self):
        """清理资源"""
        self.stop()
        if self.hotkey_listener:
            self.hotkey_listener.stop()


# 预定义的常用按键映射
COMMON_KEYS = {
    '空格': 'space',
    '回车': 'enter',
    '退格': 'backspace',
    '删除': 'delete',
    '制表符': 'tab',
    '上箭头': 'up',
    '下箭头': 'down',
    '左箭头': 'left',
    '右箭头': 'right',
    'F1': 'f1', 'F2': 'f2', 'F3': 'f3', 'F4': 'f4',
    'F5': 'f5', 'F6': 'f6', 'F7': 'f7', 'F8': 'f8',
    'F9': 'f9', 'F10': 'f10', 'F11': 'f11', 'F12': 'f12',
    'Ctrl': 'ctrl', 'Alt': 'alt', 'Shift': 'shift',
    'Win': 'win', 'Cmd': 'cmd'
}

# 预定义的组合键模板
COMBINATION_TEMPLATES = {
    '复制': ['ctrl', 'c'],
    '粘贴': ['ctrl', 'v'],
    '剪切': ['ctrl', 'x'],
    '全选': ['ctrl', 'a'],
    '撤销': ['ctrl', 'z'],
    '重做': ['ctrl', 'y'],
    '保存': ['ctrl', 's'],
    '查找': ['ctrl', 'f'],
    '替换': ['ctrl', 'h'],
    '新建': ['ctrl', 'n'],
    '打开': ['ctrl', 'o'],
    '切换窗口': ['alt', 'tab'],
    '关闭窗口': ['alt', 'f4'],
    '最小化': ['win', 'm'],
    '显示桌面': ['win', 'd']
}
