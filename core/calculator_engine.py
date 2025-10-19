import operator
import math
import re
from typing import List, Tuple, Optional, Union
from datetime import datetime
from core.history_manager import HistoryManager


class CalculatorEngine:
    """计算器核心引擎，处理所有数学运算和历史记录"""

    def __init__(self):
        # 初始化运算符映射，将运算符字符串映射到对应的函数
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': self.safe_divide,
            '^': operator.pow,
            '√': math.sqrt,
            '×': operator.mul,  # 支持界面乘法符号
            '÷': self.safe_divide  # 支持界面除法符号
        }

        # 当前输入的表达式
        self.current_expression = ""
        # 历史记录管理器
        self.history_manager = HistoryManager()

    def safe_divide(self, a: float, b: float) -> float:
        """安全除法，处理除数为零的情况"""
        if b == 0:
            raise ZeroDivisionError("除数不能为零")
        return a / b

    def add_to_expression(self, value: str) -> None:
        """向当前表达式添加数字或运算符，增强输入验证"""
        if not value:
            return

        # 防止连续添加运算符（除了负号和根号的特殊情况）
        if value in self.operators:
            if not self.current_expression:
                # 允许表达式开头为负号或根号
                if value not in ('-', '√'):
                    return
            else:
                last_char = self.current_expression[-1]
                # 不允许连续两个运算符（除了根号后可跟负号）
                if last_char in self.operators and not (last_char == '√' and value == '-'):
                    return

        self.current_expression += value

    def clear_expression(self) -> None:
        """清除当前表达式"""
        self.current_expression = ""

    def delete_last_char(self) -> None:
        """删除表达式最后一个字符"""
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]

    def _clean_and_transform_expression(self, expr: str) -> str:
        """清洗和转换表达式，将界面符号转换为可计算格式"""
        # 替换界面运算符为Python可识别的运算符
        transformed = expr.replace('×', '*').replace('÷', '/')

        # 处理幂运算
        transformed = transformed.replace('^', '**')

        # 处理平方根 - 支持√数字和√(表达式)格式
        sqrt_pattern = re.compile(r'√(\d+|\(\S+\))')
        transformed = sqrt_pattern.sub(r'math.sqrt(\1)', transformed)

        return transformed

    def _is_valid_expression(self, expr: str) -> Tuple[bool, Optional[str]]:
        """验证表达式合法性"""
        # 检查括号平衡
        stack = []
        for char in expr:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False, "括号不匹配"
                stack.pop()
        if stack:
            return False, "括号不匹配"

        # 检查无效字符
        if not re.match(r'^[\d+\-*/().^√×÷]+$', expr):
            return False, "包含无效字符"

        # 检查根号使用合法性
        for i, char in enumerate(expr):
            if char == '√':
                if i == len(expr) - 1:
                    return False, "根号后缺少表达式"
                next_char = expr[i + 1]
                if not (next_char.isdigit() or next_char == '(' or next_char == '-'):
                    return False, "根号使用不正确"

        return True, None

    def evaluate(self) -> Tuple[Optional[Union[float, int]], Optional[str]]:
        """
        计算当前表达式的值

        返回:
            Tuple[结果值, 错误信息] 如果计算成功，错误信息为None；否则结果为None
        """
        if not self.current_expression:
            return None, "表达式为空"

        # 验证表达式合法性
        is_valid, error_msg = self._is_valid_expression(self.current_expression)
        if not is_valid:
            return None, error_msg

        try:
            # 转换表达式格式
            transformed_expr = self._clean_and_transform_expression(self.current_expression)

            # 安全计算环境，限制可用函数
            safe_namespace = {
                '__builtins__': None,
                'math': math,
                'sqrt': math.sqrt,
                'pow': math.pow
            }

            # 执行计算
            result = eval(transformed_expr, safe_namespace)

            # 处理整数显示
            if isinstance(result, float) and result.is_integer():
                result = int(result)

            # 保存到历史记录
            self.history_manager.add_entry(
                expression=self.current_expression,
                result=str(result),
                timestamp=datetime.now()
            )

            return result, None

        except ZeroDivisionError:
            return None, "错误：除数不能为零"
        except ValueError as e:
            if "math domain error" in str(e):
                return None, "错误：不能对负数开平方"
            return None, f"错误：{str(e)}"
        except SyntaxError:
            return None, "错误：表达式语法错误"
        except Exception as e:
            return None, f"计算错误：{str(e)}"

    def get_history(self) -> List[dict]:
        """获取计算历史记录"""
        return self.history_manager.get_history()

    def clear_history(self) -> None:
        """清除所有历史记录"""
        self.history_manager.clear_history()