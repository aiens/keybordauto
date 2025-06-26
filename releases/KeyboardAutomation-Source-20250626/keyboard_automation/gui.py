"""
图形用户界面模块
提供直观的GUI界面用于配置和控制键盘自动化
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import threading
from typing import Dict, Any, Optional, List
from .engine import KeyboardEngine, COMMON_KEYS, COMBINATION_TEMPLATES
from .config import ConfigManager
from .permissions import PermissionManager


class KeyboardGUI:
    """键盘自动化GUI主界面"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("键盘自动化软件 v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 初始化组件
        self.engine = KeyboardEngine()
        self.config_manager = ConfigManager()
        self.permission_manager = PermissionManager()

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
        
        # 序列操作按钮
        seq_btn_frame = ttk.Frame(sequence_frame)
        seq_btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(seq_btn_frame, text="添加序列", command=self.add_sequence).pack(side=tk.LEFT, padx=2)
        ttk.Button(seq_btn_frame, text="编辑序列", command=self.edit_sequence).pack(side=tk.LEFT, padx=2)
        ttk.Button(seq_btn_frame, text="删除序列", command=self.delete_sequence).pack(side=tk.LEFT, padx=2)
        ttk.Button(seq_btn_frame, text="上移", command=self.move_sequence_up).pack(side=tk.LEFT, padx=2)
        ttk.Button(seq_btn_frame, text="下移", command=self.move_sequence_down).pack(side=tk.LEFT, padx=2)
        
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

        # 主状态
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.grid(row=0, column=0, sticky=tk.W)

        # 权限状态
        permission_frame = ttk.Frame(status_frame)
        permission_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        permission_frame.columnconfigure(0, weight=1)

        self.permission_var = tk.StringVar()
        self.permission_label = ttk.Label(permission_frame, textvariable=self.permission_var, font=('TkDefaultFont', 9))
        self.permission_label.grid(row=0, column=0, sticky=tk.W)

        ttk.Button(permission_frame, text="检查权限", command=self.check_permissions, width=10).grid(row=0, column=1, sticky=tk.E, padx=(5, 0))

        # 提示信息
        tip_text = "提示: 按ESC键可紧急停止执行 | 支持单键、组合键、文本输入 | 可设置随机间隔和随机顺序"
        ttk.Label(status_frame, text=tip_text, font=('TkDefaultFont', 8), foreground='gray').grid(row=2, column=0, sticky=tk.W, pady=(5, 0))

        # 初始权限检查
        self.check_permissions()
    
    def load_config_list(self):
        """加载配置列表"""
        configs = self.config_manager.list_configs()
        self.config_combo['values'] = configs
        if configs and not self.config_var.get():
            self.config_var.set(configs[0])
            self.on_config_selected()
    
    def on_config_selected(self, event=None):
        """配置选择事件"""
        config_name = self.config_var.get()
        if config_name:
            config = self.config_manager.load_config(config_name)
            if config:
                self.current_config = config
                self.load_config_to_ui(config)
                self.status_var.set(f"已加载配置: {config_name}")
    
    def load_config_to_ui(self, config: Dict[str, Any]):
        """将配置加载到界面"""
        # 设置重复参数
        self.repeat_count_var.set(config.get('repeat_count', 1))
        self.repeat_interval_var.set(config.get('repeat_interval', 1.0))
        
        # 清空并加载序列列表
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
        """获取按键描述"""
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

    def check_permissions(self):
        """检查权限状态"""
        try:
            has_permission, message = self.permission_manager.check_accessibility_permission()
            if has_permission:
                self.permission_var.set("✓ " + message)
                self.permission_label.config(foreground='green')
            else:
                self.permission_var.set("⚠️ " + message)
                self.permission_label.config(foreground='red')
        except Exception as e:
            self.permission_var.set(f"❌ 权限检查失败: {e}")
            self.permission_label.config(foreground='red')

    def run(self):
        """运行GUI"""
        self.root.mainloop()
    
    def new_config(self):
        """新建配置"""
        config = self.config_manager.create_default_config()
        self.current_config = config
        self.load_config_to_ui(config)
        self.status_var.set("已创建新配置")

    def save_config(self):
        """保存配置"""
        if not self.current_config:
            messagebox.showwarning("警告", "没有可保存的配置")
            return

        # 获取配置名称
        name = simpledialog.askstring("保存配置", "请输入配置名称:")
        if not name:
            return

        # 从界面更新配置
        self.update_config_from_ui()

        if self.config_manager.save_config(self.current_config, name):
            self.load_config_list()
            self.config_var.set(name)
            self.status_var.set(f"配置已保存: {name}")
        else:
            messagebox.showerror("错误", "保存配置失败")

    def delete_config(self):
        """删除配置"""
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

    def update_config_from_ui(self):
        """从界面更新配置"""
        if not self.current_config:
            return

        self.current_config['repeat_count'] = self.repeat_count_var.get()
        self.current_config['repeat_interval'] = self.repeat_interval_var.get()

        # 从序列树获取序列数据
        sequences = []
        for item in self.sequence_tree.get_children():
            # 这里需要从实际的序列数据中获取，暂时保持原有数据
            pass

        # 保持原有序列数据不变，只更新重复参数

    def start_execution(self):
        """开始执行"""
        if not self.current_config:
            messagebox.showwarning("警告", "请先选择或创建配置")
            return

        if self.is_running:
            messagebox.showwarning("警告", "程序正在执行中")
            return

        # 更新配置
        self.update_config_from_ui()

        # 开始执行
        if self.engine.execute_config(self.current_config, self.update_progress):
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_var.set("正在执行...")
        else:
            messagebox.showerror("错误", "启动执行失败")

    def stop_execution(self):
        """停止执行"""
        self.engine.stop()
        self.on_execution_stopped()

    def on_execution_stopped(self):
        """执行停止回调"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_var.set("执行已停止")

    def update_progress(self, progress: float, message: str):
        """更新进度"""
        self.progress_var.set(progress)
        self.status_var.set(message)
        self.root.update_idletasks()

    def add_sequence(self):
        """添加序列"""
        dialog = SequenceEditDialog(self.root, "添加序列")
        if dialog.result:
            sequence = dialog.result
            name = sequence.get('name', '新序列')
            keys_desc = self.get_keys_description(sequence.get('keys', []))
            count = sequence.get('count', 1)
            interval = sequence.get('interval', 0.1)

            self.sequence_tree.insert('', 'end', values=(name, keys_desc, count, interval))

            # 更新配置
            if not self.current_config:
                self.current_config = self.config_manager.create_default_config()
                self.current_config['sequences'] = []

            self.current_config['sequences'].append(sequence)
            self.status_var.set("已添加新序列")

    def edit_sequence(self):
        """编辑序列"""
        selection = self.sequence_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要编辑的序列")
            return

        item = selection[0]
        index = self.sequence_tree.index(item)

        if self.current_config and index < len(self.current_config.get('sequences', [])):
            sequence = self.current_config['sequences'][index]
            dialog = SequenceEditDialog(self.root, "编辑序列", sequence)

            if dialog.result:
                # 更新序列
                self.current_config['sequences'][index] = dialog.result

                # 更新界面
                sequence = dialog.result
                name = sequence.get('name', '序列')
                keys_desc = self.get_keys_description(sequence.get('keys', []))
                count = sequence.get('count', 1)
                interval = sequence.get('interval', 0.1)

                self.sequence_tree.item(item, values=(name, keys_desc, count, interval))
                self.status_var.set("序列已更新")

    def delete_sequence(self):
        """删除序列"""
        selection = self.sequence_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的序列")
            return

        if messagebox.askyesno("确认删除", "确定要删除选中的序列吗？"):
            item = selection[0]
            index = self.sequence_tree.index(item)

            # 从配置中删除
            if self.current_config and index < len(self.current_config.get('sequences', [])):
                del self.current_config['sequences'][index]

            # 从界面删除
            self.sequence_tree.delete(item)
            self.status_var.set("序列已删除")

    def move_sequence_up(self):
        """上移序列"""
        selection = self.sequence_tree.selection()
        if not selection:
            return

        item = selection[0]
        index = self.sequence_tree.index(item)

        if index > 0:
            # 交换配置中的位置
            if self.current_config and len(self.current_config.get('sequences', [])) > index:
                sequences = self.current_config['sequences']
                sequences[index], sequences[index-1] = sequences[index-1], sequences[index]

            # 交换界面中的位置
            self.sequence_tree.move(item, '', index-1)

    def move_sequence_down(self):
        """下移序列"""
        selection = self.sequence_tree.selection()
        if not selection:
            return

        item = selection[0]
        index = self.sequence_tree.index(item)

        if index < len(self.sequence_tree.get_children()) - 1:
            # 交换配置中的位置
            if self.current_config and len(self.current_config.get('sequences', [])) > index + 1:
                sequences = self.current_config['sequences']
                sequences[index], sequences[index+1] = sequences[index+1], sequences[index]

            # 交换界面中的位置
            self.sequence_tree.move(item, '', index+1)

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


class SequenceEditDialog:
    """序列编辑对话框"""

    def __init__(self, parent, title: str, sequence: Optional[Dict[str, Any]] = None):
        self.result = None
        self.sequence = sequence or {
            'name': '新序列',
            'keys': [],
            'count': 1,
            'interval': 0.1,
            'random_interval': False,
            'random_order': False
        }

        # 创建对话框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # 居中显示
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        self.create_widgets()
        self.load_sequence()

        # 等待对话框关闭
        self.dialog.wait_window()

    def create_widgets(self):
        """创建对话框组件"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 基本设置
        basic_frame = ttk.LabelFrame(main_frame, text="基本设置", padding="5")
        basic_frame.pack(fill=tk.X, pady=(0, 10))

        # 序列名称
        ttk.Label(basic_frame, text="序列名称:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.name_var = tk.StringVar()
        ttk.Entry(basic_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, sticky=(tk.W, tk.E))

        # 执行次数
        ttk.Label(basic_frame, text="执行次数:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.count_var = tk.IntVar()
        ttk.Spinbox(basic_frame, from_=1, to=9999, textvariable=self.count_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=(5, 0))

        # 按键间隔
        ttk.Label(basic_frame, text="按键间隔(秒):").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.interval_var = tk.DoubleVar()
        ttk.Spinbox(basic_frame, from_=0.01, to=10.0, increment=0.01, textvariable=self.interval_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=(5, 0))

        # 随机选项
        self.random_interval_var = tk.BooleanVar()
        ttk.Checkbutton(basic_frame, text="随机间隔", variable=self.random_interval_var).grid(row=3, column=0, sticky=tk.W, pady=(5, 0))

        self.random_order_var = tk.BooleanVar()
        ttk.Checkbutton(basic_frame, text="随机顺序", variable=self.random_order_var).grid(row=3, column=1, sticky=tk.W, pady=(5, 0))

        basic_frame.columnconfigure(1, weight=1)

        # 按键设置
        keys_frame = ttk.LabelFrame(main_frame, text="按键设置", padding="5")
        keys_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 按键操作按钮
        btn_frame = ttk.Frame(keys_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(btn_frame, text="添加单键", command=self.add_single_key).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="添加组合键", command=self.add_combination_key).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="添加文本", command=self.add_text).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="删除", command=self.delete_key).pack(side=tk.LEFT, padx=2)

        # 按键列表
        list_frame = ttk.Frame(keys_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('type', 'content')
        self.keys_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        self.keys_tree.heading('type', text='类型')
        self.keys_tree.heading('content', text='内容')
        self.keys_tree.column('type', width=100)
        self.keys_tree.column('content', width=400)

        self.keys_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        keys_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.keys_tree.yview)
        keys_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.keys_tree.configure(yscrollcommand=keys_scrollbar.set)

        # 对话框按钮
        dialog_btn_frame = ttk.Frame(main_frame)
        dialog_btn_frame.pack(fill=tk.X)

        ttk.Button(dialog_btn_frame, text="确定", command=self.ok_clicked).pack(side=tk.RIGHT, padx=2)
        ttk.Button(dialog_btn_frame, text="取消", command=self.cancel_clicked).pack(side=tk.RIGHT, padx=2)

    def load_sequence(self):
        """加载序列数据到界面"""
        self.name_var.set(self.sequence.get('name', ''))
        self.count_var.set(self.sequence.get('count', 1))
        self.interval_var.set(self.sequence.get('interval', 0.1))
        self.random_interval_var.set(self.sequence.get('random_interval', False))
        self.random_order_var.set(self.sequence.get('random_order', False))

        # 加载按键列表
        for key_config in self.sequence.get('keys', []):
            self.add_key_to_tree(key_config)

    def add_key_to_tree(self, key_config: Dict[str, Any]):
        """添加按键到树形控件"""
        key_type = key_config.get('type', 'single')
        if key_type == 'single':
            content = key_config.get('key', '')
        elif key_type == 'combination':
            content = '+'.join(key_config.get('keys', []))
        elif key_type == 'text':
            content = f'"{key_config.get("text", "")}"'
        else:
            content = str(key_config)

        self.keys_tree.insert('', 'end', values=(key_type, content))

    def add_single_key(self):
        """添加单键"""
        dialog = KeySelectionDialog(self.dialog, "选择按键", COMMON_KEYS)
        if dialog.result:
            key_config = {'type': 'single', 'key': dialog.result}
            self.add_key_to_tree(key_config)

    def add_combination_key(self):
        """添加组合键"""
        dialog = CombinationKeyDialog(self.dialog, "组合键设置")
        if dialog.result:
            key_config = {'type': 'combination', 'keys': dialog.result}
            self.add_key_to_tree(key_config)

    def add_text(self):
        """添加文本"""
        text = simpledialog.askstring("文本输入", "请输入要输入的文本:")
        if text:
            key_config = {'type': 'text', 'text': text}
            self.add_key_to_tree(key_config)

    def delete_key(self):
        """删除按键"""
        selection = self.keys_tree.selection()
        if selection:
            self.keys_tree.delete(selection[0])

    def ok_clicked(self):
        """确定按钮点击"""
        # 收集按键数据
        keys = []
        for item in self.keys_tree.get_children():
            values = self.keys_tree.item(item)['values']
            key_type = values[0]
            content = values[1]

            if key_type == 'single':
                keys.append({'type': 'single', 'key': content})
            elif key_type == 'combination':
                combo_keys = content.split('+')
                keys.append({'type': 'combination', 'keys': combo_keys})
            elif key_type == 'text':
                text = content.strip('"')
                keys.append({'type': 'text', 'text': text})

        # 构建结果
        self.result = {
            'name': self.name_var.get() or '新序列',
            'keys': keys,
            'count': self.count_var.get(),
            'interval': self.interval_var.get(),
            'random_interval': self.random_interval_var.get(),
            'random_order': self.random_order_var.get()
        }

        self.dialog.destroy()

    def cancel_clicked(self):
        """取消按钮点击"""
        self.result = None
        self.dialog.destroy()


class KeySelectionDialog:
    """按键选择对话框"""

    def __init__(self, parent, title: str, key_mapping: Dict[str, str]):
        self.result = None
        self.key_mapping = key_mapping

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.create_widgets()
        self.dialog.wait_window()

    def create_widgets(self):
        """创建组件"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 按键列表
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.key_listbox = tk.Listbox(list_frame)
        self.key_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.key_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.key_listbox.configure(yscrollcommand=scrollbar.set)

        # 填充按键列表
        for display_name, key_value in self.key_mapping.items():
            self.key_listbox.insert(tk.END, f"{display_name} ({key_value})")

        # 自定义输入
        custom_frame = ttk.Frame(main_frame)
        custom_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(custom_frame, text="或输入自定义按键:").pack(anchor=tk.W)
        self.custom_var = tk.StringVar()
        ttk.Entry(custom_frame, textvariable=self.custom_var).pack(fill=tk.X, pady=(5, 0))

        # 按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="确定", command=self.ok_clicked).pack(side=tk.RIGHT, padx=2)
        ttk.Button(btn_frame, text="取消", command=self.cancel_clicked).pack(side=tk.RIGHT, padx=2)

    def ok_clicked(self):
        """确定按钮点击"""
        custom_key = self.custom_var.get().strip()
        if custom_key:
            self.result = custom_key
        else:
            selection = self.key_listbox.curselection()
            if selection:
                selected_text = self.key_listbox.get(selection[0])
                # 提取括号中的按键值
                key_value = selected_text.split('(')[1].split(')')[0]
                self.result = key_value

        self.dialog.destroy()

    def cancel_clicked(self):
        """取消按钮点击"""
        self.result = None
        self.dialog.destroy()


class CombinationKeyDialog:
    """组合键设置对话框"""

    def __init__(self, parent, title: str):
        self.result = None
        self.selected_keys = []

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.create_widgets()
        self.load_templates()
        self.dialog.wait_window()

    def create_widgets(self):
        """创建组件"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 预设模板
        template_frame = ttk.LabelFrame(main_frame, text="常用组合键", padding="5")
        template_frame.pack(fill=tk.X, pady=(0, 10))

        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(template_frame, textvariable=self.template_var, state="readonly")
        self.template_combo.pack(fill=tk.X, pady=(0, 5))
        self.template_combo.bind('<<ComboboxSelected>>', self.on_template_selected)

        ttk.Button(template_frame, text="使用模板", command=self.use_template).pack()

        # 自定义组合
        custom_frame = ttk.LabelFrame(main_frame, text="自定义组合键", padding="5")
        custom_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 可用按键
        available_frame = ttk.Frame(custom_frame)
        available_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(available_frame, text="可用按键:").pack(anchor=tk.W)

        keys_frame = ttk.Frame(available_frame)
        keys_frame.pack(fill=tk.X, pady=(5, 10))

        # 修饰键
        modifier_keys = ['ctrl', 'alt', 'shift', 'win', 'cmd']
        for key in modifier_keys:
            ttk.Button(keys_frame, text=key.upper(), width=8,
                      command=lambda k=key: self.add_key(k)).pack(side=tk.LEFT, padx=2)

        # 字母数字键
        alpha_frame = ttk.Frame(available_frame)
        alpha_frame.pack(fill=tk.X, pady=(0, 10))

        # 字母键
        for i, char in enumerate('abcdefghijklmnopqrstuvwxyz'):
            if i % 13 == 0:
                row_frame = ttk.Frame(alpha_frame)
                row_frame.pack(fill=tk.X, pady=1)
            ttk.Button(row_frame, text=char.upper(), width=3,
                      command=lambda c=char: self.add_key(c)).pack(side=tk.LEFT, padx=1)

        # 已选择的按键
        selected_frame = ttk.Frame(custom_frame)
        selected_frame.pack(fill=tk.X)

        ttk.Label(selected_frame, text="已选择的按键:").pack(anchor=tk.W)
        self.selected_var = tk.StringVar()
        self.selected_label = ttk.Label(selected_frame, textvariable=self.selected_var,
                                       background='white', relief='sunken')
        self.selected_label.pack(fill=tk.X, pady=(5, 5))

        ttk.Button(selected_frame, text="清除", command=self.clear_keys).pack()

        # 按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="确定", command=self.ok_clicked).pack(side=tk.RIGHT, padx=2)
        ttk.Button(btn_frame, text="取消", command=self.cancel_clicked).pack(side=tk.RIGHT, padx=2)

    def load_templates(self):
        """加载模板"""
        templates = list(COMBINATION_TEMPLATES.keys())
        self.template_combo['values'] = templates

    def on_template_selected(self, event=None):
        """模板选择事件"""
        pass

    def use_template(self):
        """使用模板"""
        template_name = self.template_var.get()
        if template_name and template_name in COMBINATION_TEMPLATES:
            self.selected_keys = COMBINATION_TEMPLATES[template_name].copy()
            self.update_selected_display()

    def add_key(self, key: str):
        """添加按键"""
        if key not in self.selected_keys:
            self.selected_keys.append(key)
            self.update_selected_display()

    def clear_keys(self):
        """清除按键"""
        self.selected_keys.clear()
        self.update_selected_display()

    def update_selected_display(self):
        """更新已选择按键显示"""
        display_text = ' + '.join(self.selected_keys) if self.selected_keys else '(无)'
        self.selected_var.set(display_text)

    def ok_clicked(self):
        """确定按钮点击"""
        if self.selected_keys:
            self.result = self.selected_keys.copy()
        self.dialog.destroy()

    def cancel_clicked(self):
        """取消按钮点击"""
        self.result = None
        self.dialog.destroy()
