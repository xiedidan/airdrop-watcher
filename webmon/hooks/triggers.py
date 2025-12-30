"""
Hook 触发点定义

定义 Hook 可以被触发的时机点。
"""

from enum import Enum


class HookTrigger(str, Enum):
    """Hook 触发点枚举"""

    # 检测到变化，通知发送前
    # 用途：数据预处理、内容过滤、条件判断
    ON_CHANGE_DETECTED = "on_change_detected"

    # AI分析完成，即将发送通知
    # 用途：修改通知内容、添加附加信息（注：当前设计为只读）
    ON_BEFORE_NOTIFY = "on_before_notify"

    # 通知发送完成后
    # 用途：后续操作、日志记录、触发其他系统
    ON_AFTER_NOTIFY = "on_after_notify"

    # 通知发送失败时
    # 用途：备用通知、告警升级、错误处理
    ON_NOTIFY_FAILED = "on_notify_failed"

    @classmethod
    def all_triggers(cls) -> list:
        """获取所有触发点列表"""
        return [trigger.value for trigger in cls]

    @classmethod
    def is_valid(cls, trigger: str) -> bool:
        """检查触发点是否有效"""
        return trigger in cls.all_triggers()
