"""
消息模板引擎

提供灵活的消息模板系统，支持变量替换、条件判断、循环等高级功能。
"""
import re
import json
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from string import Template
from abc import ABC, abstractmethod

from ..exceptions import NotificationError


class TemplateVariable:
    """模板变量"""
    
    def __init__(self, name: str, value: Any, description: str = ""):
        """
        初始化模板变量
        
        Args:
            name: 变量名
            value: 变量值
            description: 变量描述
        """
        self.name = name
        self.value = value
        self.description = description
    
    def get_value(self, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        获取变量值
        
        Args:
            context: 上下文环境
            
        Returns:
            变量值
        """
        if callable(self.value):
            return self.value(context)
        return self.value


class BaseTemplateEngine(ABC):
    """模板引擎基类"""
    
    def __init__(self, engine_name: str):
        """
        初始化模板引擎
        
        Args:
            engine_name: 引擎名称
        """
        self.engine_name = engine_name
        self.logger = logging.getLogger(__name__)
    
    @abstractmethod
    def render(self, template: str, context: Dict[str, Any]) -> str:
        """
        渲染模板
        
        Args:
            template: 模板字符串
            context: 上下文数据
            
        Returns:
            渲染结果
        """
        pass
    
    @abstractmethod
    def validate_template(self, template: str) -> bool:
        """
        验证模板语法
        
        Args:
            template: 模板字符串
            
        Returns:
            是否有效
        """
        pass


class SimpleTemplateEngine(BaseTemplateEngine):
    """简单模板引擎（基于Python string.Template）"""
    
    def __init__(self):
        """初始化简单模板引擎"""
        super().__init__("simple")
    
    def render(self, template: str, context: Dict[str, Any]) -> str:
        """
        渲染模板
        
        Args:
            template: 模板字符串
            context: 上下文数据
            
        Returns:
            渲染结果
            
        Raises:
            NotificationError: 渲染失败
        """
        try:
            # 创建模板对象
            template_obj = Template(template)
            
            # 渲染模板
            result = template_obj.safe_substitute(context)
            
            # 检查是否有未替换的变量
            if "$" in result:
                self.logger.warning(f"模板中存在未替换的变量: {template}")
            
            return result
            
        except Exception as e:
            raise NotificationError(f"模板渲染失败: {e}", template_engine=self.engine_name)
    
    def validate_template(self, template: str) -> bool:
        """
        验证模板语法
        
        Args:
            template: 模板字符串
            
        Returns:
            是否有效
        """
        try:
            # 尝试创建模板对象
            Template(template)
            return True
        except Exception:
            return False


class AdvancedTemplateEngine(BaseTemplateEngine):
    """高级模板引擎（支持条件和循环）"""
    
    def __init__(self):
        """初始化高级模板引擎"""
        super().__init__("advanced")
        
        # 定义模板语法 - 使用更简单的语法
        self.variable_pattern = re.compile(r'\$\{([^}]+)\}')
        self.condition_pattern = re.compile(r'\$\{if\s*\(([^}]+)\)\}(.*?)\$\{endif\}', re.DOTALL)
        self.loop_pattern = re.compile(r'\$\{for\s*\(([^}]+)\)\s+in\s+([^}]+)\}(.*?)\$\{endfor\}', re.DOTALL)
    
    def render(self, template: str, context: Dict[str, Any]) -> str:
        """
        渲染模板
        
        Args:
            template: 模板字符串
            context: 上下文数据
            
        Returns:
            渲染结果
            
        Raises:
            NotificationError: 渲染失败
        """
        try:
            result = template
            
            # 处理循环
            result = self._process_loops(result, context)
            
            # 处理条件
            result = self._process_conditions(result, context)
            
            # 处理变量 - 包括条件语句中的变量
            result = self._process_variables(result, context)
            
            return result
            
        except Exception as e:
            raise NotificationError(f"高级模板渲染失败: {e}", template_engine=self.engine_name)
    
    def _process_variables(self, template: str, context: Dict[str, Any]) -> str:
        """
        处理变量替换
        
        Args:
            template: 模板字符串
            context: 上下文数据
            
        Returns:
            处理后的字符串
        """
        def replace_variable(match):
            var_name = match.group(1).strip()
            
            # 支持嵌套属性访问，如 ${user.name}
            value = self._get_nested_value(context, var_name)
            
            if value is None:
                self.logger.warning(f"模板变量未找到: {var_name}")
                return match.group(0)  # 保持原样
            
            return str(value)
        
        return self.variable_pattern.sub(replace_variable, template)
    
    def _process_conditions(self, template: str, context: Dict[str, Any]) -> str:
        """
        处理条件判断
        
        Args:
            template: 模板字符串
            context: 上下文数据
            
        Returns:
            处理后的字符串
        """
        def replace_condition(match):
            full_match = match.group(0)
            condition_expr = match.group(1).strip()
            content = match.group(2).strip()
            
            # 处理嵌套的条件表达式，如 ${has_similarity}
            if condition_expr.startswith('${') and condition_expr.endswith('}'):
                # 提取变量名
                var_name = condition_expr[2:-1].strip()
                condition_value = self._get_nested_value(context, var_name)
            else:
                # 直接评估表达式
                condition_value = self._evaluate_condition(condition_expr, context)
            
            # 评估条件
            if condition_value:
                return content
            else:
                return ""
        
        return self.condition_pattern.sub(replace_condition, template)
    
    def _process_loops(self, template: str, context: Dict[str, Any]) -> str:
        """
        处理循环
        
        Args:
            template: 模板字符串
            context: 上下文数据
            
        Returns:
            处理后的字符串
        """
        def replace_loop(match):
            item_var = match.group(1).strip()
            list_var = match.group(2).strip()
            content = match.group(3).strip()
            
            # 获取列表数据（移除括号）
            list_var = list_var.strip("()")
            items = self._get_nested_value(context, list_var)
            
            if not isinstance(items, list):
                self.logger.warning(f"循环变量不是列表: {list_var}")
                return ""
            
            # 生成循环内容
            result_parts = []
            for item in items:
                # 创建临时上下文
                temp_context = context.copy()
                temp_context[item_var] = item
                
                # 渲染循环内容
                rendered_content = self._process_variables(content, temp_context)
                result_parts.append(rendered_content)
            
            return "".join(result_parts)
        
        return self.loop_pattern.sub(replace_loop, template)
    
    def _get_nested_value(self, context: Dict[str, Any], key: str) -> Any:
        """
        获取嵌套值
        
        Args:
            context: 上下文数据
            key: 键名（支持点号分隔）
            
        Returns:
            值
        """
        keys = key.split('.')
        value = context
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        
        return value
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """
        评估条件
        
        Args:
            condition: 条件表达式
            context: 上下文数据
            
        Returns:
            条件结果
        """
        try:
            # 简单的条件评估
            # 支持基本比较操作
            
            # 替换变量
            for key, value in context.items():
                if f"${{{key}}}" in condition:
                    condition = condition.replace(f"${{{key}}}", repr(value))
            
            # 评估条件
            return eval(condition, {"__builtins__": {}})
            
        except Exception as e:
            self.logger.warning(f"条件评估失败: {condition}, 错误: {e}")
            return False
    
    def validate_template(self, template: str) -> bool:
        """
        验证模板语法
        
        Args:
            template: 模板字符串
            
        Returns:
            是否有效
        """
        try:
            # 检查基本语法
            # 这里可以添加更复杂的验证逻辑
            
            # 检查括号匹配
            if template.count("#if(") != template.count("#endif"):
                return False
            
            if template.count("#for(") != template.count("#endfor"):
                return False
            
            return True
            
        except Exception:
            return False


class MessageTemplate:
    """消息模板类"""
    
    def __init__(self, template_id: str, name: str, template_content: str,
                 template_type: str = "simple", description: str = "",
                 variables: Optional[List[Dict[str, Any]]] = None):
        """
        初始化消息模板
        
        Args:
            template_id: 模板ID
            name: 模板名称
            template_content: 模板内容
            template_type: 模板类型（simple, advanced）
            description: 模板描述
            variables: 模板变量定义
        """
        self.template_id = template_id
        self.name = name
        self.template_content = template_content
        self.template_type = template_type
        self.description = description
        self.variables = variables or []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.use_count = 0
        
        # 选择模板引擎
        if template_type == "simple":
            self.engine = SimpleTemplateEngine()
        elif template_type == "advanced":
            self.engine = AdvancedTemplateEngine()
        else:
            raise ValueError(f"不支持的模板类型: {template_type}")
    
    def render(self, context: Dict[str, Any]) -> str:
        """
        渲染模板
        
        Args:
            context: 上下文数据
            
        Returns:
            渲染结果
        """
        try:
            result = self.engine.render(self.template_content, context)
            self.use_count += 1
            self.updated_at = datetime.now()
            return result
        except Exception as e:
            raise NotificationError(f"模板渲染失败: {e}", template_engine=self.template_type)
    
    def validate(self) -> bool:
        """
        验证模板
        
        Returns:
            是否有效
        """
        return self.engine.validate_template(self.template_content)
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取模板信息
        
        Returns:
            模板信息
        """
        return {
            "template_id": self.template_id,
            "name": self.name,
            "template_type": self.template_type,
            "description": self.description,
            "variables": self.variables,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "use_count": self.use_count,
            "is_valid": self.validate()
        }


class TemplateEngine:
    """模板引擎管理器"""
    
    def __init__(self):
        """初始化模板引擎"""
        self.templates: Dict[str, MessageTemplate] = {}
        self.engines = {
            "simple": SimpleTemplateEngine(),
            "advanced": AdvancedTemplateEngine()
        }
        self.logger = logging.getLogger(__name__)
        
        # 初始化内置模板
        self._initialize_builtin_templates()
    
    def _initialize_builtin_templates(self):
        """初始化内置模板"""
        try:
            # 网页变化通知模板
            change_template = MessageTemplate(
                template_id="webpage_change",
                name="网页变化通知",
                template_content="""
📍 网页变化检测 - ${task_name}
⏰ ${timestamp}
${ai_summary_info}

变化: ${change_summary}

相似度: ${similarity}%
链接: ${url}""",
                template_type="simple",
                description="用于网页内容变化检测的通知模板",
                variables=[
                    {"name": "task_name", "type": "string", "required": True},
                    {"name": "url", "type": "string", "required": False},
                    {"name": "change_summary", "type": "string", "required": True},
                    {"name": "similarity", "type": "number", "required": False},
                    {"name": "detection_time", "type": "string", "required": True},
                    {"name": "has_url", "type": "boolean", "required": False},
                    {"name": "ai_summary", "type": "string", "required": False},
                    {"name": "ai_summary_info", "type": "string", "required": False}
                ]
            )
            
            self.register_template(change_template)
            
            # 系统通知模板
            system_template = MessageTemplate(
                template_id="system_notification",
                name="系统通知",
                template_content="""🔔 系统通知

📋 标题: ${title}
📝 内容: ${content}
⏰ 时间: ${timestamp}
🔧 类型: ${type}

${details_info}""",
                template_type="simple",
                description="用于系统级通知的模板",
                variables=[
                    {"name": "title", "type": "string", "required": True},
                    {"name": "content", "type": "string", "required": True},
                    {"name": "timestamp", "type": "string", "required": True},
                    {"name": "type", "type": "string", "required": True},
                    {"name": "has_details", "type": "boolean", "required": False},
                    {"name": "details", "type": "string", "required": False}
                ]
            )
            
            self.register_template(system_template)
            
            # 错误通知模板
            error_template = MessageTemplate(
                template_id="error_notification",
                name="错误通知",
                template_content="""❌ 错误通知

🚨 错误类型: ${error_type}
📝 错误信息: ${error_message}
⏰ 发生时间: ${timestamp}
🔧 相关任务: ${task_name}

${solution_info}
${details_info}""",
                template_type="simple",
                description="用于错误通知的模板",
                variables=[
                    {"name": "error_type", "type": "string", "required": True},
                    {"name": "error_message", "type": "string", "required": True},
                    {"name": "timestamp", "type": "string", "required": True},
                    {"name": "task_name", "type": "string", "required": False},
                    {"name": "has_solution", "type": "boolean", "required": False},
                    {"name": "solution", "type": "string", "required": False},
                    {"name": "has_details", "type": "boolean", "required": False},
                    {"name": "details", "type": "string", "required": False}
                ]
            )
            
            self.register_template(error_template)
            
            self.logger.info("内置模板初始化完成")
            
        except Exception as e:
            self.logger.error(f"初始化内置模板失败: {e}")
    
    def register_template(self, template: MessageTemplate):
        """
        注册模板
        
        Args:
            template: 模板对象
        """
        self.templates[template.template_id] = template
        self.logger.info(f"模板已注册: {template.template_id} ({template.name})")
    
    def unregister_template(self, template_id: str):
        """
        注销模板
        
        Args:
            template_id: 模板ID
        """
        if template_id in self.templates:
            del self.templates[template_id]
            self.logger.info(f"模板已注销: {template_id}")
    
    def get_template(self, template_id: str) -> Optional[MessageTemplate]:
        """
        获取模板
        
        Args:
            template_id: 模板ID
            
        Returns:
            模板对象，不存在返回None
        """
        return self.templates.get(template_id)
    
    def render_template(self, template_id: str, context: Dict[str, Any]) -> str:
        """
        渲染指定模板
        
        Args:
            template_id: 模板ID
            context: 上下文数据
            
        Returns:
            渲染结果
        """
        template = self.get_template(template_id)
        if not template:
            raise NotificationError(f"模板不存在: {template_id}")
        
        return template.render(context)
    
    def render_with_engine(self, template_content: str, context: Dict[str, Any], 
                          engine_type: str = "simple") -> str:
        """
        使用指定引擎渲染模板
        
        Args:
            template_content: 模板内容
            context: 上下文数据
            engine_type: 引擎类型
            
        Returns:
            渲染结果
        """
        engine = self.engines.get(engine_type)
        if not engine:
            raise NotificationError(f"模板引擎不存在: {engine_type}")
        
        return engine.render(template_content, context)
    
    def validate_template(self, template_content: str, engine_type: str = "simple") -> bool:
        """
        验证模板
        
        Args:
            template_content: 模板内容
            engine_type: 引擎类型
            
        Returns:
            是否有效
        """
        engine = self.engines.get(engine_type)
        if not engine:
            return False
        
        return engine.validate_template(template_content)
    
    def create_change_notification_template(self, task_name: str, url: str,
                                          change_summary: str, similarity: Optional[float] = None,
                                          detection_time: Optional[float] = None,
                                          old_content: Optional[str] = None,
                                          new_content: Optional[str] = None,
                                          ai_summary: Optional[str] = None) -> str:
        """
        创建网页变化通知模板

        Args:
            task_name: 任务名称
            url: 网页URL
            change_summary: 变化摘要
            similarity: 相似度（可选）
            detection_time: 检测耗时（可选）
            old_content: 旧内容（可选）
            new_content: 新内容（可选）
            ai_summary: AI分析摘要（可选）

        Returns:
            渲染后的消息内容
        """
        try:
            # 预计算条件内容
            similarity_info = f"📊 相似度: {similarity:.1f}%\n" if similarity is not None else ""
            detection_time_info = f"⏱️ 检测耗时: {detection_time:.3f}秒\n" if detection_time is not None else ""
            url_info = f"\n🔗 查看详情: {url}" if url else ""

            # AI摘要
            ai_summary_info = ""
            if ai_summary:
                ai_summary_info = f"\n🤖 AI摘要:\n{ai_summary}"

            context = {
                "task_name": task_name,
                "url": url,
                "change_summary": change_summary,
                "similarity": similarity if similarity is not None else 0,
                "detection_time": detection_time if detection_time is not None else 0,
                "similarity_info": similarity_info,
                "detection_time_info": detection_time_info,
                "url_info": url_info,
                "ai_summary": ai_summary or "",
                "ai_summary_info": ai_summary_info,
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            return self.render_template("webpage_change", context)

        except Exception as e:
            self.logger.error(f"创建变化通知模板失败: {e}")
            # 返回备用格式
            return self._create_fallback_change_message(task_name, url, change_summary, similarity, detection_time, ai_summary)
    
    def _create_fallback_change_message(self, task_name: str, url: str,
                                      change_summary: str, similarity: Optional[float] = None,
                                      detection_time: Optional[float] = None,
                                      ai_summary: Optional[str] = None) -> str:
        """
        创建备用的变化通知消息

        Args:
            task_name: 任务名称
            url: 网页URL
            change_summary: 变化摘要
            similarity: 相似度（可选）
            detection_time: 检测耗时（可选）
            ai_summary: AI分析摘要（可选）

        Returns:
            消息内容
        """
        lines = [
            "🎯 网页变化检测通知",
            "",
            f"📍 任务: {task_name}",
            f"🔗 URL: {url}",
            f"📝 变化: {change_summary}",
            f"⏰ 检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ]

        if similarity is not None:
            lines.insert(4, f"📊 相似度: {similarity:.1f}%")

        if detection_time is not None:
            lines.append(f"⏱️ 检测耗时: {detection_time:.3f}秒")

        if ai_summary:
            lines.insert(3, "")
            lines.insert(4, "🤖 AI摘要:")
            lines.insert(5, ai_summary)

        return "\n".join(lines)
    
    def create_system_notification_template(self, title: str, content: str, 
                                          notification_type: str = "info",
                                          details: Optional[str] = None) -> str:
        """
        创建系统通知模板
        
        Args:
            title: 通知标题
            content: 通知内容
            notification_type: 通知类型
            details: 详细信息（可选）
            
        Returns:
            渲染后的消息内容
        """
        try:
            context = {
                "title": title,
                "content": content,
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "type": notification_type,
                "has_details": bool(details),
                "details": details or ""
            }
            
            return self.render_template("system_notification", context)
            
        except Exception as e:
            self.logger.error(f"创建系统通知模板失败: {e}")
            # 返回备用格式
            return self._create_fallback_system_message(title, content, notification_type, details)
    
    def _create_fallback_system_message(self, title: str, content: str, 
                                      notification_type: str, details: Optional[str] = None) -> str:
        """
        创建备用的系统通知消息
        
        Args:
            title: 通知标题
            content: 通知内容
            notification_type: 通知类型
            details: 详细信息（可选）
            
        Returns:
            消息内容
        """
        type_emoji = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅"
        }
        
        emoji = type_emoji.get(notification_type, "🔔")
        
        lines = [
            f"{emoji} 系统通知",
            "",
            f"📋 标题: {title}",
            f"📝 内容: {content}",
            f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"🔧 类型: {notification_type}"
        ]
        
        if details:
            lines.extend(["", "📊 详细信息:", details])
        
        return "\n".join(lines)
    
    def get_all_templates(self) -> List[Dict[str, Any]]:
        """
        获取所有模板信息
        
        Returns:
            模板信息列表
        """
        return [template.get_info() for template in self.templates.values()]
    
    def get_template_categories(self) -> Dict[str, List[str]]:
        """
        获取模板分类
        
        Returns:
            模板分类字典
        """
        categories = {
            "notification": [],
            "system": [],
            "error": [],
            "custom": []
        }
        
        for template_id, template in self.templates.items():
            if "notification" in template_id:
                categories["notification"].append(template_id)
            elif "system" in template_id:
                categories["system"].append(template_id)
            elif "error" in template_id:
                categories["error"].append(template_id)
            else:
                categories["custom"].append(template_id)
        
        return categories
    
    def get_summary(self) -> Dict[str, Any]:
        """
        获取模板引擎摘要
        
        Returns:
            摘要信息
        """
        total_templates = len(self.templates)
        template_types = {}
        
        for template in self.templates.values():
            template_type = template.template_type
            template_types[template_type] = template_types.get(template_type, 0) + 1
        
        total_uses = sum(template.use_count for template in self.templates.values())
        
        return {
            "total_templates": total_templates,
            "template_types": template_types,
            "total_uses": total_uses,
            "available_engines": list(self.engines.keys()),
            "categories": self.get_template_categories()
        }