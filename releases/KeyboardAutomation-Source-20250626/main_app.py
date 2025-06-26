#!/usr/bin/env python3
"""
键盘自动化软件主程序 - 应用包版本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入GUI，但不导入权限检查
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, Any, Optional, List
from keyboard_automation.engine import KeyboardEngine, COMMON_KEYS, COMBINATION_TEMPLATES
from keyboard_automation.config import ConfigManager


class SimpleKeyboardGUI:
    """简化的键盘自动化GUI主界面"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("键盘自动化软件 v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 初始化组件
        self.engine = KeyboardEngine()
        self.config_manager = ConfigManager()
        
        # 界面变量
        self.current_config = None
        self.is_running = False
        
        # 设置停止回调
        self.engine.set_stop_callback(self.on_execution_stopped)
        
        # 创建界面
        self.create_widgets()
        self.load_config_list()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 创建各个区域
        self.create_config_area(main_frame)
        self.create_control_area(main_frame)
        self.create_sequence_area(main_frame)
        self.create_status_area(main_frame)
    
    def create_config_area(self, parent):
        """创建配置管理区域"""
        config_frame = ttk.LabelFrame(parent, text="配置管理", padding="5")
        config_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # 配置选择
        ttk.Label(config_frame, text="选择配置:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.config_var = tk.StringVar()
        self.config_combo = ttk.Combobox(config_frame, textvariable=self.config_var, state="readonly")
        self.config_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.config_combo.bind('<<ComboboxSelected>>', self.on_config_selected)
        
        # 配置操作按钮
        btn_frame = ttk.Frame(config_frame)
        btn_frame.grid(row=0, column=2, sticky=tk.E)
        
        ttk.Button(btn_frame, text="新建", command=self.new_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="保存", command=self.save_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="删除", command=self.delete_config).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="刷新", command=self.load_config_list).pack(side=tk.LEFT, padx=2)
    
    def create_control_area(self, parent):
        """创建控制区域"""
        control_frame = ttk.LabelFrame(parent, text="执行控制", padding="5")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(2, weight=1)
        
        # 重复设置
        ttk.Label(control_frame, text="重复次数:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.repeat_count_var = tk.IntVar(value=1)
        repeat_spin = ttk.Spinbox(control_frame, from_=1, to=9999, textvariable=self.repeat_count_var, width=10)
        repeat_spin.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        ttk.Label(control_frame, text="轮次间隔(秒):").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.repeat_interval_var = tk.DoubleVar(value=1.0)
        interval_spin = ttk.Spinbox(control_frame, from_=0.1, to=60.0, increment=0.1, 
                                   textvariable=self.repeat_interval_var, width=10)
        interval_spin.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        
        # 控制按钮
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=0, column=4, sticky=tk.E)
        
        self.start_btn = ttk.Button(btn_frame, text="开始执行", command=self.start_execution)
        self.start_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_btn = ttk.Button(btn_frame, text="停止执行", command=self.stop_execution, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=1, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def create_sequence_area(self, parent):
        """创建序列编辑区域"""
        sequence_frame = ttk.LabelFrame(parent, text="按键序列", padding="5")
        sequence_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        sequence_frame.columnconfigure(0, weight=1)
        sequence_frame.rowconfigure(1, weight=1)
        
        # 序列列表
        list_frame = ttk.Frame(sequence_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview
        columns = ('name', 'keys', 'count', 'interval')
        self.sequence_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        # 设置列标题
        self.sequence_tree.heading('name', text='序列名称')
        self.sequence_tree.heading('keys', text='按键')
        self.sequence_tree.heading('count', text='次数')
        self.sequence_tree.heading('interval', text='间隔(秒)')
        
        # 设置列宽
        self.sequence_tree.column('name', width=150)
        self.sequence_tree.column('keys', width=300)
        self.sequence_tree.column('count', width=80)
        self.sequence_tree.column('interval', width=80)
        
        self.sequence_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.sequence_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.sequence_tree.configure(yscrollcommand=scrollbar.set)
    
    def create_status_area(self, parent):
        """创建状态区域"""
        status_frame = ttk.LabelFrame(parent, text="状态信息", padding="5")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar(value="就绪 - 注意：需要在系统设置中授权辅助功能权限")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # 提示信息
        tip_text = "提示: 按ESC键可紧急停止执行 | 支持单键、组合键、文本输入 | 可设置随机间隔和随机顺序"
        ttk.Label(status_frame, text=tip_text, font=('TkDefaultFont', 8), foreground='gray').grid(row=1, column=0, sticky=tk.W)
    
    # 简化的方法实现
    def load_config_list(self):
        configs = self.config_manager.list_configs()
        self.config_combo['values'] = configs
        if configs and not self.config_var.get():
            self.config_var.set(configs[0])
            self.on_config_selected()
    
    def on_config_selected(self, event=None):
        config_name = self.config_var.get()
        if config_name:
            config = self.config_manager.load_config(config_name)
            if config:
                self.current_config = config
                self.load_config_to_ui(config)
                self.status_var.set(f"已加载配置: {config_name}")
    
    def load_config_to_ui(self, config: Dict[str, Any]):
        self.repeat_count_var.set(config.get('repeat_count', 1))
        self.repeat_interval_var.set(config.get('repeat_interval', 1.0))
        
        for item in self.sequence_tree.get_children():
            self.sequence_tree.delete(item)
        
        sequences = config.get('sequences', [])
        for i, sequence in enumerate(sequences):
            name = sequence.get('name', f'序列{i+1}')
            keys_desc = self.get_keys_description(sequence.get('keys', []))
            count = sequence.get('count', 1)
            interval = sequence.get('interval', 0.1)
            
            self.sequence_tree.insert('', 'end', values=(name, keys_desc, count, interval))
    
    def get_keys_description(self, keys: List[Dict[str, Any]]) -> str:
        descriptions = []
        for key_config in keys:
            key_type = key_config.get('type', 'single')
            if key_type == 'single':
                key = key_config.get('key', '')
                descriptions.append(key)
            elif key_type == 'combination':
                combo_keys = key_config.get('keys', [])
                descriptions.append('+'.join(combo_keys))
            elif key_type == 'text':
                text = key_config.get('text', '')
                descriptions.append(f'文本:"{text[:10]}..."' if len(text) > 10 else f'文本:"{text}"')
        
        return ', '.join(descriptions)
    
    def new_config(self):
        config = self.config_manager.create_default_config()
        self.current_config = config
        self.load_config_to_ui(config)
        self.status_var.set("已创建新配置")
    
    def save_config(self):
        if not self.current_config:
            messagebox.showwarning("警告", "没有可保存的配置")
            return
        
        name = simpledialog.askstring("保存配置", "请输入配置名称:")
        if not name:
            return
        
        self.current_config['repeat_count'] = self.repeat_count_var.get()
        self.current_config['repeat_interval'] = self.repeat_interval_var.get()
        
        if self.config_manager.save_config(self.current_config, name):
            self.load_config_list()
            self.config_var.set(name)
            self.status_var.set(f"配置已保存: {name}")
        else:
            messagebox.showerror("错误", "保存配置失败")
    
    def delete_config(self):
        config_name = self.config_var.get()
        if not config_name:
            messagebox.showwarning("警告", "请先选择要删除的配置")
            return
        
        if messagebox.askyesno("确认删除", f"确定要删除配置 '{config_name}' 吗？"):
            if self.config_manager.delete_config(config_name):
                self.load_config_list()
                self.status_var.set(f"配置已删除: {config_name}")
            else:
                messagebox.showerror("错误", "删除配置失败")
    
    def start_execution(self):
        if not self.current_config:
            messagebox.showwarning("警告", "请先选择或创建配置")
            return
        
        if self.is_running:
            messagebox.showwarning("警告", "程序正在执行中")
            return
        
        self.current_config['repeat_count'] = self.repeat_count_var.get()
        self.current_config['repeat_interval'] = self.repeat_interval_var.get()
        
        if self.engine.execute_config(self.current_config, self.update_progress):
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_var.set("正在执行...")
        else:
            messagebox.showerror("错误", "启动执行失败")
    
    def stop_execution(self):
        self.engine.stop()
        self.on_execution_stopped()
    
    def on_execution_stopped(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_var.set("执行已停止")
    
    def update_progress(self, progress: float, message: str):
        self.progress_var.set(progress)
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()
    
    def on_closing(self):
        """关闭事件处理"""
        if self.is_running:
            if messagebox.askokcancel("退出", "程序正在执行中，确定要退出吗？"):
                self.engine.stop()
                self.engine.cleanup()
                self.root.destroy()
        else:
            self.engine.cleanup()
            self.root.destroy()


def main():
    """主函数"""
    try:
        # 直接启动GUI，不进行权限检查
        app = SimpleKeyboardGUI()
        app.run()
    except Exception as e:
        # 在应用包中，将错误写入日志文件
        if os.environ.get('RESOURCEPATH'):
            try:
                log_path = os.path.expanduser("~/Library/Logs/KeyboardAutomation.log")
                os.makedirs(os.path.dirname(log_path), exist_ok=True)
                with open(log_path, 'a', encoding='utf-8') as f:
                    import traceback
                    from datetime import datetime
                    f.write(f"\n{datetime.now()}: {e}\n")
                    f.write(traceback.format_exc())
            except:
                pass
        else:
            print(f"程序运行出错: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
