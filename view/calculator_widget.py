from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QGridLayout, QLabel, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QPixmap
from core.calculator_engine import CalculatorEngine


class CuteButton(QPushButton):
    """可爱风格的按钮（仅保留文本）"""

    def __init__(self, text: str, parent=None, color: str = "#FF99CC"):
        super().__init__(text, parent)
        self.original_color = color
        self.pressed_color = self.adjust_color(color, -30)
        self.hover_color = self.adjust_color(color, 30)

        # 按钮样式
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.original_color};
                color: white;
                border-radius: 20px;  # 圆润边角
                font-family: "Comic Sans MS", "Arial Rounded MT Bold";
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
                margin: 5px;
                border: 3px solid white;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
                transform: scale(1.05);  # 悬停放大
            }}
            QPushButton:pressed {{
                background-color: {self.pressed_color};
                transform: scale(0.95);  # 按下缩小
            }}
        """)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def adjust_color(self, color_hex: str, value: int) -> str:
        """调整颜色亮度"""
        r = int(color_hex[1:3], 16)
        g = int(color_hex[3:5], 16)
        b = int(color_hex[5:7], 16)

        r = max(0, min(255, r + value))
        g = max(0, min(255, g + value))
        b = max(0, min(255, b + value))

        return f"#{r:02x}{g:02x}{b:02x}"

    def animate_click(self):
        """按钮点击动画"""
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(200)
        original_geometry = self.geometry()

        animation.setKeyValues([
            (0, original_geometry),
            (0.3, QRect(original_geometry.x() + 3, original_geometry.y() + 3,
                        original_geometry.width() - 6, original_geometry.height() - 6)),
            (0.7, QRect(original_geometry.x() - 2, original_geometry.y() - 2,
                        original_geometry.width() + 4, original_geometry.height() + 4)),
            (1, original_geometry)
        ])
        animation.start()


class CalculatorWidget(QWidget):
    """儿童风格计算器界面（已删除历史记录模块）"""

    switch_to_game = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = CalculatorEngine()
        self.init_ui()

        # 背景样式
        self.setStyleSheet("""
            background-color: #FFF5F8;
            background-image: url(:/images/cute_pattern.png); 
            background-repeat: repeat;
        """)

    def init_ui(self):
        """初始化界面（移除历史记录区域）"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题区域
        title_container = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(QPixmap(":/icons/calculator.png").scaled(36, 36, Qt.KeepAspectRatio))
        title_container.addWidget(title_icon)

        title_label = QLabel("🐱 儿童益智计算器 🐰")
        title_label.setFont(QFont("Comic Sans MS", 22, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #FF6B8B; 
            margin: 10px 0px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        """)
        title_container.addWidget(title_label)
        title_container.addStretch()
        main_layout.addLayout(title_container)

        # 显示区域
        self.create_display_area(main_layout)

        # 按钮区域
        self.create_button_area(main_layout)

        # 游戏切换按钮（移至按钮区域下方）
        self.create_game_buttons(main_layout)

        self.setLayout(main_layout)
        self.setMinimumSize(450, 550)  # 调整最小高度（因删除历史记录区域）

    def create_display_area(self, parent_layout):
        """显示区域"""
        display_frame = QFrame()
        display_frame.setStyleSheet("""
            background-color: #E6F7FF;
            border-radius: 15px; 
            padding: 15px;
            border: 5px dashed #99D9EA;
            box-shadow: 0 6px 10px rgba(0,0,0,0.1);
        """)
        display_layout = QVBoxLayout(display_frame)

        # 表达式显示
        self.expression_display = QLineEdit()
        self.expression_display.setFont(QFont("Comic Sans MS", 16))
        self.expression_display.setAlignment(Qt.AlignRight)
        self.expression_display.setReadOnly(True)
        self.expression_display.setStyleSheet("""
            background-color: rgba(255,255,255,0.7);
            border-radius: 8px;
            padding: 10px;
            color: #555555;
            margin-bottom: 10px;
        """)
        display_layout.addWidget(self.expression_display)

        # 结果显示
        self.result_display = QLineEdit()
        self.result_display.setFont(QFont("Comic Sans MS", 28, QFont.Bold))
        self.result_display.setAlignment(Qt.AlignRight)
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("""
            background-color: rgba(255,255,255,0.9);
            border-radius: 8px;
            padding: 10px;
            color: #FF6B8B;
        """)
        display_layout.addWidget(self.result_display)

        parent_layout.addWidget(display_frame)

    def create_button_area(self, parent_layout):
        """按钮区域"""
        button_grid = QGridLayout()
        button_grid.setSpacing(8)

        # 按钮布局：(文本, 颜色, 行, 列, 行跨度, 列跨度)
        buttons = [
            ('C', "#FF6B6B", 0, 0, 1, 1),    # 红色清除键
            ('⌫', "#FFB86C", 0, 1, 1, 1),    # 橙色删除键
            ('^', "#8BE9FD", 0, 2, 1, 1),    # 浅蓝色幂运算
            ('√', "#8BE9FD", 0, 3, 1, 1),    # 浅蓝色根号

            ('7', "#50FA7B", 1, 0, 1, 1),    # 绿色数字
            ('8', "#50FA7B", 1, 1, 1, 1),
            ('9', "#50FA7B", 1, 2, 1, 1),
            ('÷', "#BD93F9", 1, 3, 1, 1),    # 紫色除法

            ('4', "#50FA7B", 2, 0, 1, 1),
            ('5', "#50FA7B", 2, 1, 1, 1),
            ('6', "#50FA7B", 2, 2, 1, 1),
            ('×', "#BD93F9", 2, 3, 1, 1),    # 紫色乘法

            ('1', "#50FA7B", 3, 0, 1, 1),
            ('2', "#50FA7B", 3, 1, 1, 1),
            ('3', "#50FA7B", 3, 2, 1, 1),
            ('-', "#BD93F9", 3, 3, 1, 1),    # 紫色减法

            ('0', "#50FA7B", 4, 0, 1, 2),
            ('.', "#FF79C6", 4, 2, 1, 1),    # 粉色小数点
            ('+', "#BD93F9", 4, 3, 1, 1),    # 紫色加法

            ('=', "#FF79C6", 5, 0, 1, 4),    # 粉色等号
        ]

        # 创建按钮并添加到网格
        for text, color, row, col, row_span, col_span in buttons:
            btn = CuteButton(text, color=color)
            btn.clicked.connect(lambda checked, t=text: self.on_button_clicked(t))
            button_grid.addWidget(btn, row, col, row_span, col_span)

        parent_layout.addLayout(button_grid)

    def create_game_buttons(self, parent_layout):
        """游戏切换按钮"""
        game_layout = QHBoxLayout()
        game_layout.setSpacing(10)

        games = [
            ("二十四点", "#BD93F9"),  # 紫色
            ("贪吃蛇", "#50FA7B"),    # 绿色
            ("俄罗斯方块", "#FFB86C"), # 橙色
            ("速算挑战", "#FF79C6")   # 粉色
        ]

        for game_name, color in games:
            btn = CuteButton(game_name, color=color)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border-radius: 15px;
                    font-family: "Comic Sans MS";
                    font-size: 16px;
                    padding: 10px;
                    margin: 5px;
                    border: 2px solid white;
                    box-shadow: 0 3px 5px rgba(0,0,0,0.1);
                }}
                QPushButton:hover {{
                    background-color: {self.adjust_color(color, 30)};
                    transform: scale(1.05);
                }}
                QPushButton:pressed {{
                    background-color: {self.adjust_color(color, -30)};
                    transform: scale(0.95);
                }}
            """)
            btn.clicked.connect(lambda checked, g=game_name: self.switch_to_game.emit(g))
            game_layout.addWidget(btn)

        parent_layout.addLayout(game_layout)

    def adjust_color(self, color_hex: str, value: int) -> str:
        """调整颜色亮度"""
        r = int(color_hex[1:3], 16)
        g = int(color_hex[3:5], 16)
        b = int(color_hex[5:7], 16)

        r = max(0, min(255, r + value))
        g = max(0, min(255, g + value))
        b = max(0, min(255, b + value))

        return f"#{r:02x}{g:02x}{b:02x}"

    def on_button_clicked(self, text: str):
        """按钮点击事件"""
        sender_btn = self.sender()
        if hasattr(sender_btn, 'animate_click'):
            sender_btn.animate_click()

        # 计算逻辑（移除历史记录相关调用）
        if text == '=':
            result, error = self.calculator.evaluate()
            if error:
                self.result_display.setText(f"❌ {error}")
            elif result is not None:
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.result_display.setText(f"✅ {result}")
        elif text == 'C':
            self.calculator.clear_expression()
            self.expression_display.clear()
            self.result_display.clear()
        elif text == '⌫':
            self.calculator.delete_last_char()
            self.expression_display.setText(self.calculator.current_expression)
        else:
            self.calculator.add_to_expression(text)
            self.expression_display.setText(self.calculator.current_expression)
            self.result_display.clear()