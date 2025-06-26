"""
配置管理模块
负责配置的保存、加载、验证和管理
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = config_dir
        self.ensure_config_dir()
    
    def ensure_config_dir(self):
        """确保配置目录存在"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def save_config(self, config: Dict[str, Any], name: str) -> bool:
        """
        保存配置到文件
        
        Args:
            config: 配置字典
            name: 配置名称
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # 添加元数据
            config_with_meta = {
                'name': name,
                'created_at': datetime.now().isoformat(),
                'version': '1.0',
                **config
            }
            
            filename = f"{name}.json"
            filepath = os.path.join(self.config_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config_with_meta, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def load_config(self, name: str) -> Optional[Dict[str, Any]]:
        """
        从文件加载配置
        
        Args:
            name: 配置名称
            
        Returns:
            Dict[str, Any]: 配置字典，失败返回None
        """
        try:
            filename = f"{name}.json"
            filepath = os.path.join(self.config_dir, filename)
            
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 验证配置
            if self.validate_config(config):
                return config
            else:
                print(f"配置文件 {name} 格式无效")
                return None
                
        except Exception as e:
            print(f"加载配置失败: {e}")
            return None
    
    def list_configs(self) -> List[str]:
        """
        列出所有可用的配置
        
        Returns:
            List[str]: 配置名称列表
        """
        try:
            configs = []
            for filename in os.listdir(self.config_dir):
                if filename.endswith('.json'):
                    config_name = filename[:-5]  # 移除.json后缀
                    configs.append(config_name)
            return sorted(configs)
        except Exception as e:
            print(f"列出配置失败: {e}")
            return []
    
    def delete_config(self, name: str) -> bool:
        """
        删除配置文件
        
        Args:
            name: 配置名称
            
        Returns:
            bool: 删除是否成功
        """
        try:
            filename = f"{name}.json"
            filepath = os.path.join(self.config_dir, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            else:
                return False
        except Exception as e:
            print(f"删除配置失败: {e}")
            return False
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        验证配置格式是否正确
        
        Args:
            config: 配置字典
            
        Returns:
            bool: 配置是否有效
        """
        try:
            # 检查必需字段
            if 'sequences' not in config:
                return False
            
            sequences = config['sequences']
            if not isinstance(sequences, list):
                return False
            
            # 验证每个序列
            for sequence in sequences:
                if not isinstance(sequence, dict):
                    return False
                
                if 'keys' not in sequence:
                    return False
                
                keys = sequence['keys']
                if not isinstance(keys, list):
                    return False
                
                # 验证每个按键配置
                for key_config in keys:
                    if not isinstance(key_config, dict):
                        return False
                    
                    if 'type' not in key_config:
                        return False
                    
                    key_type = key_config['type']
                    if key_type not in ['single', 'combination', 'text']:
                        return False
                    
                    # 根据类型验证特定字段
                    if key_type == 'single' and 'key' not in key_config:
                        return False
                    elif key_type == 'combination' and 'keys' not in key_config:
                        return False
                    elif key_type == 'text' and 'text' not in key_config:
                        return False
            
            return True
            
        except Exception as e:
            print(f"配置验证失败: {e}")
            return False
    
    def create_default_config(self) -> Dict[str, Any]:
        """
        创建默认配置
        
        Returns:
            Dict[str, Any]: 默认配置字典
        """
        return {
            'name': '默认配置',
            'description': '这是一个示例配置',
            'repeat_count': 1,
            'repeat_interval': 1.0,
            'sequences': [
                {
                    'name': '示例序列',
                    'keys': [
                        {
                            'type': 'single',
                            'key': 'space'
                        }
                    ],
                    'count': 1,
                    'interval': 0.5,
                    'random_interval': False,
                    'random_order': False
                }
            ]
        }
    
    def export_config(self, name: str, export_path: str) -> bool:
        """
        导出配置到指定路径
        
        Args:
            name: 配置名称
            export_path: 导出路径
            
        Returns:
            bool: 导出是否成功
        """
        try:
            config = self.load_config(name)
            if config is None:
                return False
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"导出配置失败: {e}")
            return False
    
    def import_config(self, import_path: str, name: str) -> bool:
        """
        从指定路径导入配置
        
        Args:
            import_path: 导入路径
            name: 配置名称
            
        Returns:
            bool: 导入是否成功
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if self.validate_config(config):
                return self.save_config(config, name)
            else:
                print("导入的配置格式无效")
                return False
                
        except Exception as e:
            print(f"导入配置失败: {e}")
            return False
