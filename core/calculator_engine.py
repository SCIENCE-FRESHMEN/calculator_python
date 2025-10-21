import operator
import math
import re
from typing import List, Tuple, Optional, Union
from datetime import datetime
from core.history_manager import HistoryManager


class CalculatorEngine:
    """计算器核心引擎，修复小数运算问题"""

    def __init__(self):
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': self.safe_divide,
            '^': operator.pow,
            '√': math.sqrt,
            '×': operator.mul,
            '÷': self.safe_divide,
            '%': operator.mod
        }
        self.current_expression = ""
        self.history_manager = HistoryManager()
        self.last_result = None

    def safe_divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("除数不能为零")
        return a / b

    def add_to_expression(self, value: str) -> None:
        """修复小数输入逻辑：允许正确的小数格式（如 `.5`、`3.`、`2.5`）"""
        if not value:
            return

        # 处理连续计算（使用上一次结果）
        if self.last_result is not None and not self.current_expression:
            if value in self.operators and value not in ('-', '√'):
                self.current_expression = str(self.last_result)

        # 处理小数点（核心修复部分）
        if value == '.':
            # 允许表达式开头直接输入小数点（如 `.5` → 自动补全为 `0.5`）
            if not self.current_expression:
                self.current_expression += "0."
                return

            # 允许运算符后直接输入小数点（如 `5+` 后输入 `.3` → `5+0.3`）
            last_char = self.current_expression[-1]
            if last_char in self.operators or last_char in '(':
                self.current_expression += "0."
                return

            # 检查当前数字是否已有小数点（避免重复输入）
            # 分割当前表达式，取最后一个数字部分
            number_pattern = re.compile(r'[\d.]+$')
            match = number_pattern.search(self.current_expression)
            if match and '.' in match.group():
                return  # 已有小数点，不允许再输入

        # 防止连续添加运算符（特殊情况处理）
        if value in self.operators:
            if not self.current_expression:
                if value not in ('-', '√'):
                    return
            else:
                last_char = self.current_expression[-1]
                if last_char in self.operators and not (last_char == '√' and value == '-'):
                    return

        self.current_expression += value

    def clear_expression(self) -> None:
        self.current_expression = ""

    def delete_last_char(self) -> None:
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]

    def _clean_and_transform_expression(self, expr: str) -> str:
        """修复小数格式转换：处理 `.5` 等简写形式"""
        transformed = expr.replace('×', '*').replace('÷', '/')
        transformed = transformed.replace('^', '**')

        # 处理根号
        sqrt_pattern = re.compile(r'√(\()?(\S+?)(?(1)\))')
        transformed = sqrt_pattern.sub(r'math.sqrt(\2)', transformed)

        # 处理取余运算
        transformed = re.sub(r'(\d+)%(\d+)', r'\1 % \2', transformed)

        # 修复小数简写（核心修复：将 `.3` 转为 `0.3`，`3.` 转为 `3.0`）
        transformed = re.sub(r'(?<![\d])\.(\d+)', r'0.\1', transformed)  # .5 → 0.5
        transformed = re.sub(r'(\d+)\.(?![\d])', r'\1.0', transformed)  # 5. → 5.0

        return transformed

    def _is_valid_expression(self, expr: str) -> Tuple[bool, Optional[str]]:
        """放松小数相关的验证限制"""
        # 检查括号平衡
        stack = []
        for char in expr:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False, "括号不匹配（多了右括号）"
                stack.pop()
        if stack:
            return False, "括号不匹配（多了左括号）"

        # 检查无效字符（允许小数点）
        if not re.match(r'^[\d+\-*/().^√×÷%]+$', expr):
            return False, "包含无效字符（仅允许数字、运算符和小数点）"

        # 检查根号使用合法性
        for i, char in enumerate(expr):
            if char == '√':
                if i == len(expr) - 1:
                    return False, "根号后缺少表达式"
                next_char = expr[i + 1]
                if not (next_char.isdigit() or next_char in '(-.'):  # 允许根号后接小数点
                    return False, "根号后需跟数字、左括号或小数点"

        # 检查运算符位置合法性（允许小数点在数字开头/结尾）
        if expr[0] in self.operators and expr[0] not in ('-', '√'):
            return False, "表达式不能以运算符开头"
        if expr[-1] in self.operators and expr[-1] not in ('%', '.'):  # 允许以小数点结尾（自动补0）
            return False, "表达式不能以运算符结尾"

        return True, None

    def evaluate(self) -> Tuple[Optional[Union[float, int]], Optional[str]]:
        """优化小数计算结果显示：保留合理小数位数，避免精度丢失"""
        if not self.current_expression:
            return None, "表达式为空"

        is_valid, error_msg = self._is_valid_expression(self.current_expression)
        if not is_valid:
            return None, error_msg

        try:
            transformed_expr = self._clean_and_transform_expression(self.current_expression)
            safe_namespace = {
                '__builtins__': None,
                'math': math,
                'sqrt': math.sqrt,
                'pow': math.pow
            }

            result = eval(transformed_expr, safe_namespace)

            # 修复小数显示：保留最多6位小数，避免无意义的0（如 2.0 → 2，2.500000 → 2.5）
            if isinstance(result, float):
                # 检查是否为整数（如 4.0 → 4）
                if result.is_integer():
                    result = int(result)
                else:
                    # 保留最多6位小数，去除末尾的0
                    result = round(result, 6)
                    result = float(f"{result:.6f}".rstrip('0').rstrip('.') if '.' in f"{result:.6f}" else f"{result}")

            # 保存历史记录
            self.history_manager.add_entry(
                expression=self.current_expression,
                result=str(result),
                timestamp=datetime.now()
            )
            self.last_result = result
            return result, None

        except ZeroDivisionError:
            return None, "错误：除数不能为零"
        except ValueError as e:
            if "math domain error" in str(e):
                return None, "错误：不能对负数开平方"
            return None, f"错误：{str(e)}"
        except SyntaxError:
            return None, "错误：表达式语法错误（可能缺少数字或括号）"
        except Exception as e:
            return None, f"计算错误：{str(e)}"

    def get_history(self) -> List[dict]:
        return self.history_manager.get_history()

    def clear_history(self) -> None:
        self.history_manager.clear_history()

    def use_last_result(self) -> None:
        if self.last_result is not None:
            self.current_expression += str(self.last_result)