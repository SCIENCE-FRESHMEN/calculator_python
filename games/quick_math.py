import random
from typing import Tuple, Optional


class QuickMathGame:
    """速算挑战游戏核心逻辑"""

    def __init__(self):
        self.difficulty = 1  # 难度等级 1-3
        self.current_question = ""
        self.current_answer = 0
        self.operators = ['+', '-']  # 初始运算符

    def set_difficulty(self, difficulty: int) -> None:
        """设置游戏难度"""
        if 1 <= difficulty <= 3:
            self.difficulty = difficulty
            # 根据难度调整可用运算符
            if difficulty >= 2:
                self.operators = ['+', '-', '*']
            if difficulty >= 3:
                self.operators = ['+', '-', '*', '/']

    def generate_question(self) -> Tuple[str, float]:
        """
        生成一个速算问题

        返回:
            Tuple[问题字符串, 正确答案]
        """
        # 根据难度调整数字范围
        if self.difficulty == 1:
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
        elif self.difficulty == 2:
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 15)
        else:  # difficulty == 3
            num1 = random.randint(1, 50)
            num2 = random.randint(1, 20)

        # 随机选择运算符
        op = random.choice(self.operators)

        # 确保减法结果不为负，除法结果为整数
        if op == '-':
            # 确保结果非负
            if num1 < num2:
                num1, num2 = num2, num1
            self.current_answer = num1 - num2
        elif op == '*':
            # 难度3时使用更大的数字
            if self.difficulty == 3:
                num1 = random.randint(1, 15)
                num2 = random.randint(1, 10)
            self.current_answer = num1 * num2
        elif op == '/':
            # 确保可以整除且除数不为零
            num2 = random.randint(1, 10)
            num1 = num2 * random.randint(1, 10)
            self.current_answer = num1 // num2
        else:  # '+'
            self.current_answer = num1 + num2

        # 构建问题字符串
        self.current_question = f"{num1} {op} {num2} = ?"
        return self.current_question, self.current_answer

    def check_answer(self, user_answer: str) -> bool:
        """
        检查用户答案是否正确

        参数:
            user_answer: 用户输入的答案字符串

        返回:
            如果答案正确则返回True，否则返回False
        """
        try:
            # 转换用户答案为数字
            user_num = float(user_answer)

            # 考虑浮点数精度问题
            return abs(user_num - self.current_answer) < 0.001
        except ValueError:
            # 输入不是有效的数字
            return False

    def get_correct_answer(self) -> str:
        """返回当前问题的正确答案字符串"""
        # 如果是整数，返回整数形式，否则返回浮点数
        if isinstance(self.current_answer, float) and self.current_answer.is_integer():
            return str(int(self.current_answer))
        return str(self.current_answer)
