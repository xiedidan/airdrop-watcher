"""
脚本路径验证器

验证 Hook 脚本路径的安全性，防止恶意脚本执行。
"""

import os
from pathlib import Path
from typing import Optional, List, Tuple
from dataclasses import dataclass

from webmon.utils.logger import get_logger


@dataclass
class ValidationResult:
    """验证结果"""
    valid: bool
    error_message: Optional[str] = None
    resolved_path: Optional[Path] = None


class ScriptValidator:
    """
    脚本路径验证器

    负责验证脚本路径的安全性，包括：
    - 白名单路径检查：只允许特定目录下的脚本
    - 黑名单路径检查：禁止系统目录和危险路径
    - 路径遍历检查：禁止 .. 等路径遍历符号
    - 脚本存在性检查
    - 执行权限检查
    """

    # 系统目录黑名单（禁止执行这些目录下的脚本）
    SYSTEM_DIRECTORIES_BLACKLIST = [
        '/etc',
        '/usr',
        '/bin',
        '/sbin',
        '/lib',
        '/lib64',
        '/boot',
        '/root',
        '/var',
        '/proc',
        '/sys',
        '/dev',
        '/run',
        '/snap',
        '/opt',
    ]

    # 危险路径模式
    DANGEROUS_PATTERNS = [
        '..',      # 路径遍历
        '~/',      # 展开到用户目录的 shell 语法
        '$(',      # 命令替换
        '`',       # 反引号命令替换
        ';',       # 命令分隔符
        '|',       # 管道
        '&',       # 后台执行
        '>',       # 重定向
        '<',       # 重定向
    ]

    def __init__(self, project_root: Optional[Path] = None):
        """
        初始化验证器

        Args:
            project_root: 项目根目录路径，默认为当前工作目录
        """
        self.logger = get_logger(__name__)
        self.project_root = (project_root or Path.cwd()).resolve()
        self.user_home = Path.home().resolve()

        # 构建白名单路径
        self._whitelist_dirs = self._build_whitelist()

    def _build_whitelist(self) -> List[Path]:
        """构建白名单目录列表"""
        whitelist = []

        # 项目根目录下的 scripts/ 和 hooks/ 目录
        whitelist.append(self.project_root / 'scripts')
        whitelist.append(self.project_root / 'hooks')

        # 用户主目录下的 scripts/ 和 webmon/hooks/ 目录
        whitelist.append(self.user_home / 'scripts')
        whitelist.append(self.user_home / 'webmon' / 'hooks')

        # 记录白名单路径
        self.logger.debug(f"脚本白名单目录: {[str(p) for p in whitelist]}")

        return whitelist

    def validate(self, script_path: str) -> ValidationResult:
        """
        验证脚本路径

        执行完整的路径验证，包括：
        1. 检查危险模式
        2. 解析并规范化路径
        3. 检查黑名单
        4. 检查白名单
        5. 检查脚本存在性
        6. 检查执行权限

        Args:
            script_path: 脚本路径（绝对路径或相对路径）

        Returns:
            ValidationResult: 验证结果
        """
        # 1. 检查危险模式
        danger_check = self._check_dangerous_patterns(script_path)
        if not danger_check[0]:
            return ValidationResult(
                valid=False,
                error_message=danger_check[1]
            )

        # 2. 解析并规范化路径
        try:
            resolved_path = self._resolve_path(script_path)
        except Exception as e:
            return ValidationResult(
                valid=False,
                error_message=f"路径解析失败: {e}"
            )

        # 3. 检查黑名单
        blacklist_check = self._check_blacklist(resolved_path)
        if not blacklist_check[0]:
            return ValidationResult(
                valid=False,
                error_message=blacklist_check[1]
            )

        # 4. 检查白名单
        whitelist_check = self._check_whitelist(resolved_path)
        if not whitelist_check[0]:
            return ValidationResult(
                valid=False,
                error_message=whitelist_check[1]
            )

        # 5. 检查脚本存在性
        if not resolved_path.exists():
            return ValidationResult(
                valid=False,
                error_message=f"脚本不存在: {resolved_path}"
            )

        if not resolved_path.is_file():
            return ValidationResult(
                valid=False,
                error_message=f"路径不是文件: {resolved_path}"
            )

        # 6. 检查执行权限
        if not os.access(resolved_path, os.X_OK):
            return ValidationResult(
                valid=False,
                error_message=f"脚本没有执行权限: {resolved_path}"
            )

        # 验证通过
        self.logger.debug(f"脚本路径验证通过: {resolved_path}")
        return ValidationResult(
            valid=True,
            resolved_path=resolved_path
        )

    def _check_dangerous_patterns(self, path: str) -> Tuple[bool, Optional[str]]:
        """
        检查路径是否包含危险模式

        Args:
            path: 原始路径字符串

        Returns:
            (是否安全, 错误信息)
        """
        for pattern in self.DANGEROUS_PATTERNS:
            if pattern in path:
                return (
                    False,
                    f"路径包含危险模式 '{pattern}': {path}"
                )
        return (True, None)

    def _resolve_path(self, script_path: str) -> Path:
        """
        解析并规范化路径

        Args:
            script_path: 原始路径字符串

        Returns:
            规范化后的绝对路径
        """
        path = Path(script_path)

        # 如果是绝对路径，直接解析
        if path.is_absolute():
            return path.resolve()

        # 相对路径：相对于项目根目录
        return (self.project_root / path).resolve()

    def _check_blacklist(self, resolved_path: Path) -> Tuple[bool, Optional[str]]:
        """
        检查路径是否在黑名单中

        Args:
            resolved_path: 已解析的绝对路径

        Returns:
            (是否安全, 错误信息)
        """
        path_str = str(resolved_path)

        for blacklisted_dir in self.SYSTEM_DIRECTORIES_BLACKLIST:
            # 检查路径是否以黑名单目录开头
            if path_str.startswith(blacklisted_dir + '/') or path_str == blacklisted_dir:
                return (
                    False,
                    f"脚本位于系统目录（禁止）: {blacklisted_dir}"
                )

        return (True, None)

    def _check_whitelist(self, resolved_path: Path) -> Tuple[bool, Optional[str]]:
        """
        检查路径是否在白名单中

        Args:
            resolved_path: 已解析的绝对路径

        Returns:
            (是否合法, 错误信息)
        """
        # 检查路径是否位于任一白名单目录下
        for whitelist_dir in self._whitelist_dirs:
            try:
                # 检查 resolved_path 是否是 whitelist_dir 的子路径
                resolved_path.relative_to(whitelist_dir)
                return (True, None)
            except ValueError:
                # 不是该目录的子路径，继续检查下一个
                continue

        # 不在任何白名单目录中
        whitelist_str = ', '.join([str(p) for p in self._whitelist_dirs])
        return (
            False,
            f"脚本路径不在白名单目录中。允许的目录: {whitelist_str}"
        )

    def validate_path_only(self, script_path: str) -> ValidationResult:
        """
        仅验证路径安全性（不检查文件存在性和权限）

        用于配置验证场景，脚本可能尚未创建。

        Args:
            script_path: 脚本路径

        Returns:
            ValidationResult: 验证结果
        """
        # 1. 检查危险模式
        danger_check = self._check_dangerous_patterns(script_path)
        if not danger_check[0]:
            return ValidationResult(
                valid=False,
                error_message=danger_check[1]
            )

        # 2. 解析并规范化路径
        try:
            resolved_path = self._resolve_path(script_path)
        except Exception as e:
            return ValidationResult(
                valid=False,
                error_message=f"路径解析失败: {e}"
            )

        # 3. 检查黑名单
        blacklist_check = self._check_blacklist(resolved_path)
        if not blacklist_check[0]:
            return ValidationResult(
                valid=False,
                error_message=blacklist_check[1]
            )

        # 4. 检查白名单
        whitelist_check = self._check_whitelist(resolved_path)
        if not whitelist_check[0]:
            return ValidationResult(
                valid=False,
                error_message=whitelist_check[1]
            )

        # 路径验证通过
        return ValidationResult(
            valid=True,
            resolved_path=resolved_path
        )

    def add_whitelist_dir(self, directory: Path):
        """
        添加白名单目录

        Args:
            directory: 要添加的目录路径
        """
        resolved_dir = directory.resolve()
        if resolved_dir not in self._whitelist_dirs:
            self._whitelist_dirs.append(resolved_dir)
            self.logger.info(f"添加白名单目录: {resolved_dir}")

    def get_whitelist_dirs(self) -> List[Path]:
        """获取当前白名单目录列表"""
        return self._whitelist_dirs.copy()
