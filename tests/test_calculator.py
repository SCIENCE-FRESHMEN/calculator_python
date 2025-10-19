import unittest
import math
from core.calculator_engine import CalculatorEngine
from core.validator import InputValidator


class TestCalculatorEngine(unittest.TestCase):
    """计算器引擎测试类"""

    def setUp(self):
        """测试前初始化计算器引擎"""
        self.calc = CalculatorEngine()

    def test_addition(self):
        """测试加法运算"""
        self.calc.current_expression = "2+3"
        result, error = self.calc.evaluate()
        self.assertEqual(result, 5)
        self.assertIsNone(error)

    def test_subtraction(self):
        """测试减法运算"""
        self.calc.current_expression = "10-4"
        result, error = self.calc.evaluate()
        self.assertEqual(result, 6)
        self.assertIsNone(error)

    def test_multiplication(self):
        """测试乘法运算"""
        self.calc.current_expression = "5*6"
        result, error = self.calc.evaluate()
        self.assertEqual(result, 30)
        self.assertIsNone(error)

    def test_division(self):
        """测试除法运算"""
        self.calc.current_expression = "10/2"
        result, error = self.calc.evaluate()
        self.assertEqual(result, 5)
        self.assertIsNone(error)

    def test_division_by_zero(self):
        """测试除以零的情况"""
        self.calc.current_expression = "5/0"
        result, error = self.calc.evaluate()
        self.assertIsNone(result)
        self.assertIsNotNone(error)

    def test_power(self):
        """测试幂运算"""
        self.calc.current_expression = "2^3"
        result, error = self.calc.evaluate()
        self.assertEqual(result, 8)
        self.assertIsNone(error)

    def test_square_root(self):
        """测试平方根运算"""
        self.calc.current_expression = "√16"
        result, error = self.calc.evaluate()
        self.assertEqual(result, 4)
        self.assertIsNone(error)

    def test_complex_expression(self):
        """测试复杂表达式"""
        self.calc.current_expression = "((5+3)*2)-4"
        result, error = self.calc.evaluate()
        self.assertEqual(result, 12)
        self.assertIsNone(error)

    def test_clear_expression(self):
        """测试清除表达式"""
        self.calc.current_expression = "123+456"
        self.calc.clear_expression()
        self.assertEqual(self.calc.current_expression, "")

    def test_delete_last_char(self):
        """测试删除最后一个字符"""
        self.calc.current_expression = "123+456"
        self.calc.delete_last_char()
        self.assertEqual(self.calc.current_expression, "123+45")

    def test_history_recording(self):
        """测试历史记录功能"""
        self.calc.current_expression = "2+2"
        self.calc.evaluate()
        history = self.calc.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['expression'], "2+2")
        self.assertEqual(history[0]['result'], "4")


class TestInputValidator(unittest.TestCase):
    """输入验证器测试类"""

    def setUp(self):
        """测试前初始化验证器"""
        self.validator = InputValidator()

    def test_valid_numbers(self):
        """测试有效数字输入"""
        self.assertTrue(self.validator.is_valid_number("0"))
        self.assertTrue(self.validator.is_valid_number("123"))
        self.assertTrue(self.validator.is_valid_number("123.45"))
        self.assertTrue(self.validator.is_valid_number(".5"))
        self.assertTrue(self.validator.is_valid_number("5."))

    def test_invalid_numbers(self):
        """测试无效数字输入"""
        self.assertFalse(self.validator.is_valid_number("abc"))
        self.assertFalse(self.validator.is_valid_number("12.34.56"))
        self.assertFalse(self.validator.is_valid_number("12a34"))

    def test_valid_expressions(self):
        """测试有效表达式"""
        self.assertTrue(self.validator.is_valid_expression("1+2"))
        self.assertTrue(self.validator.is_valid_expression("(3*4)-5"))
        self.assertTrue(self.validator.is_valid_expression("√(16+9)"))
        self.assertTrue(self.validator.is_valid_expression("2^3+4"))

    def test_invalid_expressions(self):
        """测试无效表达式"""
        self.assertFalse(self.validator.is_valid_expression("1++2"))
        self.assertFalse(self.validator.is_valid_expression("(3*4-5"))
        self.assertFalse(self.validator.is_valid_expression("12/"))
        self.assertFalse(self.validator.is_valid_expression("√16+"))


if __name__ == '__main__':
    unittest.main()
