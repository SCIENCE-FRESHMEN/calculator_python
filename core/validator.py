import re
from typing import Optional


class InputValidator:
    """验证计算器输入的有效性"""

    def __init__(self):
        """初始化验证器，编译正则表达式"""
        # 匹配有效的数字（整数、小数）
        self.number_pattern = re.compile(
            r'^[-+]?'  # 可选的正负号
            r'(\d+(\.\d*)?|\.\d+)'  # 数字部分（整数、带小数点的数或纯小数）
            r'$'  # 结束
        )

        # 匹配有效的表达式（简化版，主要用于基本验证）
        self.expression_pattern = re.compile(
            r'^[\d+\-*/().^√]+$'  # 只允许数字和特定运算符
        )

        # 运算符集合
        self.operators = {'+', '-', '*', '/', '^', '√'}

    def is_valid_number(self, input_str: str) -> bool:
        """
        检查输入是否为有效的数字

        参数:
            input_str: 要检查的输入字符串

        返回:
            如果是有效数字则返回True，否则返回False
        """
        if not input_str or not isinstance(input_str, str):
            return False
        return bool(self.number_pattern.match(input_str.strip()))

    def is_valid_expression(self, expression: str) -> bool:
        """
        检查表达式是否有效

        参数:
            expression: 要检查的表达式

        返回:
            如果表达式有效则返回True，否则返回False
        """
        if not expression or not isinstance(expression, str):
            return False

        # 基本字符检查
        if not self.expression_pattern.match(expression):
            return False

        # 检查括号是否匹配
        if not self._is_balanced_parentheses(expression):
            return False

        # 检查连续运算符（除了负号）
        if self._has_invalid_operator_sequence(expression):
            return False

        # 检查根号后的表达式是否有效
        if not self._is_valid_square_root_usage(expression):
            return False

        return True

    def _is_balanced_parentheses(self, expression: str) -> bool:
        """检查括号是否平衡（数量相等且正确嵌套）"""
        stack = []
        for char in expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False  # 右括号多于左括号
                stack.pop()
        return len(stack) == 0  # 左右括号数量相等

    def _has_invalid_operator_sequence(self, expression: str) -> bool:
        """检查是否有无效的运算符序列（如连续两个运算符）"""
        # 允许的运算符序列例外情况：负号开头或左括号后的负号
        # 以及根号后的负号（虽然数学上无效，但在这里只做格式检查）
        for i in range(len(expression) - 1):
            current = expression[i]
            next_char = expression[i + 1]

            if current in self.operators and next_char in self.operators:
                # 检查是否是允许的例外情况
                if not (
                        # 负号情况：当前是负号且前一个字符是运算符或开头
                        (current == '-' and (
                                i == 0 or expression[i - 1] in self.operators or expression[i - 1] == '(')) or
                        # 根号后面跟负号的情况
                        (current == '√' and next_char == '-')
                ):
                    return True
        return False

    def _is_valid_square_root_usage(self, expression: str) -> bool:
        """检查根号的使用是否有效（根号后必须跟数字或左括号）"""
        for i, char in enumerate(expression):
            if char == '√':
                # 根号不能是最后一个字符
                if i == len(expression) - 1:
                    return False
                next_char = expression[i + 1]
                # 根号后必须跟数字或左括号
                if not (next_char.isdigit() or next_char == '('):
                    return False
        return True

    def get_validation_error(self, expression: str) -> Optional[str]:
        """
        获取验证错误信息

        参数:
            expression: 要检查的表达式

        返回:
            错误信息，如果没有错误则返回None
        """
        if not expression:
            return "表达式不能为空"

        if not self.expression_pattern.match(expression):
            return "表达式包含无效字符"

        if not self._is_balanced_parentheses(expression):
            return "括号不匹配"

        if self._has_invalid_operator_sequence(expression):
            return "包含无效的运算符序列"

        if not self._is_valid_square_root_usage(expression):
            return "根号使用不正确"

        return None
