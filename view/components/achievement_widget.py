from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QScrollArea,
                             QFrame, QGridLayout)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class AchievementWidget(QWidget):
    """成就展示组件"""
    back_to_calculator = QtCore.pyqtSignal()  # 返回计算器的信号

    def __init__(self, achievement_system):
        super().__init__()
        self.achievement_system = achievement_system
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)

        # 标题
        title_label = QLabel("我的成就")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 成就分类标签
        categories_layout = QHBoxLayout()

        calculator_btn = QPushButton("计算器")
        calculator_btn.setFont(QFont("Arial", 12))
        categories_layout.addWidget(calculator_btn)

        twentyfour_btn = QPushButton("二十四点")
        twentyfour_btn.setFont(QFont("Arial", 12))
        categories_layout.addWidget(twentyfour_btn)

        snake_btn = QPushButton("贪吃蛇")
        snake_btn.setFont(QFont("Arial", 12))
        categories_layout.addWidget(snake_btn)

        tetris_btn = QPushButton("俄罗斯方块")
        tetris_btn.setFont(QFont("Arial", 12))
        categories_layout.addWidget(tetris_btn)

        quickmath_btn = QPushButton("速算挑战")
        quickmath_btn.setFont(QFont("Arial", 12))
        categories_layout.addWidget(quickmath_btn)

        all_btn = QPushButton("全部")
        all_btn.setFont(QFont("Arial", 12))
        categories_layout.addWidget(all_btn)

        main_layout.addLayout(categories_layout)

        # 成就列表
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        achievements_container = QWidget()
        self.achievements_layout = QGridLayout(achievements_container)

        scroll_area.setWidget(achievements_container)
        main_layout.addWidget(scroll_area, 1)

        # 返回按钮
        back_btn = QPushButton("返回计算器")
        back_btn.setFont(QFont("Arial", 14))
        back_btn.clicked.connect(self.back_to_calculator.emit)
        main_layout.addWidget(back_btn)

        # 加载成就
        self.load_achievements()

    def load_achievements(self):
        """加载并显示所有成就，添加类型验证"""
        # 清除现有成就
        while self.achievements_layout.count():
            item = self.achievements_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 获取所有成就并确保是列表
        achievements = self.achievement_system.achievements
        if not isinstance(achievements, list):
            achievements = []

        row = 0
        col = 0

        for ach in achievements:
            # 验证成就项是否为字典且包含必要字段
            if not isinstance(ach, dict) or not all(key in ach for key in ["icon", "title", "description", "unlocked"]):
                continue  # 跳过无效的成就项

            # 创建成就卡片
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #f0f0f0;
                    border-radius: 8px;
                    padding: 10px;
                    margin: 5px;
                }
            """)
            card_layout = QVBoxLayout(card)

            # 成就图标和标题
            icon_label = QLabel(ach["icon"])
            icon_label.setFont(QFont("Arial", 24))
            icon_label.setAlignment(Qt.AlignCenter)

            title_label = QLabel(ach["title"])
            title_label.setFont(QFont("Arial", 14, QFont.Bold))
            title_label.setAlignment(Qt.AlignCenter)

            # 成就描述
            desc_label = QLabel(ach["description"])
            desc_label.setFont(QFont("Arial", 10))
            desc_label.setWordWrap(True)

            # 解锁状态
            status = "已解锁" if ach["unlocked"] else "未解锁"
            status_color = "#28a745" if ach["unlocked"] else "#6c757d"
            status_label = QLabel(status)
            status_label.setStyleSheet(f"color: {status_color};")
            status_label.setAlignment(Qt.AlignCenter)

            # 添加到卡片布局
            card_layout.addWidget(icon_label)
            card_layout.addWidget(title_label)
            card_layout.addWidget(desc_label)
            card_layout.addWidget(status_label)

            # 添加到网格布局
            self.achievements_layout.addWidget(card, row, col)

            # 控制网格布局的行列
            col += 1
            if col >= 3:
                col = 0
                row += 1
