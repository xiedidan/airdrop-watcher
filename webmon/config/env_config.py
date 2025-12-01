"""
环境变量配置管理 - 处理.env文件
"""
import os
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dotenv import load_dotenv, set_key
from ..exceptions import ConfigurationError


class EnvConfig:
    """环境变量配置管理器"""
    
    # 环境变量配置定义
    ENV_CONFIGS = {
        # 推送平台配置
        'PUSHPLUS_TOKEN': {
            'type': str,
            'required': False,
            'description': 'PushPlus推送平台令牌',
            'default': None
        },
        'TELEGRAM_BOT_TOKEN': {
            'type': str,
            'required': False,
            'description': 'Telegram Bot令牌',
            'default': None
        },
        'TELEGRAM_CHAT_ID': {
            'type': str,
            'required': False,
            'description': 'Telegram聊天ID',
            'default': None
        },
        'DISCORD_WEBHOOK_URL': {
            'type': str,
            'required': False,
            'description': 'Discord Webhook URL',
            'default': None
        },
        'FEISHU_WEBHOOK_URL': {
            'type': str,
            'required': False,
            'description': '飞书Webhook URL',
            'default': None
        },
        
        # 监控配置
        'DEFAULT_INTERVAL': {
            'type': int,
            'required': False,
            'description': '默认检测间隔（秒）',
            'default': 300
        },
        'DEFAULT_TIMEOUT': {
            'type': int,
            'required': False,
            'description': '默认超时时间（毫秒）',
            'default': 30000
        },
        'MAX_RETRIES': {
            'type': int,
            'required': False,
            'description': '最大重试次数',
            'default': 3
        },
        'BROWSER_HEADLESS': {
            'type': bool,
            'required': False,
            'description': '浏览器无头模式',
            'default': True
        },
        
        # 检测配置
        'SIMILARITY_THRESHOLD': {
            'type': float,
            'required': False,
            'description': '相似度阈值',
            'default': 0.85
        },
        'ENABLE_SMART_DETECTION': {
            'type': bool,
            'required': False,
            'description': '启用智能检测',
            'default': True
        },
        'MIN_CHANGE_LENGTH': {
            'type': int,
            'required': False,
            'description': '最小变化长度',
            'default': 10
        },
        
        # 日志配置
        'LOG_LEVEL': {
            'type': str,
            'required': False,
            'description': '日志级别',
            'default': 'INFO',
            'choices': ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        },
        'LOG_FILE': {
            'type': str,
            'required': False,
            'description': '日志文件路径',
            'default': 'logs/webmon.log'
        },
        'LOG_MAX_SIZE': {
            'type': str,
            'required': False,
            'description': '日志文件最大大小',
            'default': '10MB'
        },
        'LOG_BACKUP_COUNT': {
            'type': int,
            'required': False,
            'description': '日志备份数量',
            'default': 5
        },
        
        # 高级配置
        'CONCURRENT_TASKS': {
            'type': int,
            'required': False,
            'description': '并发任务数',
            'default': 5
        },
        'RATE_LIMIT_PER_MINUTE': {
            'type': int,
            'required': False,
            'description': '每分钟请求限制',
            'default': 30
        },
        'PROXY_URL': {
            'type': str,
            'required': False,
            'description': '代理服务器URL',
            'default': None
        },
        'CUSTOM_USER_AGENT': {
            'type': str,
            'required': False,
            'description': '自定义User-Agent',
            'default': None
        }
    }
    
    def __init__(self, env_file: Optional[Path] = None):
        """
        初始化环境变量配置管理器
        
        Args:
            env_file: .env文件路径
        """
        self.env_file = env_file or Path.cwd() / '.env'
        self.data = {}
        self.logger = logging.getLogger(__name__)
    
    def load(self) -> bool:
        """
        加载.env文件
        
        Returns:
            是否成功加载
        """
        try:
            if self.env_file.exists():
                # 使用load_dotenv加载环境变量
                load_dotenv(self.env_file)
                self.logger.info(f"环境变量文件已加载: {self.env_file}")
            
            # 从环境变量中读取配置
            self._load_from_environment()
            return True
            
        except Exception as e:
            self.logger.error(f"加载环境变量文件失败: {e}")
            return False
    
    def _load_from_environment(self):
        """从环境变量加载配置"""
        for key, config in self.ENV_CONFIGS.items():
            # 从环境变量获取值
            value = os.getenv(key)
            
            if value is not None:
                # 类型转换
                try:
                    value = self._convert_type(value, config['type'])
                except ValueError as e:
                    self.logger.warning(f"环境变量 {key} 类型转换失败: {e}, 使用默认值")
                    value = config['default']
            else:
                # 使用默认值
                value = config['default']
            
            self.data[key] = value
            
            # 记录加载的配置（屏蔽敏感信息）
            if self._is_sensitive_key(key):
                self.logger.debug(f"环境变量已加载: {key} = {'*' * 8}")
            else:
                self.logger.debug(f"环境变量已加载: {key} = {value}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取环境变量值
        
        Args:
            key: 环境变量名
            default: 默认值
            
        Returns:
            环境变量值
        """
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """
        设置环境变量值
        
        Args:
            key: 环境变量名
            value: 值
            
        Returns:
            是否成功
        """
        try:
            # 验证键名
            if key not in self.ENV_CONFIGS:
                self.logger.warning(f"未知的环境变量: {key}")
                return False
            
            # 验证值
            config = self.ENV_CONFIGS[key]
            if not self._validate_value(key, value):
                return False
            
            # 类型转换
            value = self._convert_type(str(value), config['type'])
            
            # 更新内存中的值
            self.data[key] = value
            
            # 更新环境变量
            os.environ[key] = str(value)
            
            # 更新.env文件
            if self.env_file.exists():
                set_key(self.env_file, key, str(value))
            else:
                # 创建新的.env文件
                self._create_env_file()
                set_key(self.env_file, key, str(value))
            
            self.logger.info(f"环境变量已更新: {key}")
            return True
            
        except Exception as e:
            self.logger.error(f"设置环境变量失败: {key} = {value}, 错误: {e}")
            return False
    
    def remove(self, key: str) -> bool:
        """
        删除环境变量
        
        Args:
            key: 环境变量名
            
        Returns:
            是否成功
        """
        try:
            if key in self.data:
                del self.data[key]
            
            if key in os.environ:
                del os.environ[key]
            
            # 从.env文件中删除
            if self.env_file.exists():
                self._remove_from_env_file(key)
            
            self.logger.info(f"环境变量已删除: {key}")
            return True
            
        except Exception as e:
            self.logger.error(f"删除环境变量失败: {key}, 错误: {e}")
            return False
    
    def list_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        列出所有配置项及其定义
        
        Returns:
            配置定义字典
        """
        result = {}
        for key, config in self.ENV_CONFIGS.items():
            result[key] = {
                'value': self.get(key),
                'description': config['description'],
                'required': config['required'],
                'type': config['type'].__name__,
                'default': config['default']
            }
        return result
    
    def get_descriptions(self) -> Dict[str, str]:
        """
        获取所有配置项的描述
        
        Returns:
            配置描述字典
        """
        return {key: config['description'] for key, config in self.ENV_CONFIGS.items()}
    
    def validate_all(self) -> Dict[str, bool]:
        """
        验证所有配置项
        
        Returns:
            验证结果字典
        """
        results = {}
        for key in self.ENV_CONFIGS.keys():
            results[key] = self._validate_value(key, self.get(key))
        return results
    
    def _convert_type(self, value: str, target_type: type) -> Any:
        """
        类型转换
        
        Args:
            value: 字符串值
            target_type: 目标类型
            
        Returns:
            转换后的值
        """
        if target_type == bool:
            return value.lower() in ('true', '1', 'yes', 'on', 'enabled')
        elif target_type == int:
            return int(value)
        elif target_type == float:
            return float(value)
        elif target_type == str:
            return str(value)
        else:
            raise ValueError(f"不支持的目标类型: {target_type}")
    
    def _validate_value(self, key: str, value: Any) -> bool:
        """
        验证配置值
        
        Args:
            key: 配置键
            value: 配置值
            
        Returns:
            是否有效
        """
        if key not in self.ENV_CONFIGS:
            return False
        
        config = self.ENV_CONFIGS[key]
        
        # 类型验证
        if not isinstance(value, config['type']):
            try:
                value = self._convert_type(str(value), config['type'])
            except ValueError:
                self.logger.error(f"配置 {key} 类型错误: 期望 {config['type'].__name__}, 实际 {type(value).__name__}")
                return False
        
        # 特定验证
        if key == 'LOG_LEVEL' and value not in config.get('choices', []):
            self.logger.error(f"配置 {key} 值无效: {value}, 可选值: {config.get('choices', [])}")
            return False
        
        if 'DEFAULT_INTERVAL' in key and value < 60:
            self.logger.warning(f"配置 {key} 值过小: {value} 秒，建议至少 60 秒")
        
        if 'DEFAULT_TIMEOUT' in key and value < 5000:
            self.logger.warning(f"配置 {key} 值过小: {value} 毫秒，建议至少 5000 毫秒")
        
        return True
    
    def _is_sensitive_key(self, key: str) -> bool:
        """
        判断是否为敏感配置键
        
        Args:
            key: 配置键
            
        Returns:
            是否为敏感信息
        """
        sensitive_patterns = ['TOKEN', 'PASSWORD', 'SECRET', 'KEY', 'WEBHOOK']
        return any(pattern in key.upper() for pattern in sensitive_patterns)
    
    def _create_env_file(self):
        """创建.env文件"""
        try:
            self.env_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 创建.env文件并写入注释
            content = ["# ==============================================", 
                      "# WebMon - 网页监控工具环境变量配置",
                      "# ==============================================",
                      ""]
            
            # 按类别分组
            categories = {
                '推送平台配置': ['PUSHPLUS_TOKEN', 'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID', 
                           'DISCORD_WEBHOOK_URL', 'FEISHU_WEBHOOK_URL'],
                '监控配置': ['DEFAULT_INTERVAL', 'DEFAULT_TIMEOUT', 'MAX_RETRIES', 'BROWSER_HEADLESS'],
                '检测配置': ['SIMILARITY_THRESHOLD', 'ENABLE_SMART_DETECTION', 'MIN_CHANGE_LENGTH'],
                '日志配置': ['LOG_LEVEL', 'LOG_FILE', 'LOG_MAX_SIZE', 'LOG_BACKUP_COUNT'],
                '高级配置': ['CONCURRENT_TASKS', 'RATE_LIMIT_PER_MINUTE', 'PROXY_URL', 'CUSTOM_USER_AGENT']
            }
            
            for category, keys in categories.items():
                content.append(f"# {category}")
                for key in keys:
                    config = self.ENV_CONFIGS[key]
                    description = config['description']
                    default_value = config['default']
                    
                    if default_value is not None:
                        content.append(f"# {description}")
                        content.append(f"{key}={default_value}")
                    else:
                        content.append(f"# {description} (可选)")
                        content.append(f"# {key}=")
                    content.append("")
            
            self.env_file.write_text('\n'.join(content))
            self.logger.info(f"环境变量文件已创建: {self.env_file}")
            
        except Exception as e:
            self.logger.error(f"创建.env文件失败: {e}")
            raise ConfigurationError(f"创建.env文件失败: {e}")
    
    def _remove_from_env_file(self, key: str):
        """从.env文件中删除配置"""
        try:
            if not self.env_file.exists():
                return
            
            lines = self.env_file.read_text().splitlines()
            new_lines = []
            skip_next = False
            
            for i, line in enumerate(lines):
                if skip_next:
                    skip_next = False
                    continue
                
                # 检查当前行是否包含要删除的键
                if line.strip().startswith(f"{key}="):
                    # 跳过当前行和前面的注释行（如果有）
                    if i > 0 and new_lines and new_lines[-1].startswith('#'):
                        new_lines.pop()
                    skip_next = True
                    continue
                
                new_lines.append(line)
            
            self.env_file.write_text('\n'.join(new_lines))
            
        except Exception as e:
            self.logger.error(f"从.env文件删除配置失败: {key}, 错误: {e}")