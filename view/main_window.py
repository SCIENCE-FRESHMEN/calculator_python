from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QStackedWidget, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from .calculator_widget import CalculatorWidget
from .game_widgets import (TwentyFourGameWidget, SnakeGameWidget,
                           TetrisGameWidget, QuickMathGameWidget)
from view.components.achievement_widget import AchievementWidget


class MainWindow(QMainWindow):
    """应用程序主窗口"""

    def __init__(self, achievement_system):
        super().__init__()
        self.achievement_system = achievement_system
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)

        # 顶部标题
        title_label = QLabel("儿童益智计算器")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("margin: 10px 0px; color: #2c3e50;")
        main_layout.addWidget(title_label)

        # 创建堆叠窗口用于切换不同功能界面
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # 创建计算器界面
        self.calculator_widget = CalculatorWidget()
        self.calculator_widget.switch_to_game.connect(self.switch_to_game)
        self.stacked_widget.addWidget(self.calculator_widget)

        # 创建游戏界面
        self.game_widgets = {
            "二十四点": TwentyFourGameWidget(self.achievement_system),
            "贪吃蛇": SnakeGameWidget(self.achievement_system),
            "俄罗斯方块": TetrisGameWidget(self.achievement_system),
            "速算挑战": QuickMathGameWidget(self.achievement_system)
        }

        # 将游戏界面添加到堆叠窗口
        for game_name, widget in self.game_widgets.items():
            # 设置返回按钮的回调
            widget.back_to_calculator.connect(self.switch_to_calculator)
            self.stacked_widget.addWidget(widget)

        # 创建成就界面
        self.achievement_widget = AchievementWidget(self.achievement_system)
        self.achievement_widget.back_to_calculator.connect(self.switch_to_calculator)
        self.stacked_widget.addWidget(self.achievement_widget)

        # 底部导航栏
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(10, 10, 10, 10)

        # 计算器按钮
        self.calc_btn = QPushButton("计算器")
        self.calc_btn.setFont(QFont("Arial", 12))
        self.calc_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.calc_btn.clicked.connect(self.switch_to_calculator)
        nav_layout.addWidget(self.calc_btn)

        # 成就按钮
        self.achievement_btn = QPushButton("我的成就")
        self.achievement_btn.setFont(QFont("Arial", 12))
        self.achievement_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        self.achievement_btn.clicked.connect(self.switch_to_achievements)
        nav_layout.addWidget(self.achievement_btn)

        nav_layout.addStretch()

        main_layout.addLayout(nav_layout)

        # 默认显示计算器界面
        self.switch_to_calculator()

    def switch_to_calculator(self):
        """切换到计算器界面"""
        self.stacked_widget.setCurrentWidget(self.calculator_widget)
        self.setWindowTitle("儿童益智计算器 - 计算器")

    def switch_to_game(self, game_name: str):
        """
        切换到指定游戏界面

        参数:
            game_name: 游戏名称
        """
        if game_name in self.game_widgets:
            self.stacked_widget.setCurrentWidget(self.game_widgets[game_name])
            self.setWindowTitle(f"儿童益智计算器 - {game_name}")

    def switch_to_achievements(self):
        """切换到成就界面"""
        self.achievement_widget.update_achievements()
        self.stacked_widget.setCurrentWidget(self.achievement_widget)
        self.setWindowTitle("儿童益智计算器 - 我的成就")
