import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    """应用程序配置"""
    # 应用基本信息
    APP_NAME: str = "儿童益智计算器"
    VERSION: str = "1.0.0"
    AUTHOR: str = "儿童教育软件团队"

    # 路径配置
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    RESOURCES_DIR: str = os.path.join(BASE_DIR, "resources")
    IMAGES_DIR: str = os.path.join(RESOURCES_DIR, "images")
    SOUNDS_DIR: str = os.path.join(RESOURCES_DIR, "sounds")

    # 窗口配置
    MIN_WIDTH: int = 800
    MIN_HEIGHT: int = 600
    DEFAULT_FONT: str = "Arial"

    # 游戏配置
    SNAKE_INITIAL_SPEED: float = 0.5  # 初始速度（秒/步）
    SNAKE_MAX_SPEED: float = 0.1  # 最大速度（秒/步）
    QUICK_MATH_TIME_LIMIT: int = 60  # 速算挑战时间限制（秒）
    TETRIS_INITIAL_SPEED: float = 1.0  # 俄罗斯方块初始下落速度（秒/步）

    # 成就配置
    ACHIEVEMENT_UNLOCK_SOUND: str = os.path.join(SOUNDS_DIR, "unlock.wav")

    def ensure_directories(self) -> None:
        """确保所有必要的目录存在"""
        for dir_path in [self.DATA_DIR, self.RESOURCES_DIR,
                         self.IMAGES_DIR, self.SOUNDS_DIR]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)


# 创建配置实例
config = AppConfig()
# 确保目录存在
config.ensure_directories()
