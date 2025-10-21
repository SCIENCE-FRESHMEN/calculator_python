from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QGridLayout, QMessageBox,
                             QSlider, QGroupBox, QFormLayout, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QRect, QPoint
from PyQt5.QtGui import QFont, QPainter, QBrush, QColor, QPen, QKeyEvent, QImage, QPixmap
import sys
import random
import pygame  # 新增：确保导入pygame
from games.twenty_four_game import TwentyFourGame
from games.snake_game import SnakeGame
from games.quick_math import QuickMathGame
from games.teris_game import TetrisGame  # 修正：正确导入俄罗斯方块类


class GameBaseWidget(QWidget):
    """游戏界面基类，包含通用功能"""
    back_to_calculator = pyqtSignal()

    def __init__(self, achievement_system, parent=None):
        super().__init__(parent)
        self.achievement_system = achievement_system
        self.init_ui()  # 父类初始化时调用UI初始化

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
        super().__init__(achievement_system, parent)  # 调用父类初始化

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
    """贪吃蛇游戏界面（已修复父类初始化问题）"""

    def __init__(self, achievement_system, parent=None):
        # 1. 初始化自身属性
        self.game = SnakeGame(width=20, height=15)
        self.timer = QTimer()
        self.timer_interval = 200  # 初始速度（毫秒/帧）
        self.game.need_check = False  # 关闭验证，直接启动

        # 2. 关键修复：调用父类初始化方法（必须在属性初始化后调用）
        super().__init__(achievement_system, parent)

        # 3. 连接定时器信号（在父类初始化后执行）
        self.timer.timeout.connect(self.update_game)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 添加标题栏
        header_layout = self.create_game_header("数学贪吃蛇")
        main_layout.addLayout(header_layout)

        # 状态区域（分数、长度）
        status_layout = QHBoxLayout()
        self.score_label = QLabel("分数: 0")
        self.length_label = QLabel("长度: 1")
        self.score_label.setFont(QFont("Arial", 14))
        self.length_label.setFont(QFont("Arial", 14))
        status_layout.addWidget(self.score_label)
        status_layout.addStretch(1)
        status_layout.addWidget(self.length_label)
        main_layout.addLayout(status_layout)

        # Pygame画布（关键：将Pygame画面嵌入PyQt）
        self.game_canvas = QFrame()
        self.game_canvas.setFixedSize(
            self.game.grid_width * 25,  # 每个格子25像素
            self.game.grid_height * 25
        )
        self.game_canvas.setStyleSheet("background-color: #f0f0f0; border: 2px solid #333;")
        main_layout.addWidget(self.game_canvas)

        # 控制按钮
        control_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始游戏")
        self.pause_btn = QPushButton("暂停")
        self.reset_btn = QPushButton("重置")
        for btn in [self.start_btn, self.pause_btn, self.reset_btn]:
            btn.setFont(QFont("Arial", 14))
            control_layout.addWidget(btn)
        self.start_btn.clicked.connect(self.start_game)
        self.pause_btn.clicked.connect(self.pause_game)
        self.reset_btn.clicked.connect(self.reset_game)
        main_layout.addLayout(control_layout)

        # 初始化Pygame
        pygame.init()
        self.game_surface = pygame.Surface(
            (self.game.grid_width * 25, self.game.grid_height * 25)
        )

    def start_game(self):
        self.game.running = True
        self.timer.start(self.timer_interval)

    def pause_game(self):
        self.game.running = not self.game.running
        if self.game.running:
            self.timer.start(self.timer_interval)
        else:
            self.timer.stop()

    def reset_game(self):
        self.game.reset()
        self.score_label.setText(f"分数: {self.game.score}")
        self.length_label.setText(f"长度: {self.game.snake_length}")
        self.timer.start(self.timer_interval)

    def update_game(self):
        """更新游戏状态并绘制到PyQt组件"""
        if self.game.running:
            self.game.update()  # 更新游戏逻辑
            self.score_label.setText(f"分数: {self.game.score}")
            self.length_label.setText(f"长度: {self.game.snake_length}")

        # 绘制Pygame画面
        self.game.draw(self.game_surface)  # 假设SnakeGame有draw方法
        # 转换Pygame表面为PyQt图像
        w, h = self.game_surface.get_size()
        q_image = QImage(
            self.game_surface.get_buffer().raw,
            w, h, QImage.Format_RGB32
        )
        pixmap = QPixmap.fromImage(q_image)

        # 绘制到Qt组件
        painter = QPainter(self.game_canvas)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

    def keyPressEvent(self, event: QKeyEvent):
        """处理键盘事件（方向键控制）"""
        if event.key() == Qt.Key_Left:
            self.game.change_direction("LEFT")
        elif event.key() == Qt.Key_Right:
            self.game.change_direction("RIGHT")
        elif event.key() == Qt.Key_Up:
            self.game.change_direction("UP")
        elif event.key() == Qt.Key_Down:
            self.game.change_direction("DOWN")
        super().keyPressEvent(event)


class TetrisGameWidget(GameBaseWidget):
    """俄罗斯方块游戏界面"""

    def __init__(self, achievement_system, parent=None):
        self.game = TetrisGame()  # 初始化俄罗斯方块引擎
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        super().__init__(achievement_system, parent)  # 调用父类初始化

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题栏
        header_layout = self.create_game_header("俄罗斯方块")
        main_layout.addLayout(header_layout)

        # 主游戏区和信息区
        content_layout = QHBoxLayout()

        # 游戏画布（Pygame嵌入）
        self.game_canvas = QFrame()
        self.canvas_width = self.game.board.width * 30  # 每个格子30像素
        self.canvas_height = self.game.board.height * 30
        self.game_canvas.setFixedSize(self.canvas_width, self.canvas_height)
        self.game_canvas.setStyleSheet("background-color: #000; border: 2px solid #666;")
        content_layout.addWidget(self.game_canvas)

        # 右侧信息区（分数、下一个方块）
        info_layout = QVBoxLayout()
        self.score_label = QLabel("分数: 0")
        self.level_label = QLabel("等级: 1")
        for lbl in [self.score_label, self.level_label]:
            lbl.setFont(QFont("Arial", 16, QFont.Bold))
            lbl.setStyleSheet("color: #333; margin: 10px 0;")
            info_layout.addWidget(lbl)
        info_layout.addStretch(1)
        content_layout.addLayout(info_layout)

        main_layout.addLayout(content_layout)

        # 控制按钮
        control_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始")
        self.pause_btn = QPushButton("暂停")
        self.reset_btn = QPushButton("重置")
        for btn in [self.start_btn, self.pause_btn, self.reset_btn]:
            btn.setFont(QFont("Arial", 14))
            control_layout.addWidget(btn)
        self.start_btn.clicked.connect(self.start_game)
        self.pause_btn.clicked.connect(self.pause_game)
        self.reset_btn.clicked.connect(self.reset_game)
        main_layout.addLayout(control_layout)

        # 初始化Pygame
        pygame.init()
        self.game_surface = pygame.Surface((self.canvas_width, self.canvas_height))

    def start_game(self):
        self.game.paused = False
        self.timer.start(int(self.game.fall_speed * 1000))  # 根据游戏速度调整定时器

    def pause_game(self):
        self.game.toggle_pause()
        if self.game.paused:
            self.timer.stop()
        else:
            self.timer.start(int(self.game.fall_speed * 1000))

    def reset_game(self):
        self.game.reset()
        self.score_label.setText(f"分数: {self.game.score}")
        self.level_label.setText(f"等级: {self.game.level}")
        self.timer.start(int(self.game.fall_speed * 1000))

    def update_game(self):
        """更新游戏状态并绘制"""
        if not self.game.paused and not self.game.game_over:
            self.game.update(100)  # 更新游戏逻辑（传入毫秒数）
            self.score_label.setText(f"分数: {self.game.score}")
            self.level_label.setText(f"等级: {self.game.level}")
            # 随等级提升加快速度
            self.timer.setInterval(int(self.game.fall_speed * 1000))

        # 绘制游戏画面
        self.game_surface.fill((0, 0, 0))  # 黑色背景
        self.game.board.draw(self.game_surface)  # 绘制游戏板
        if self.game.current_piece:
            self.game.current_piece.draw(self.game_surface)  # 绘制当前方块

        # 转换为PyQt图像并显示
        w, h = self.game_surface.get_size()
        q_image = QImage(
            self.game_surface.get_buffer().raw,
            w, h, QImage.Format_RGB32
        )
        pixmap = QPixmap.fromImage(q_image)

        painter = QPainter(self.game_canvas)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

    def keyPressEvent(self, event: QKeyEvent):
        """处理键盘事件（方向键、空格等）"""
        if self.game.game_over:
            return
        if event.key() == Qt.Key_Left:
            self.game.move_left()
        elif event.key() == Qt.Key_Right:
            self.game.move_right()
        elif event.key() == Qt.Key_Down:
            self.game.move_down()
        elif event.key() == Qt.Key_Up:
            self.game.rotate()  # 旋转
        elif event.key() == Qt.Key_Space:
            while self.game.move_down():  # 硬降（一直下落直到碰撞）
                pass
        super().keyPressEvent(event)


class QuickMathGameWidget(GameBaseWidget):
    """速算挑战游戏界面"""

    def __init__(self, achievement_system, parent=None):
        self.game = QuickMathGame()  # 导入速算游戏核心逻辑
        self.timer = QTimer()  # 用于计时
        self.time_left = 10  # 初始答题时间（秒）
        self.score = 0  # 当前分数
        super().__init__(achievement_system, parent)  # 调用父类初始化

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
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

        # 计时区域
        timer_layout = QHBoxLayout()
        self.timer_label = QLabel(f"剩余时间: {self.time_left}秒")
        self.timer_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.timer_label.setStyleSheet("color: #e74c3c;")
        timer_layout.addWidget(self.timer_label)

        self.score_label = QLabel(f"当前分数: {self.score}")
        self.score_label.setFont(QFont("Arial", 14, QFont.Bold))
        timer_layout.addStretch(1)
        timer_layout.addWidget(self.score_label)
        main_layout.addLayout(timer_layout)

        # 问题显示区域
        self.question_frame = QFrame()
        self.question_frame.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        question_layout = QHBoxLayout(self.question_frame)

        self.question_label = QLabel("点击开始按钮开始游戏")
        self.question_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.question_label.setAlignment(Qt.AlignCenter)
        question_layout.addWidget(self.question_label)
        main_layout.addWidget(self.question_frame)

        # 答案输入区域
        input_layout = QVBoxLayout()

        input_label = QLabel("请输入答案:")
        input_label.setFont(QFont("Arial", 14))
        input_layout.addWidget(input_label)

        self.answer_input = QLineEdit()
        self.answer_input.setFont(QFont("Arial", 16))
        self.answer_input.setStyleSheet("padding: 10px; border-radius: 5px; border: 2px solid #bdc3c7;")
        self.answer_input.returnPressed.connect(self.check_answer)  # 回车提交
        input_layout.addWidget(self.answer_input)

        main_layout.addLayout(input_layout)

        # 按钮区域
        buttons_layout = QHBoxLayout()

        self.start_btn = QPushButton("开始游戏")
        self.start_btn.setFont(QFont("Arial", 14))
        self.start_btn.setStyleSheet("""
            background-color: #2ecc71;
            color: white;
            border-radius: 5px;
            padding: 10px;
            margin-right: 10px;
        """)
        self.start_btn.clicked.connect(self.start_game)

        self.submit_btn = QPushButton("提交答案")
        self.submit_btn.setFont(QFont("Arial", 14))
        self.submit_btn.setStyleSheet("""
            background-color: #f39c12;
            color: white;
            border-radius: 5px;
            padding: 10px;
            margin-right: 10px;
        """)
        self.submit_btn.clicked.connect(self.check_answer)
        self.submit_btn.setEnabled(False)  # 初始禁用

        self.next_btn = QPushButton("下一题")
        self.next_btn.setFont(QFont("Arial", 14))
        self.next_btn.setStyleSheet("""
            background-color: #9b59b6;
            color: white;
            border-radius: 5px;
            padding: 10px;
        """)
        self.next_btn.clicked.connect(self.generate_new_question)
        self.next_btn.setEnabled(False)  # 初始禁用

        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.submit_btn)
        buttons_layout.addWidget(self.next_btn)
        main_layout.addLayout(buttons_layout)

        # 反馈区域
        self.feedback_label = QLabel("")
        self.feedback_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("min-height: 30px;")
        main_layout.addWidget(self.feedback_label)

        # 计时器逻辑
        self.timer.timeout.connect(self.update_timer)

    def set_difficulty(self, difficulty: int):
        """设置游戏难度"""
        self.game.set_difficulty(difficulty)
        for i, btn in enumerate(self.difficulty_buttons):
            btn.setChecked(i + 1 == difficulty)

    def start_game(self):
        """开始游戏"""
        self.score = 0
        self.score_label.setText(f"当前分数: {self.score}")
        self.start_btn.setEnabled(False)
        self.submit_btn.setEnabled(True)
        self.next_btn.setEnabled(True)
        self.generate_new_question()
        self.achievement_system.update_stat("quickmath_games_played")

    def generate_new_question(self):
        """生成新题目"""
        self.time_left = 10  # 重置时间（简单难度10秒）
        self.timer_label.setText(f"剩余时间: {self.time_left}秒")
        self.answer_input.clear()
        self.feedback_label.setText("")

        # 生成题目
        question, _ = self.game.generate_question()
        self.question_label.setText(question)

        # 启动计时器
        self.timer.start(1000)  # 每秒刷新一次

    def update_timer(self):
        """更新计时器"""
        self.time_left -= 1
        self.timer_label.setText(f"剩余时间: {self.time_left}秒")

        if self.time_left <= 0:
            self.timer.stop()
            self.feedback_label.setText(f"时间到！正确答案是: {self.game.get_correct_answer()}")
            self.feedback_label.setStyleSheet("color: #e74c3c;")
            self.submit_btn.setEnabled(False)

    def check_answer(self):
        """检查答案"""
        if self.time_left <= 0:
            return

        self.timer.stop()
        user_answer = self.answer_input.text().strip()

        if not user_answer:
            self.feedback_label.setText("请输入答案！")
            self.feedback_label.setStyleSheet("color: #f39c12;")
            return

        if self.game.check_answer(user_answer):
            # 答案正确
            self.feedback_label.setText("正确！太棒了！")
            self.feedback_label.setStyleSheet("color: #2ecc71;")
            self.score += 10 * self.game.difficulty  # 分数与难度挂钩
            self.score_label.setText(f"当前分数: {self.score}")
            self.achievement_system.update_stat("quickmath_games_won")
        else:
            # 答案错误
            self.feedback_label.setText(f"不正确，正确答案是: {self.game.get_correct_answer()}")
            self.feedback_label.setStyleSheet("color: #e74c3c;")

        self.submit_btn.setEnabled(False)