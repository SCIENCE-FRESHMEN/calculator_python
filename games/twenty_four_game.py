import random
from itertools import permutations, product
from typing import List, Optional, Tuple


class TwentyFourGame:
    """二十四点游戏核心逻辑"""

    def __init__(self):
        self.numbers = []  # 当前题目数字
        self.solution = ""  # 解决方案
        self.difficulty = 1  # 难度等级 1-3

    def generate_numbers(self, difficulty: int = 1) -> List[int]:
        """
        生成符合难度的四个数字

        难度1: 1-10的数字，包含更多可解组合
        难度2: 1-13的数字，增加难度
        难度3: 1-13的数字，包含更多质数和大数
        """
        self.difficulty = difficulty

        if difficulty == 1:
            # 简单模式：1-10，更多小数字
            self.numbers = [random.randint(1, 10) for _ in range(4)]
        elif difficulty == 2:
            # 中等模式：1-13，均衡分布
            self.numbers = [random.randint(1, 13) for _ in range(4)]
        else:
            # 困难模式：增加大数和质数概率
            pool = [1, 2, 3, 5, 7, 11, 13] + [random.randint(4, 10) for _ in range(5)]
            self.numbers = random.sample(pool, 4)

        # 确保生成的数字有解
        if not self.find_solution():
            return self.generate_numbers(difficulty)

        return self.numbers

    def find_solution(self) -> bool:
        """寻找当前数字组合的解决方案，返回是否有解"""
        # 所有可能的运算符组合 (+, -, *, /)
        operators = ['+', '-', '*', '/']

        # 尝试所有数字排列
        for nums in permutations(self.numbers):
            # 尝试所有运算符组合
            for ops in product(operators, repeat=3):
                # 尝试不同的运算顺序（括号位置）
                # 形式1: ((a op1 b) op2 c) op3 d
                try:
                    result1 = self.calculate(nums[0], nums[1], ops[0])
                    result2 = self.calculate(result1, nums[2], ops[1])
                    final = self.calculate(result2, nums[3], ops[2])
                    if abs(final - 24) < 0.001:
                        self.solution = f"(({nums[0]} {ops[0]} {nums[1]}) {ops[1]} {nums[2]}) {ops[2]} {nums[3]}"
                        return True
                except:
                    pass

                # 形式2: (a op1 (b op2 c)) op3 d
                try:
                    result1 = self.calculate(nums[1], nums[2], ops[1])
                    result2 = self.calculate(nums[0], result1, ops[0])
                    final = self.calculate(result2, nums[3], ops[2])
                    if abs(final - 24) < 0.001:
                        self.solution = f"({nums[0]} {ops[0]} ({nums[1]} {ops[1]} {nums[2]})) {ops[2]} {nums[3]}"
                        return True
                except:
                    pass

                # 形式3: a op1 ((b op2 c) op3 d)
                try:
                    result1 = self.calculate(nums[1], nums[2], ops[1])
                    result2 = self.calculate(result1, nums[3], ops[2])
                    final = self.calculate(nums[0], result2, ops[0])
                    if abs(final - 24) < 0.001:
                        self.solution = f"{nums[0]} {ops[0]} (({nums[1]} {ops[1]} {nums[2]}) {ops[2]} {nums[3]})"
                        return True
                except:
                    pass

                # 形式4: a op1 (b op2 (c op3 d))
                try:
                    result1 = self.calculate(nums[2], nums[3], ops[2])
                    result2 = self.calculate(nums[1], result1, ops[1])
                    final = self.calculate(nums[0], result2, ops[0])
                    if abs(final - 24) < 0.001:
                        self.solution = f"{nums[0]} {ops[0]} ({nums[1]} {ops[1]} ({nums[2]} {ops[2]} {nums[3]}))"
                        return True
                except:
                    pass

                # 形式5: (a op1 b) op2 (c op3 d)
                try:
                    result1 = self.calculate(nums[0], nums[1], ops[0])
                    result2 = self.calculate(nums[2], nums[3], ops[2])
                    final = self.calculate(result1, result2, ops[1])
                    if abs(final - 24) < 0.001:
                        self.solution = f"({nums[0]} {ops[0]} {nums[1]}) {ops[1]} ({nums[2]} {ops[2]} {nums[3]})"
                        return True
                except:
                    pass

        return False

    def calculate(self, a: float, b: float, op: str) -> float:
        """执行基本运算，处理除法特殊情况"""
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                raise ValueError("除数不能为零")
            return a / b
        else:
            raise ValueError(f"未知运算符: {op}")

    def get_hint(self) -> str:
        """提供一个解题提示"""
        if not self.solution:
            return "抱歉，没有提示可用"

        # 根据难度提供不同详细程度的提示
        if self.difficulty == 1:
            # 简单提示：指出一个运算符
            for op in ['+', '-', '*', '/']:
                if op in self.solution:
                    return f"尝试使用 {op} 运算符"
        elif self.difficulty == 2:
            # 中等提示：指出两个数字的组合
            for num1 in self.numbers:
                for num2 in self.numbers:
                    if num1 != num2 and f"{num1} " in self.solution and f" {num2}" in self.solution:
                        return f"尝试将 {num1} 和 {num2} 先组合运算"
        else:
            # 困难提示：指出部分表达式
            return f"尝试这样开始: {self.solution[:8]}..."

        return "思考一下如何组合这些数字"

    def check_answer(self, user_answer: str) -> Tuple[bool, str]:
        """
        验证用户答案是否正确

        返回:
            Tuple[是否正确, 反馈信息]
        """
        if not user_answer:
            return False, "请输入你的答案"

        # 简单验证：检查计算结果是否为24
        try:
            # 替换用户输入中的×为*，÷为/
            normalized = user_answer.replace('×', '*').replace('÷', '/')

            # 检查是否使用了所有数字
            for num in self.numbers:
                if str(num) not in normalized:
                    return False, f"请使用所有数字: {self.numbers}"

            # 计算结果
            result = eval(normalized)

            if abs(result - 24) < 0.001:
                return True, "太棒了，正确答案！"
            else:
                return False, f"计算结果是 {result}，不是24哦"
        except Exception as e:
            return False, f"表达式有误: {str(e)}"

    def get_solution(self) -> str:
        """返回完整解决方案"""
        return self.solution if self.solution else "没有找到解决方案"
