"""
JSON配置文件管理 - 处理config.json文件
"""
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from ..exceptions import ConfigurationError


class JsonConfig:
    """JSON配置文件管理器"""
    
    def __init__(self, json_file: Path):
        """
        初始化JSON配置管理器
        
        Args:
            json_file: JSON配置文件路径
        """
        self.json_file = json_file
        self.data = {}
        self.logger = logging.getLogger(__name__)
    
    def load(self) -> bool:
        """
        加载JSON配置文件
        
        Returns:
            是否成功加载
        """
        try:
            if not self.json_file.exists():
                self.logger.warning(f"JSON配置文件不存在: {self.json_file}")
                return False
            
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            self.logger.info(f"JSON配置文件已加载: {self.json_file}")
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON配置文件格式错误: {e}")
            raise ConfigurationError(f"JSON配置文件格式错误: {e}")
        except Exception as e:
            self.logger.error(f"加载JSON配置文件失败: {e}")
            raise ConfigurationError(f"加载JSON配置文件失败: {e}")
    
    def save(self) -> bool:
        """
        保存JSON配置文件
        
        Returns:
            是否成功保存
        """
        try:
            # 确保目录存在
            self.json_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 更新修改时间
            if isinstance(self.data, dict):
                self.data['updated_at'] = datetime.now().isoformat()
            
            # 保存文件
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"JSON配置文件已保存: {self.json_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存JSON配置文件失败: {e}")
            raise ConfigurationError(f"保存JSON配置文件失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点分表示法 (如 'monitoring.default_interval')
            default: 默认值
            
        Returns:
            配置值
        """
        try:
            if '.' in key:
                # 使用点分表示法访问嵌套配置
                keys = key.split('.')
                value = self.data
                
                for k in keys:
                    if isinstance(value, dict) and k in value:
                        value = value[k]
                    else:
                        return default
                
                return value
            else:
                # 直接访问
                if isinstance(self.data, dict):
                    return self.data.get(key, default)
                else:
                    return default
                    
        except Exception as e:
            self.logger.error(f"获取配置值失败: {key}, 错误: {e}")
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """
        设置配置值
        
        Args:
            key: 配置键，支持点分表示法
            value: 配置值
            
        Returns:
            是否成功
        """
        try:
            if '.' in key:
                # 使用点分表示法设置嵌套配置
                keys = key.split('.')
                
                # 确保data是字典
                if not isinstance(self.data, dict):
                    self.data = {}
                
                # 导航到父级
                current = self.data
                for k in keys[:-1]:
                    if k not in current:
                        current[k] = {}
                    current = current[k]
                
                # 设置值
                current[keys[-1]] = value
            else:
                # 直接设置
                if not isinstance(self.data, dict):
                    self.data = {}
                self.data[key] = value
            
            self.logger.debug(f"JSON配置已更新: {key} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"设置配置值失败: {key} = {value}, 错误: {e}")
            return False
    
    def remove(self, key: str) -> bool:
        """
        删除配置值
        
        Args:
            key: 配置键，支持点分表示法
            
        Returns:
            是否成功
        """
        try:
            if '.' in key:
                # 使用点分表示法删除嵌套配置
                keys = key.split('.')
                
                if not isinstance(self.data, dict):
                    return False
                
                # 导航到父级
                current = self.data
                for k in keys[:-1]:
                    if k not in current:
                        return False
                    current = current[k]
                
                # 删除值
                if keys[-1] in current:
                    del current[keys[-1]]
                    return True
                else:
                    return False
            else:
                # 直接删除
                if isinstance(self.data, dict) and key in self.data:
                    del self.data[key]
                    return True
                else:
                    return False
                    
        except Exception as e:
            self.logger.error(f"删除配置值失败: {key}, 错误: {e}")
            return False
    
    def get_all(self) -> Dict[str, Any]:
        """
        获取所有配置
        
        Returns:
            完整配置数据
        """
        return self.data.copy() if isinstance(self.data, dict) else {}
    
    def update(self, updates: Dict[str, Any]) -> bool:
        """
        批量更新配置
        
        Args:
            updates: 更新字典
            
        Returns:
            是否成功
        """
        try:
            if not isinstance(self.data, dict):
                self.data = {}
            
            self.data.update(updates)
            self.logger.info(f"JSON配置已批量更新: {list(updates.keys())}")
            return True
            
        except Exception as e:
            self.logger.error(f"批量更新配置失败: {e}")
            return False
    
    def merge(self, other_data: Dict[str, Any], overwrite: bool = True) -> bool:
        """
        合并配置数据
        
        Args:
            other_data: 要合并的数据
            overwrite: 是否覆盖现有值
            
        Returns:
            是否成功
        """
        try:
            if not isinstance(self.data, dict):
                self.data = {}
            
            if overwrite:
                # 完全覆盖
                self.data.update(other_data)
            else:
                # 只添加不存在的键
                for key, value in other_data.items():
                    if key not in self.data:
                        self.data[key] = value
            
            self.logger.info("JSON配置已合并")
            return True
            
        except Exception as e:
            self.logger.error(f"合并配置失败: {e}")
            return False
    
    def validate(self) -> bool:
        """
        验证配置数据
        
        Returns:
            是否有效
        """
        try:
            if not isinstance(self.data, dict):
                self.logger.error("配置数据必须为字典类型")
                return False
            
            # 检查必需字段
            required_fields = ['version', 'monitoring', 'detection', 'notification', 'tasks', 'storage']
            for field in required_fields:
                if field not in self.data:
                    self.logger.error(f"缺少必需字段: {field}")
                    return False
            
            # 验证版本号
            version = self.data.get('version')
            if not isinstance(version, str) or not version.strip():
                self.logger.error("版本号格式无效")
                return False
            
            # 验证任务列表
            tasks = self.data.get('tasks', [])
            if not isinstance(tasks, list):
                self.logger.error("任务列表必须为数组类型")
                return False
            
            # 验证监控配置
            monitoring = self.data.get('monitoring', {})
            if not isinstance(monitoring, dict):
                self.logger.error("监控配置必须为字典类型")
                return False
            
            # 验证检测配置
            detection = self.data.get('detection', {})
            if not isinstance(detection, dict):
                self.logger.error("检测配置必须为字典类型")
                return False
            
            # 验证通知配置
            notification = self.data.get('notification', {})
            if not isinstance(notification, dict):
                self.logger.error("通知配置必须为字典类型")
                return False
            
            # 验证存储配置
            storage = self.data.get('storage', {})
            if not isinstance(storage, dict):
                self.logger.error("存储配置必须为字典类型")
                return False
            
            self.logger.info("JSON配置验证通过")
            return True
            
        except Exception as e:
            self.logger.error(f"配置验证失败: {e}")
            return False
    
    def backup(self, backup_file: Optional[Path] = None) -> bool:
        """
        备份配置文件
        
        Args:
            backup_file: 备份文件路径
            
        Returns:
            是否成功
        """
        try:
            if not backup_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = self.json_file.parent / f"config_backup_{timestamp}.json"
            
            # 确保备份目录存在
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 复制文件
            with open(self.json_file, 'r', encoding='utf-8') as src:
                content = src.read()
            
            with open(backup_file, 'w', encoding='utf-8') as dst:
                dst.write(content)
            
            self.logger.info(f"JSON配置已备份到: {backup_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"备份JSON配置失败: {e}")
            return False
    
    def restore(self, backup_file: Path) -> bool:
        """
        从备份文件恢复配置
        
        Args:
            backup_file: 备份文件路径
            
        Returns:
            是否成功
        """
        try:
            if not backup_file.exists():
                self.logger.error(f"备份文件不存在: {backup_file}")
                return False
            
            # 验证备份文件格式
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            if not isinstance(backup_data, dict):
                self.logger.error("备份文件格式无效")
                return False
            
            # 备份当前配置
            self.backup()
            
            # 恢复配置
            self.data = backup_data
            self.save()
            
            self.logger.info(f"JSON配置已从备份恢复: {backup_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"恢复JSON配置失败: {e}")
            return False
    
    def export_config(self, export_file: Path, include_sensitive: bool = True) -> bool:
        """
        导出配置（用于分享或迁移）
        
        Args:
            export_file: 导出文件路径
            include_sensitive: 是否包含敏感信息
            
        Returns:
            是否成功
        """
        try:
            export_data = self.data.copy()
            
            if not include_sensitive:
                # 移除敏感信息
                self._remove_sensitive_data(export_data)
            
            # 确保导出目录存在
            export_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存导出文件
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"配置已导出到: {export_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"导出配置失败: {e}")
            return False
    
    def import_config(self, import_file: Path, merge: bool = True) -> bool:
        """
        导入配置
        
        Args:
            import_file: 导入文件路径
            merge: 是否合并到现有配置
            
        Returns:
            是否成功
        """
        try:
            if not import_file.exists():
                self.logger.error(f"导入文件不存在: {import_file}")
                return False
            
            # 读取导入文件
            with open(import_file, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if not isinstance(import_data, dict):
                self.logger.error("导入文件格式无效")
                return False
            
            if merge:
                # 合并配置
                self.merge(import_data, overwrite=True)
            else:
                # 完全替换
                self.data = import_data
            
            self.save()
            
            self.logger.info(f"配置已从文件导入: {import_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"导入配置失败: {e}")
            return False
    
    def _remove_sensitive_data(self, data: Dict[str, Any]):
        """移除敏感数据"""
        sensitive_keys = ['token', 'password', 'secret', 'key', 'webhook']
        
        def remove_from_dict(d):
            keys_to_remove = []
            for key, value in d.items():
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    keys_to_remove.append(key)
                elif isinstance(value, dict):
                    remove_from_dict(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            remove_from_dict(item)
            
            for key in keys_to_remove:
                d[key] = '[REDACTED]'
        
        remove_from_dict(data)
    
    def get_size(self) -> int:
        """
        获取配置文件大小
        
        Returns:
            文件大小（字节）
        """
        try:
            return self.json_file.stat().st_size if self.json_file.exists() else 0
        except Exception:
            return 0
    
    def get_version(self) -> Optional[str]:
        """
        获取配置版本
        
        Returns:
            版本号
        """
        return self.get('version')
    
    def is_compatible(self, target_version: str) -> bool:
        """
        检查配置版本兼容性
        
        Args:
            target_version: 目标版本
            
        Returns:
            是否兼容
        """
        current_version = self.get_version()
        if not current_version:
            return False
        
        # 简单的版本兼容性检查
        try:
            current_parts = current_version.split('.')
            target_parts = target_version.split('.')
            
            # 主要版本号必须相同
            return current_parts[0] == target_parts[0]
            
        except Exception:
            return False