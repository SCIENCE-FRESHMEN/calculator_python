import sys
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow
from core.achievement_system import AchievementSystem
def main():
    import matplotlib
    matplotlib.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
    app = QApplication(sys.argv)
    achievement_system = AchievementSystem()
    window = MainWindow(achievement_system)
    window.setWindowTitle("儿童益智计算器")
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
