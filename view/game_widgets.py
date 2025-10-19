from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QGridLayout, QMessageBox,
                             QSlider, QGroupBox, QFormLayout, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QRect, QPoint
from PyQt5.QtGui import QFont, QPainter, QBrush, QColor, QPen, QKeyEvent
import sys
import random
from games.twenty_four_game import TwentyFourGame
from games.snake_game import SnakeGame
from games.quick_math import QuickMathGame


class GameBaseWidget(QWidget):
    """游戏界面基类，包含通用功能"""
    back_to_calculator = pyqtSignal()

    def __init__(self, achievement_system, parent=None):
        super().__init__(parent)
        self.achievement_system = achievement_system
        self.init_ui()

    def init_ui(self):
        """初始化UI，由子类实现"""
        pass

    def create_game_header(self, title: str):
        """创建游戏标题栏和返回按钮"""
        header_layout = QHBoxLayout()

        # 返回按钮
        back_btn = QPushButton("← 返回计算器")
        back_btn.clicked.connect(self.back_to_calculator)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        header_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # 游戏标题
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # 占位符，用于平衡布局
        header_layout.addStretch(1)

        return header_layout


class TwentyFourGameWidget(GameBaseWidget):
    """二十四点游戏界面"""

    def __init__(self, achievement_system, parent=None):
        self.game = TwentyFourGame()
        self.current_numbers = []
        super().__init__(achievement_system, parent)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 添加标题栏
        header_layout = self.create_game_header("二十四点挑战")
        main_layout.addLayout(header_layout)

        # 难度选择
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel("难度: ")
        difficulty_label.setFont(QFont("Arial", 14))

        self.difficulty_buttons = []
        for i, text in enumerate(["简单", "中等", "困难"]):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setFont(QFont("Arial", 14))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border-radius: 5px;
                    padding: 5px 15px;
                    margin: 0 5px;
                }
                QPushButton:checked {
                    background-color: #2980b9;
                    border: 2px solid #1f6dad;
                }
            """)
            btn.clicked.connect(lambda checked, d=i + 1: self.set_difficulty(d))
            self.difficulty_buttons.append(btn)
            difficulty_layout.addWidget(btn)

        difficulty_layout.addStretch(1)
        difficulty_layout.insertWidget(0, difficulty_label)
        main_layout.addLayout(difficulty_layout)

        # 默认选择简单难度
        self.difficulty_buttons[0].setChecked(True)
        self.game.difficulty = 1

        # 数字显示区域
        self.numbers_frame = QFrame()
        self.numbers_frame.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        numbers_layout = QHBoxLayout(self.numbers_frame)
        numbers_layout.setSpacing(20)
        numbers_layout.setAlignment(Qt.AlignCenter)

        self.number_labels = []
        for _ in range(4):
            lbl = QLabel("?")
            lbl.setFont(QFont("Arial", 36, QFont.Bold))
            lbl.setStyleSheet("color: #2c3e50; background-color: #ecf0f1; border-radius: 10px; padding: 15px 25px;")
            lbl.setAlignment(Qt.AlignCenter)
            self.number_labels.append(lbl)
            numbers_layout.addWidget(lbl)

        main_layout.addWidget(self.numbers_frame)

        # 输入区域
        input_layout = QVBoxLayout()

        input_label = QLabel("请用上面的数字，通过加减乘除和括号，计算出24:")
        input_label.setFont(QFont("Arial", 14))
        input_layout.addWidget(input_label)

        self.answer_input = QLineEdit()
        self.answer_input.setFont(QFont("Arial", 16))
        self.answer_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 2px solid #bdc3c7;")
        input_layout.addWidget(self.answer_input)

        # 按钮区域
        buttons_layout = QHBoxLayout()

        self.submit_btn = QPushButton("提交答案")
        self.submit_btn.setFont(QFont("Arial", 14))
        self.submit_btn.setStyleSheet("""
            background-color: #2ecc71;
            color: white;
            border-radius: 5px;
            padding: 10px;
            margin-right: 10px;
        """)
        self.submit_btn.clicked.connect(self.check_answer)

        self.hint_btn = QPushButton("提示")
        self.hint_btn.setFont(QFont("Arial", 14))
        self.hint_btn.setStyleSheet("""
            background-color: #f39c12;
            color: white;
            border-radius: 5px;
            padding: 10px;
            margin-right: 10px;
        """)
        self.hint_btn.clicked.connect(self.show_hint)

        self.new_btn = QPushButton("新题目")
        self.new_btn.setFont(QFont("Arial", 14))
        self.new_btn.setStyleSheet("""
            background-color: #9b59b6;
            color: white;
            border-radius: 5px;
            padding: 10px;
        """)
        self.new_btn.clicked.connect(self.generate_new_game)

        buttons_layout.addWidget(self.submit_btn)
        buttons_layout.addWidget(self.hint_btn)
        buttons_layout.addWidget(self.new_btn)
        input_layout.addLayout(buttons_layout)

        main_layout.addLayout(input_layout)

        # 反馈区域
        self.feedback_label = QLabel("")
        self.feedback_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("min-height: 30px;")
        main_layout.addWidget(self.feedback_label)

        # 状态区域
        stats_layout = QHBoxLayout()

        self.score_label = QLabel("已解决: 0题")
        self.score_label.setFont(QFont("Arial", 14))
        stats_layout.addWidget(self.score_label)

        stats_layout.addStretch(1)

        self.solution_label = QLabel("")
        self.solution_label.setFont(QFont("Arial", 14))
        self.solution_label.setStyleSheet("color: #7f8c8d;")
        stats_layout.addWidget(self.solution_label)

        main_layout.addLayout(stats_layout)

        # 初始化游戏
        self.generate_new_game()

        # 初始化统计
        self.games_won = 0

    def set_difficulty(self, difficulty: int):
        """设置游戏难度"""
        self.game.difficulty = difficulty
        # 更新按钮状态
        for i, btn in enumerate(self.difficulty_buttons):
            btn.setChecked(i + 1 == difficulty)

    def generate_new_game(self):
        """生成新的游戏题目"""
        self.current_numbers = self.game.generate_numbers(self.game.difficulty)
        # 更新数字显示
        for i, num in enumerate(self.current_numbers):
            self.number_labels[i].setText(str(num))

        # 重置输入和反馈
        self.answer_input.clear()
        self.feedback_label.setText("")
        self.solution_label.setText("")

        # 更新统计
        self.achievement_system.update_stat("twentyfour_games_played")

    def check_answer(self):
        """检查用户答案"""
        user_answer = self.answer_input.text().strip()
        if not user_answer:
            self.feedback_label.setText("请输入答案!")
            self.feedback_label.setStyleSheet("color: #f39c12; text-align: center;")
            return

        is_correct, message = self.game.check_answer(user_answer)

        if is_correct:
            self.feedback_label.setText(f"正确! {message}")
            self.feedback_label.setStyleSheet("color: #2ecc71; text-align: center;")
            self.games_won += 1
            self.score_label.setText(f"已解决: {self.games_won}题")
            # 显示正确答案
            self.solution_label.setText(f"一种解法: {self.game.get_solution()}")
            # 更新成就系统
            self.achievement_system.update_stat("twentyfour_games_won")
        else:
            self.feedback_label.setText(f"不正确: {message}")
            self.feedback_label.setStyleSheet("color: #e74c3c; text-align: center;")

    def show_hint(self):
        """显示提示"""
        hint = self.game.get_hint()
        self.feedback_label.setText(f"提示: {hint}")
        self.feedback_label.setStyleSheet("color: #f39c12; text-align: center;")


class SnakeGameWidget(GameBaseWidget):
    """贪吃蛇游戏界面"""

    def __init__(self, achievement_system, parent=None):
        self.game = SnakeGame(width=20, height=15)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        super().__init__(achievement_system, parent)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 添加标题栏
        header_layout = self.create_game_header("数学贪吃蛇")
        main_layout.addLayout(header_layout)

        # 状态区域
        status_layout = QHBoxLayout()

        self.score_label = QLabel("分数: 0")
        self.score_label.setFont(QFont("Arial", 14, QFont.Bold))
        status_layout.addWidget(self.score_label)

        self.level_label = QLabel("等级: 1")
        self.level_label.setFont(QFont("Arial", 14, QFont.Bold))
        status_layout.addWidget(self.level_label)

        status_layout.addStretch(1)

        self.start_btn = QPushButton("开始游戏")
        self.start_btn.setFont(QFont("Arial", 14))
        self.start_btn.setStyleSheet("""
            background-color: #2ecc71;
            color: white;
            border-radius: 5px;
            padding: 5px 15px;
        """)
        self.start_btn.clicked.connect(self.start_game)

        self.reset_btn = QPushButton("重置游戏")
        self.reset_btn.setFont(QFont("Arial", 14))
        self.reset_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            border-radius: 5px;
            padding: 5px 15px;
        """)
        self.reset_btn.clicked.connect(self.reset_game)

        status_layout.addWidget(self.start_btn)
        status_layout.addWidget(self.reset_btn)

        main_layout.addLayout(status_layout)

        # 游戏区域
        self.game_area = QFrame()
        self.game_area.setStyleSheet("background-color: #2c3e50; border-radius: 10px;")
        self.game_area.setMinimumSize(600, 450)
        main_layout.addWidget(self.game_area)

        # 控制说明
        controls_layout = QHBoxLayout()

        controls_label = QLabel("使用方向键控制蛇的移动 | 吃到食物后请解答数学题")
        controls_label.setFont(QFont("Arial", 12))
        controls_layout.addWidget(controls_label)

        main_layout.addLayout(controls_layout)

        # 数学题对话框（初始隐藏）
        self.math_dialog = QFrame()
        self.math_dialog.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        self.math_dialog.setVisible(False)
        math_layout = QVBoxLayout(self.math_dialog)

        self.math_question_label = QLabel("")
        self.math_question_label.setFont(QFont("Arial", 16, QFont.Bold))
        math_layout.addWidget(self.math_question_label)

        math_input_layout = QHBoxLayout()
        math_input_label = QLabel("答案: ")
        math_input_label.setFont(QFont("Arial", 14))

        self.math_answer_input = QLineEdit()
        self.math_answer_input.setFont(QFont("Arial", 14))
        self.math_answer_input.setStyleSheet("padding: 5px; border-radius: 5px;")
        self.math_answer_input.returnPressed.connect(self.check_math_answer)

        self.math_submit_btn = QPushButton("提交")
        self.math_submit_btn.setFont(QFont("Arial", 14))
        self.math_submit_btn.setStyleSheet("""
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            padding: 5px 15px;
        """)
        self.math_submit_btn.clicked.connect(self.check_math_answer)

        math_input_layout.addWidget(math_input_label)
        math_input_layout.addWidget(self.math_answer_input)
        math_input_layout.addWidget(self.math_submit_btn)
        math_layout.addLayout(math_input_layout)

        main_layout.addWidget(self.math_dialog)

        # 初始化游戏
        self.reset_game()

    def start_game(self):
        """开始游戏"""
        if not self.game.game_over:
            self.timer.start(int(self.game.speed * 1000))
            self.start_btn.setText("暂停")
            self.start_btn.clicked.disconnect()
            self.start_btn.clicked.connect(self.pause_game)
        else:
            self.reset_game()
            self.start_game()

    def pause_game(self):
        """暂停游戏"""
        self.timer.stop()
        self.start_btn.setText("继续")
        self.start_btn.clicked.disconnect()
        self.start_btn.clicked.connect(self.start_game)

    def reset_game(self):
        """重置游戏"""
        self.timer.stop()
        self.game.reset()
        self.score_label.setText(f"分数: {self.game.score}")
        self.level_label.setText(f"等级: {self.game.level}")
        self.start_btn.setText("开始游戏")
        self.start_btn.clicked.disconnect()
        self.start_btn.clicked.connect(self.start_game)
        self.math_dialog.setVisible(False)
        self.update()

    def update_game(self):
        """更新游戏状态"""
        moved = self.game.move()
        if not moved and self.game.game_over:
            self.timer.stop()
            QMessageBox.information(self, "游戏结束", f"游戏结束! 你的分数是: {self.game.score}")
            # 更新成就系统
            self.achievement_system.update_stat("snake_games_played")
            self.achievement_system.update_stat("snake_high_score", self.game.score, is_increment=False)

        # 检查是否需要显示数学题
        if self.game.waiting_for_math_answer:
            self.timer.stop()
            self.math_question_label.setText(self.game.math_question)
            self.math_answer_input.clear()
            self.math_dialog.setVisible(True)
            self.math_answer_input.setFocus()

        # 更新分数和等级显示
        self.score_label.setText(f"分数: {self.game.score}")
        self.level_label.setText(f"等级: {self.game.level}")

        # 重绘游戏区域
        self.update()

    def check_math_answer(self):
        """检查数学题答案"""
        user_answer = self.math_answer_input.text().strip()
        if self.game.check_math_answer(user_answer):
            self.math_dialog.setVisible(False)
            # 继续游戏
            self.timer.start(int(self.game.speed * 1000))
            # 更新成就系统
            self.achievement_system.update_stat("quickmath_correct_answers")
        else:
            QMessageBox.warning(self, "答案错误", "答案不正确，请再试一次!")
            self.math_answer_input.clear()
            self.math_answer_input.setFocus()

    def paintEvent(self, event):
        """绘制游戏元素"""
        if not hasattr(self, 'game_area'):
            return

        painter = QPainter(self)
        game_rect = self.game_area.geometry()

        # 计算每个格子的大小
        cell_width = game_rect.width() // self.game.width
        cell_height = game_rect.height() // self.game.height

        # 绘制蛇
        for i, (x, y) in enumerate(self.game.snake):
            # 蛇头颜色不同
            color = QColor(46, 204, 113) if i == 0 else QColor(39, 174, 96)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.NoPen))
            painter.drawRect(
                game_rect.x() + x * cell_width,
                game_rect.y() + y * cell_height,
                cell_width - 1,  # 减1是为了看到格子间的间隙
                cell_height - 1
            )

        # 绘制食物
        food_x, food_y = self.game.food_position
        painter.setBrush(QBrush(QColor(231, 76, 60)))
        painter.drawRect(
            game_rect.x() + food_x * cell_width,
            game_rect.y() + food_y * cell_height,
            cell_width - 1,
            cell_height - 1
        )

        # 在食物上显示数字
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        text = str(self.game.food_value)
        text_rect = painter.boundingRect(
            game_rect.x() + food_x * cell_width,
            game_rect.y() + food_y * cell_height,
            cell_width - 1,
            cell_height - 1,
            Qt.AlignCenter,
            text
        )
        painter.drawText(text_rect, Qt.AlignCenter, text)

    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() == Qt.Key_Left and self.game.direction != (1, 0):
            self.game.change_direction((-1, 0))
        elif event.key() == Qt.Key_Right and self.game.direction != (-1, 0):
            self.game.change_direction((1, 0))
        elif event.key() == Qt.Key_Up and self.game.direction != (0, 1):
            self.game.change_direction((0, -1))
        elif event.key() == Qt.Key_Down and self.game.direction != (0, -1):
            self.game.change_direction((0, 1))
        elif event.key() == Qt.Key_Space:
            if self.timer.isActive():
                self.pause_game()
            else:
                self.start_game()
        else:
            super().keyPressEvent(event)


class TetrisGameWidget(GameBaseWidget):
    """俄罗斯方块游戏界面（简化版）"""

    def __init__(self, achievement_system, parent=None):
        super().__init__(achievement_system, parent)
        # 这里只是一个占位实现，完整实现需要更复杂的逻辑
        self.score = 0
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 添加标题栏
        header_layout = self.create_game_header("数学俄罗斯方块")
        main_layout.addLayout(header_layout)

        # 状态区域
        status_layout = QHBoxLayout()

        self.score_label = QLabel("分数: 0")
        self.score_label.setFont(QFont("Arial", 14, QFont.Bold))
        status_layout.addWidget(self.score_label)

        status_layout.addStretch(1)

        self.start_btn = QPushButton("开始游戏")
        self.start_btn.setFont(QFont("Arial", 14))
        self.start_btn.setStyleSheet("""
            background-color: #2ecc71;
            color: white;
            border-radius: 5px;
            padding: 5px 15px;
        """)
        self.start_btn.clicked.connect(self.start_game)

        self.reset_btn = QPushButton("重置游戏")
        self.reset_btn.setFont(QFont("Arial", 14))
        self.reset_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            border-radius: 5px;
            padding: 5px 15px;
        """)
        self.reset_btn.clicked.connect(self.reset_game)

        status_layout.addWidget(self.start_btn)
        status_layout.addWidget(self.reset_btn)

        main_layout.addLayout(status_layout)

        # 游戏区域
        self.game_area = QFrame()
        self.game_area.setStyleSheet("background-color: #2c3e50; border-radius: 10px;")
        self.game_area.setMinimumSize(600, 450)

        # 临时提示文本
        temp_layout = QVBoxLayout(self.game_area)
        temp_label = QLabel("俄罗斯方块游戏正在开发中...\n完成一行会出现数学题，答对可获得额外分数!")
        temp_label.setFont(QFont("Arial", 16))
        temp_label.setStyleSheet("color: white; text-align: center;")
        temp_label.setAlignment(Qt.AlignCenter)
        temp_layout.addWidget(temp_label)

        main_layout.addWidget(self.game_area)

        # 控制说明
        controls_label = QLabel("使用方向键控制方块: ← → 移动, ↑ 旋转, ↓ 加速下落")
        controls_label.setFont(QFont("Arial", 12))
        main_layout.addWidget(controls_label)

    def start_game(self):
        """开始游戏"""
        QMessageBox.information(self, "开发中", "俄罗斯方块游戏正在开发中，敬请期待!")
        # 更新成就系统
        self.achievement_system.update_stat("tetris_games_played")

    def reset_game(self):
        """重置游戏"""
        self.score = 0
        self.score_label.setText(f"分数: {self.score}")


class QuickMathGameWidget(GameBaseWidget):
    """速算挑战游戏界面"""

    def __init__(self, achievement_system, parent=None):
        self.game = QuickMathGame()
        self.correct_count = 0
        self.incorrect_count = 0
        self.timer = QTimer()
        self.time_remaining = 60  # 60秒
        super().__init__(achievement_system, parent)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 添加标题栏
        header_layout = self.create_game_header("速算挑战")
        main_layout.addLayout(header_layout)

        # 难度选择
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel("难度: ")
        difficulty_label.setFont(QFont("Arial", 14))

        self.difficulty_buttons = []
        for i, text in enumerate(["简单", "中等", "困难"]):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setFont(QFont("Arial", 14))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border-radius: 5px;
                    padding: 5px 15px;
                    margin: 0 5px;
                }
                QPushButton:checked {
                    background-color: #2980b9;
                    border: 2px solid #1f6dad;
                }
            """)
            btn.clicked.connect(lambda checked, d=i + 1: self.set_difficulty(d))
            self.difficulty_buttons.append(btn)
            difficulty_layout.addWidget(btn)

        difficulty_layout.addStretch(1)
        difficulty_layout.insertWidget(0, difficulty_label)
        main_layout.addLayout(difficulty_layout)

        # 默认选择简单难度
        self.difficulty_buttons[0].setChecked(True)
        self.game.set_difficulty(1)

        # 状态区域
        status_layout = QHBoxLayout()

        self.score_label = QLabel("正确: 0 | 错误: 0")
        self.score_label.setFont(QFont("Arial", 14, QFont.Bold))
        status_layout.addWidget(self.score_label)

        self.time_label = QLabel(f"剩余时间: {self.time_remaining}秒")
        self.time_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.time_label.setStyleSheet("color: #e74c3c;")
        status_layout.addWidget(self.time_label)

        status_layout.addStretch(1)

        self.start_btn = QPushButton("开始挑战")
        self.start_btn.setFont(QFont("Arial", 14))
        self.start_btn.setStyleSheet("""
            background-color: #2ecc71;
            color: white;
            border-radius: 5px;
            padding: 5px 15px;
        """)
        self.start_btn.clicked.connect(self.start_game)

        status_layout.addWidget(self.start_btn)
        main_layout.addLayout(status_layout)

        # 问题区域
        self.question_frame = QFrame()
        self.question_frame.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        question_layout = QVBoxLayout(self.question_frame)

        self.question_label = QLabel("点击开始挑战")
        self.question_label.setFont(QFont("Arial", 32, QFont.Bold))
        self.question_label.setAlignment(Qt.AlignCenter)
        question_layout.addWidget(self.question_label)

        main_layout.addWidget(self.question_frame)

        # 输入区域
        input_layout = QHBoxLayout()

        self.answer_input = QLineEdit()
        self.answer_input.setFont(QFont("Arial", 24))
        self.answer_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 2px solid #bdc3c7;")
        self.answer_input.setAlignment(Qt.AlignCenter)
        self.answer_input.returnPressed.connect(self.check_answer)
        self.answer_input.setEnabled(False)

        self.submit_btn = QPushButton("提交")
        self.submit_btn.setFont(QFont("Arial", 18))
        self.submit_btn.setStyleSheet("""
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            margin-left: 10px;
        """)
        self.submit_btn.clicked.connect(self.check_answer)
        self.submit_btn.setEnabled(False)

        input_layout.addWidget(self.answer_input)
        input_layout.addWidget(self.submit_btn)
        main_layout.addLayout(input_layout)

        # 反馈区域
        self.feedback_label = QLabel("")
        self.feedback_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("min-height: 30px;")
        main_layout.addWidget(self.feedback_label)

        # 定时器设置
        self.timer.timeout.connect(self.update_timer)

    def set_difficulty(self, difficulty: int):
        """设置游戏难度"""
        self.game.set_difficulty(difficulty)
        # 更新按钮状态
        for i, btn in enumerate(self.difficulty_buttons):
            btn.setChecked(i + 1 == difficulty)

    def start_game(self):
        """开始速算挑战"""
        self.correct_count = 0
        self.incorrect_count = 0
        self.time_remaining = 60
        self.score_label.setText(f"正确: {self.correct_count} | 错误: {self.incorrect_count}")
        self.time_label.setText(f"剩余时间: {self.time_remaining}秒")
        self.feedback_label.setText("")

        # 生成第一个问题
        self.generate_new_question()

        # 启用输入
        self.answer_input.setEnabled(True)
        self.submit_btn.setEnabled(True)
        self.answer_input.clear()
        self.answer_input.setFocus()

        # 开始计时
        self.timer.start(1000)  # 每秒更新一次

        # 更新按钮状态
        self.start_btn.setEnabled(False)
        self.start_btn.setText("挑战中...")

        # 更新成就系统
        self.achievement_system.update_stat("quickmath_games_played")

    def generate_new_question(self):
        """生成新的问题"""
        question, _ = self.game.generate_question()
        self.question_label.setText(question)

    def check_answer(self):
        """检查答案"""
        user_answer = self.answer_input.text().strip()
        if not user_answer:
            return

        is_correct = self.game.check_answer(user_answer)

        if is_correct:
            self.feedback_label.setText("正确! 真棒!")
            self.feedback_label.setStyleSheet("color: #2ecc71; text-align: center;")
            self.correct_count += 1
            # 更新成就系统
            self.achievement_system.update_stat("quickmath_correct_answers")
        else:
            self.feedback_label.setText(f"错误! 正确答案是 {self.game.get_correct_answer()}")
            self.feedback_label.setStyleSheet("color: #e74c3c; text-align: center;")
            self.incorrect_count += 1

        # 更新分数
        self.score_label.setText(f"正确: {self.correct_count} | 错误: {self.incorrect_count}")

        # 生成新问题
        self.generate_new_question()
        self.answer_input.clear()

    def update_timer(self):
        """更新计时器"""
        self.time_remaining -= 1
        self.time_label.setText(f"剩余时间: {self.time_remaining}秒")

        # 时间到
        if self.time_remaining <= 0:
            self.timer.stop()
            self.answer_input.setEnabled(False)
            self.submit_btn.setEnabled(False)
            self.start_btn.setEnabled(True)
            self.start_btn.setText("再来一次")

            # 显示结果
            QMessageBox.information(
                self,
                "挑战结束",
                f"时间到!\n正确: {self.correct_count}题\n错误: {self.incorrect_count}题"
            )

    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() == Qt.Key_Return and self.answer_input.isEnabled():
            self.check_answer()
        else:
            super().keyPressEvent(event)
