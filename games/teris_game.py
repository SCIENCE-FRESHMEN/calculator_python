import pygame
import random
import os
import json
from typing import List, Tuple, Dict, Optional, Set, Union
import time

# 初始化pygame
pygame.init()

# 游戏常量
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
DARK_BLUE = (0, 50, 150)
LIGHT_BLUE = (100, 180, 255)
GOLD = (255, 215, 0)

# 方块形状和颜色定义
SHAPES = {
    'I': [(0, -1), (0, 0), (0, 1), (0, 2)],
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
    'T': [(0, 0), (-1, 0), (1, 0), (0, 1)],
    'S': [(0, 0), (1, 0), (0, 1), (-1, 1)],
    'Z': [(0, 0), (-1, 0), (0, 1), (1, 1)],
    'J': [(0, 0), (0, 1), (0, -1), (-1, -1)],
    'L': [(0, 0), (0, 1), (0, -1), (1, -1)]
}

COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': MAGENTA,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}

# 游戏区域尺寸
GAME_AREA_WIDTH = GRID_WIDTH * CELL_SIZE
GAME_AREA_HEIGHT = GRID_HEIGHT * CELL_SIZE

# 侧边栏尺寸
SIDEBAR_WIDTH = 200
SIDEBAR_HEIGHT = GAME_AREA_HEIGHT

# 窗口尺寸
WINDOW_WIDTH = GAME_AREA_WIDTH + SIDEBAR_WIDTH
WINDOW_HEIGHT = GAME_AREA_HEIGHT

# 字体设置
pygame.font.init()
FONT_SMALL = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Arial"], 24)
FONT_MEDIUM = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Arial"], 36)
FONT_LARGE = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Arial"], 48)
FONT_XLARGE = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Arial"], 64)

# 墙壁踢（Wall Kick）数据 - 用于旋转时的位置调整
WALL_KICKS = {
    'I': [
        [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
        [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
        [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
        [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)]
    ],
    'default': [
        [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
        [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
        [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
        [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
    ]
}


class Button:
    """按钮类，用于创建交互按钮"""

    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.border_radius = 8  # 按钮圆角

    def draw(self, surface):
        # 绘制按钮背景
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=self.border_radius)

        # 绘制按钮文字
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Tetromino:
    """
    俄罗斯方块方块类，负责管理单个方块的形状、位置、旋转等操作
    """

    def __init__(self, shape_type: Optional[str] = None):
        """
        初始化方块

        Args:
            shape_type: 方块类型，如果为None则随机选择
        """
        if shape_type is None:
            self.shape_type = random.choice(list(SHAPES.keys()))
        else:
            self.shape_type = shape_type

        self.shape = SHAPES[self.shape_type]
        self.color = COLORS[self.shape_type]
        self.x = GRID_WIDTH // 2
        self.y = 0
        self.rotation_state = 0

    def get_rotated_shape(self, rotation_state: int) -> List[Tuple[int, int]]:
        """
        获取旋转后的方块形状

        Args:
            rotation_state: 旋转状态，0-3表示不同的旋转角度

        Returns:
            旋转后的方块形状坐标列表
        """
        rotated = []
        for dx, dy in self.shape:
            if self.shape_type == 'O':
                # O型方块旋转不变
                rotated.append((dx, dy))
            elif rotation_state == 1:
                # 顺时针旋转90度
                rotated.append((-dy, dx))
            elif rotation_state == 2:
                # 顺时针旋转180度
                rotated.append((-dx, -dy))
            elif rotation_state == 3:
                # 顺时针旋转270度
                rotated.append((dy, -dx))
            else:
                # 0度（初始状态）
                rotated.append((dx, dy))
        return rotated

    def rotate(self, clockwise: bool = True) -> None:
        """
        旋转方块

        Args:
            clockwise: 是否顺时针旋转
        """
        if clockwise:
            self.rotation_state = (self.rotation_state + 1) % 4
        else:
            self.rotation_state = (self.rotation_state - 1) % 4

    def get_current_shape(self) -> List[Tuple[int, int]]:
        """
        获取当前旋转状态下的方块形状

        Returns:
            当前形状的坐标列表
        """
        return self.get_rotated_shape(self.rotation_state)

    def get_blocks(self) -> List[Tuple[int, int]]:
        """
        获取方块在游戏板上的绝对坐标

        Returns:
            方块各块的绝对坐标列表
        """
        return [(self.x + dx, self.y + dy) for dx, dy in self.get_current_shape()]

    def try_wall_kick(self, game_board: 'GameBoard', clockwise: bool = True) -> Tuple[int, int]:
        """
        尝试墙壁踢（Wall Kick）调整

        Args:
            game_board: 游戏板对象
            clockwise: 是否顺时针旋转

        Returns:
            调整的x和y偏移量，如果不需要调整则返回(0, 0)
        """
        original_rotation = self.rotation_state

        # 先尝试旋转
        if clockwise:
            new_rotation = (original_rotation + 1) % 4
        else:
            new_rotation = (original_rotation - 1) % 4

        # 获取适用的墙壁踢数据
        if self.shape_type == 'I':
            kicks = WALL_KICKS['I']
        else:
            kicks = WALL_KICKS['default']

        # 确定踢动数据的索引
        from_state = original_rotation
        to_state = new_rotation

        # 尝试各种踢动位置
        for dx, dy in kicks[from_state]:
            # 保存当前位置
            original_x, original_y = self.x, self.y

            # 应用踢动
            self.x += dx
            self.y += dy

            # 临时应用旋转
            self.rotation_state = new_rotation

            # 检查是否碰撞
            if not game_board.check_collision(self):
                # 没有碰撞，保留这个位置和旋转状态
                return (dx, dy)

            # 恢复位置和旋转状态
            self.x, self.y = original_x, original_y
            self.rotation_state = original_rotation

        # 所有踢动都失败，返回(0, 0)表示无法旋转
        return (0, 0)

    def __repr__(self) -> str:
        return f"Tetromino(shape_type={self.shape_type}, x={self.x}, y={self.y}, rotation={self.rotation_state})"


class GameBoard:
    """
    游戏板类，负责管理游戏区域的状态和逻辑
    """

    def __init__(self, width: int, height: int):
        """
        初始化游戏板

        Args:
            width: 游戏板宽度（列数）
            height: 游戏板高度（行数）
        """
        self.width = width
        self.height = height
        self.reset()

    def reset(self) -> None:
        """重置游戏板为初始状态"""
        # 创建空的游戏板，每个单元格为None表示空，否则存储颜色
        self.grid: List[List[Optional[Tuple[int, int, int]]]] = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]
        self.cleared_lines = 0

    def check_collision(self, tetromino: Tetromino) -> bool:
        """
        检查方块是否与游戏板边界或已有方块碰撞

        Args:
            tetromino: 要检查的方块

        Returns:
            如果碰撞则返回True，否则返回False
        """
        for x, y in tetromino.get_blocks():
            # 检查是否超出边界
            if x < 0 or x >= self.width or y >= self.height:
                return True
            # 检查是否与已有方块碰撞（忽略y < 0的情况，允许方块从顶部出现）
            if y >= 0 and self.grid[y][x] is not None:
                return True
        return False

    def lock_tetromino(self, tetromino: Tetromino) -> bool:
        """
        将方块锁定在游戏板上

        Args:
            tetromino: 要锁定的方块

        Returns:
            如果成功锁定返回True，如果方块顶部超出游戏区域则返回False（游戏结束）
        """
        for x, y in tetromino.get_blocks():
            if y < 0:
                # 方块顶部超出游戏区域，游戏结束
                return False
            self.grid[y][x] = tetromino.color
        return True

    def clear_lines(self) -> int:
        """
        清除已满的行并返回清除的行数

        Returns:
            清除的行数
        """
        lines_cleared = 0
        new_grid = []

        for row in self.grid:
            if all(cell is not None for cell in row):
                # 这一行已满，不添加到新网格中
                lines_cleared += 1
            else:
                # 这一行未满，添加到新网格中
                new_grid.append(row)

        # 在顶部添加与清除行数相等的空行
        for _ in range(lines_cleared):
            new_grid.insert(0, [None for _ in range(self.width)])

        self.grid = new_grid
        self.cleared_lines += lines_cleared
        return lines_cleared

    def get_ghost_position(self, tetromino: Tetromino) -> int:
        """
        计算方块的幽灵位置（即方块下落到底部的y坐标）

        Args:
            tetromino: 要计算的方块

        Returns:
            幽灵方块的y坐标
        """
        original_y = tetromino.y
        drop_distance = 0

        # 尝试下落，直到碰撞
        while True:
            tetromino.y += 1
            if self.check_collision(tetromino):
                tetromino.y = original_y
                return original_y + drop_distance
            drop_distance += 1

    def is_row_completed(self, row: int) -> bool:
        """
        检查指定行是否已满

        Args:
            row: 行索引

        Returns:
            如果行已满则返回True，否则返回False
        """
        return all(cell is not None for cell in self.grid[row])

    def __repr__(self) -> str:
        return f"GameBoard(width={self.width}, height={self.height}, cleared_lines={self.cleared_lines})"


class ScoreSystem:
    """
    计分系统类，负责计算和管理游戏分数
    """

    def __init__(self):
        """初始化计分系统"""
        self.score = 0
        self.combo = 0
        self.level = 1
        self.lines_cleared = 0
        self.high_score = self.load_high_score()

    def add_line_clear_score(self, lines: int) -> None:
        """
        添加消除行的分数

        Args:
            lines: 消除的行数
        """
        if lines == 0:
            self.combo = 0
            return

        # 基础分数
        line_scores = {1: 100, 2: 300, 3: 500, 4: 800}
        base_score = line_scores.get(lines, 0)

        # 计算 combo 加成（每连续消除一次增加10%，最高100%）
        combo_multiplier = 1 + min(self.combo, 10) * 0.1

        # 计算总分（受当前等级影响）
        total_score = int(base_score * self.level * combo_multiplier)
        self.score += total_score

        # 更新 combo 和消除的总行数
        self.combo += 1
        self.lines_cleared += lines

        # 每消除10行提升一级
        self.level = max(1, self.lines_cleared // 10 + 1)

        # 更新最高分
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def add_soft_drop_score(self, distance: int) -> None:
        """
        添加软降分数

        Args:
            distance: 软降的距离
        """
        self.score += distance
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def add_hard_drop_score(self, distance: int) -> None:
        """
        添加硬降分数

        Args:
            distance: 硬降的距离
        """
        self.score += distance * 2
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def reset(self) -> None:
        """重置分数系统"""
        self.score = 0
        self.combo = 0
        self.level = 1
        self.lines_cleared = 0

    def load_high_score(self) -> int:
        """
        从文件加载最高分

        Returns:
            最高分，如果文件不存在则返回0
        """
        try:
            if os.path.exists('high_score.json'):
                with open('high_score.json', 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
            return 0
        except Exception as e:
            print(f"Error loading high score: {e}")
            return 0

    def save_high_score(self) -> None:
        """将最高分保存到文件"""
        try:
            with open('high_score.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except Exception as e:
            print(f"Error saving high score: {e}")

    def __repr__(self) -> str:
        return f"ScoreSystem(score={self.score}, level={self.level}, lines_cleared={self.lines_cleared}, high_score={self.high_score})"


class GameEngine:
    """
    游戏引擎类，负责控制游戏流程和逻辑
    """

    def __init__(self, width: int, height: int):
        """
        初始化游戏引擎

        Args:
            width: 游戏板宽度
            height: 游戏板高度
        """
        self.board = GameBoard(width, height)
        self.score_system = ScoreSystem()

        self.current_tetromino: Optional[Tetromino] = None
        self.next_tetromino = Tetromino()
        self.hold_tetromino: Optional[Tetromino] = None
        self.can_hold = True

        self.game_over = False
        self.paused = False
        self.need_check = True  # 添加验证状态

        self.fall_time = 0
        self.fall_speed = self.get_fall_speed()
        self.last_fall_time = pygame.time.get_ticks()

        self.clear_line_animation = False
        self.clear_line_timer = 0
        self.cleared_lines: Set[int] = set()

        self.spawn_new_tetromino()

    def get_fall_speed(self) -> float:
        """
        根据当前等级获取下落速度（秒/格）

        Returns:
            下落速度
        """
        # 等级越高，下落速度越快
        speeds = [
            0.3, 0.27, 0.24, 0.21, 0.18,  # 1-5级
            0.15, 0.12, 0.09, 0.06, 0.045,  # 6-10级
            0.03, 0.027, 0.024, 0.021, 0.018,  # 11-15级
            0.015, 0.012, 0.009, 0.006, 0.003  # 16-20级
        ]
        level = self.score_system.level
        return speeds[min(level - 1, len(speeds) - 1)]

    def spawn_new_tetromino(self) -> bool:
        """
        生成新的方块

        Returns:
            如果成功生成返回True，如果游戏结束返回False
        """
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = Tetromino()
        self.can_hold = True

        # 检查新生成的方块是否立即碰撞
        if self.board.check_collision(self.current_tetromino):
            self.game_over = True
            return False
        return True

    def hold(self) -> None:
        """保存当前方块并取出已保存的方块（如果有的话）"""
        if not self.can_hold or self.game_over or self.paused:
            return

        if self.hold_tetromino is None:
            self.hold_tetromino = self.current_tetromino
            self.spawn_new_tetromino()
        else:
            # 交换当前方块和保存的方块
            temp = self.current_tetromino
            self.current_tetromino = self.hold_tetromino
            # 重置位置和旋转状态
            self.current_tetromino.x = self.board.width // 2
            self.current_tetromino.y = 0
            self.current_tetromino.rotation_state = 0
            self.hold_tetromino = temp

        self.can_hold = False

    def move(self, dx: int, dy: int) -> bool:
        """
        移动方块

        Args:
            dx: x方向移动量
            dy: y方向移动量

        Returns:
            如果移动成功返回True，否则返回False
        """
        if self.current_tetromino is None or self.game_over or self.paused or self.clear_line_animation or self.need_check:
            return False

        # 保存当前位置
        original_x = self.current_tetromino.x
        original_y = self.current_tetromino.y

        # 尝试移动
        self.current_tetromino.x += dx
        self.current_tetromino.y += dy

        # 检查碰撞
        if self.board.check_collision(self.current_tetromino):
            # 碰撞，恢复位置
            self.current_tetromino.x = original_x
            self.current_tetromino.y = original_y
            return False

        # 移动成功
        return True

    def rotate(self, clockwise: bool = True) -> bool:
        """
        旋转方块

        Args:
            clockwise: 是否顺时针旋转

        Returns:
            如果旋转成功返回True，否则返回False
        """
        if self.current_tetromino is None or self.game_over or self.paused or self.clear_line_animation or self.need_check:
            return False

        # 尝试墙壁踢
        dx, dy = self.current_tetromino.try_wall_kick(self.board, clockwise)

        if dx != 0 or dy != 0:
            # 墙壁踢成功
            return True
        else:
            # 墙壁踢失败，无法旋转
            return False

    def soft_drop(self) -> bool:
        """
        软降方块（向下移动一格）

        Returns:
            如果移动成功返回True，否则返回False
        """
        if self.move(0, 1):
            self.score_system.add_soft_drop_score(1)
            return True
        return False

    def hard_drop(self) -> int:
        """
        硬降方块（直接下落到最底部）

        Returns:
            下落的距离
        """
        if self.current_tetromino is None or self.game_over or self.paused or self.clear_line_animation or self.need_check:
            return 0

        original_y = self.current_tetromino.y
        drop_distance = 0

        # 一直下落直到碰撞
        while self.move(0, 1):
            drop_distance += 1

        # 锁定方块
        if drop_distance > 0:
            self.lock_current_tetromino()
            self.score_system.add_hard_drop_score(drop_distance)

        return drop_distance

    def lock_current_tetromino(self) -> None:
        """锁定当前方块并检查是否需要消除行"""
        if self.current_tetromino is None:
            return

        # 锁定方块
        success = self.board.lock_tetromino(self.current_tetromino)
        if not success:
            self.game_over = True
            return

        # 检查并清除已满的行
        lines_cleared = self.board.clear_lines()
        if lines_cleared > 0:
            self.score_system.add_line_clear_score(lines_cleared)
            # 准备行消除动画
            self.clear_line_animation = True
            self.clear_line_timer = pygame.time.get_ticks()
            # 记录被消除的行
            self.cleared_lines = set()
            # 检测哪些行被消除（简化版）
            for y in range(self.board.height):
                if self.board.is_row_completed(y):
                    self.cleared_lines.add(y)
        else:
            # 没有消除行，直接生成新方块
            self.spawn_new_tetromino()

    def update(self) -> None:
        """更新游戏状态"""
        if self.game_over or self.paused or self.need_check:
            return

        current_time = pygame.time.get_ticks()

        # 处理行消除动画
        if self.clear_line_animation:
            # 动画持续300毫秒
            if current_time - self.clear_line_timer > 300:
                self.clear_line_animation = False
                self.spawn_new_tetromino()
            return

        # 自动下落
        if current_time - self.last_fall_time > self.fall_speed * 1000:
            if not self.soft_drop():
                # 无法下落，锁定方块
                self.lock_current_tetromino()
            self.last_fall_time = current_time
            # 更新下落速度（可能因等级提升而改变）
            self.fall_speed = self.get_fall_speed()

    def toggle_pause(self) -> None:
        """切换游戏暂停状态"""
        if not self.game_over and not self.need_check:
            self.paused = not self.paused

    def reset(self) -> None:
        """重置游戏"""
        self.board.reset()
        self.score_system.reset()
        self.current_tetromino = None
        self.next_tetromino = Tetromino()
        self.hold_tetromino = None
        self.can_hold = True
        self.game_over = False
        self.paused = False
        self.need_check = True  # 重置时重新显示验证界面
        self.fall_time = 0
        self.fall_speed = self.get_fall_speed()
        self.last_fall_time = pygame.time.get_ticks()
        self.clear_line_animation = False
        self.clear_line_timer = 0
        self.cleared_lines = set()
        self.spawn_new_tetromino()

    def handle_input(self, key: int) -> None:
        """
        处理用户输入

        Args:
            key: 按键代码
        """
        # 验证状态下的输入处理
        if self.need_check:
            if key == pygame.K_SPACE:
                self.need_check = False
            return

        if self.game_over:
            if key == pygame.K_r:
                self.reset()
            return

        if key == pygame.K_p:
            self.toggle_pause()
            return

        if self.paused or self.clear_line_animation:
            return

        if key == pygame.K_LEFT:
            self.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.move(1, 0)
        elif key == pygame.K_DOWN:
            self.soft_drop()
        elif key == pygame.K_UP:
            self.rotate()
        elif key == pygame.K_SPACE:
            self.hard_drop()
        elif key == pygame.K_c:
            self.hold()

    def __repr__(self) -> str:
        return f"GameEngine(game_over={self.game_over}, paused={self.paused}, level={self.score_system.level})"


class Renderer:
    """
    渲染器类，负责游戏的图形渲染
    """

    def __init__(self, engine: GameEngine, width: int, height: int, sidebar_width: int):
        """
        初始化渲染器

        Args:
            engine: 游戏引擎对象
            width: 游戏区域宽度
            height: 游戏区域高度
            sidebar_width: 侧边栏宽度
        """
        self.engine = engine
        self.game_width = width
        self.game_height = height
        self.sidebar_width = sidebar_width
        self.window_width = width + sidebar_width
        self.window_height = height

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("俄罗斯方块")

        self.clock = pygame.time.Clock()

        # 创建验证按钮
        self._create_check_button()

    def _create_check_button(self):
        """创建验证界面的按钮"""
        button_width = 180
        button_height = 60
        x = self.window_width // 2 - button_width // 2
        y = self.window_height // 2 + 60
        self.check_button = Button(
            x, y, button_width, button_height,
            "已完成挑战", FONT_MEDIUM,
            BLUE, LIGHT_BLUE, WHITE
        )

    def draw_cell(self, x: int, y: int, color: Tuple[int, int, int],
                  x_offset: int = 0, y_offset: int = 0, alpha: int = 255) -> None:
        """
        绘制单个方块

        Args:
            x: 网格x坐标
            y: 网格y坐标
            color: 方块颜色
            x_offset: x方向偏移量（像素）
            y_offset: y方向偏移量（像素）
            alpha: 透明度（0-255）
        """
        rect = pygame.Rect(
            x * CELL_SIZE + x_offset,
            y * CELL_SIZE + y_offset,
            CELL_SIZE - 1,  # 减1是为了留出网格线的空间
            CELL_SIZE - 1
        )

        # 如果需要透明效果，创建一个临时表面
        if alpha != 255:
            s = pygame.Surface((CELL_SIZE - 1, CELL_SIZE - 1), pygame.SRCALPHA)
            s.fill((*color, alpha))
            self.screen.blit(s, rect)
        else:
            pygame.draw.rect(self.screen, color, rect)

    def draw_tetromino(self, tetromino: Tetromino, x_offset: int = 0, y_offset: int = 0,
                       alpha: int = 255, ghost: bool = False) -> None:
        """
        绘制方块

        Args:
            tetromino: 要绘制的方块
            x_offset: x方向偏移量（像素）
            y_offset: y方向偏移量（像素）
            alpha: 透明度（0-255）
            ghost: 是否绘制为幽灵方块（半透明灰色）
        """
        for x, y in tetromino.get_blocks():
            # 只绘制可见的部分
            if y >= 0:
                color = GRAY if ghost else tetromino.color
                self.draw_cell(x, y, color, x_offset, y_offset, alpha)

    def draw_ghost_tetromino(self, tetromino: Tetromino) -> None:
        """
        绘制幽灵方块（显示方块下落到底部的位置）

        Args:
            tetromino: 要绘制幽灵的方块
        """
        if tetromino is None:
            return

        original_y = tetromino.y
        ghost_y = self.engine.board.get_ghost_position(tetromino)

        # 保存原始y坐标，绘制幽灵后恢复
        tetromino.y = ghost_y
        self.draw_tetromino(tetromino, alpha=100, ghost=True)
        tetromino.y = original_y

    def draw_board(self) -> None:
        """绘制游戏板"""
        # 绘制背景
        self.screen.fill(BLACK)

        # 绘制已锁定的方块
        for y, row in enumerate(self.engine.board.grid):
            for x, color in enumerate(row):
                if color is not None:
                    # 行消除动画效果
                    if self.engine.clear_line_animation and y in self.engine.cleared_lines:
                        # 闪烁效果：根据时间交替显示和隐藏
                        current_time = pygame.time.get_ticks()
                        if (current_time - self.engine.clear_line_timer) % 100 < 50:
                            self.draw_cell(x, y, WHITE)
                    else:
                        self.draw_cell(x, y, color)

        # 绘制当前方块
        if self.engine.current_tetromino is not None and not self.engine.game_over:
            # 先绘制幽灵方块
            self.draw_ghost_tetromino(self.engine.current_tetromino)
            # 再绘制实际方块
            self.draw_tetromino(self.engine.current_tetromino)

    def draw_sidebar(self) -> None:
        """绘制侧边栏（分数、下一个方块、保持区域等）"""
        sidebar_x = self.game_width
        sidebar_y = 0

        # 绘制侧边栏背景
        pygame.draw.rect(
            self.screen,
            LIGHT_GRAY,
            (sidebar_x, sidebar_y, self.sidebar_width, self.window_height)
        )

        # 绘制分数
        score_text = FONT_MEDIUM.render(f"分数: {self.engine.score_system.score}", True, BLACK)
        self.screen.blit(score_text, (sidebar_x + 10, 20))

        # 绘制等级
        level_text = FONT_MEDIUM.render(f"等级: {self.engine.score_system.level}", True, BLACK)
        self.screen.blit(level_text, (sidebar_x + 10, 60))

        # 绘制消除的行数
        lines_text = FONT_MEDIUM.render(f"行数: {self.engine.score_system.lines_cleared}", True, BLACK)
        self.screen.blit(lines_text, (sidebar_x + 10, 100))

        # 绘制最高分
        high_score_text = FONT_MEDIUM.render(f"最高分: {self.engine.score_system.high_score}", True, BLACK)
        self.screen.blit(high_score_text, (sidebar_x + 10, 140))

        # 绘制下一个方块标题
        next_text = FONT_SMALL.render("下一个:", True, BLACK)
        self.screen.blit(next_text, (sidebar_x + 10, 200))

        # 绘制下一个方块
        if self.engine.next_tetromino is not None:
            # 调整位置使方块居中显示
            self.draw_tetromino(
                self.engine.next_tetromino,
                x_offset=sidebar_x + 70,
                y_offset=230
            )

        # 绘制保持区域标题
        hold_text = FONT_SMALL.render("保持 (C):", True, BLACK)
        self.screen.blit(hold_text, (sidebar_x + 10, 350))

        # 绘制保持的方块
        if self.engine.hold_tetromino is not None:
            # 调整位置使方块居中显示
            self.draw_tetromino(
                self.engine.hold_tetromino,
                x_offset=sidebar_x + 70,
                y_offset=380
            )

        # 绘制操作说明
        controls_y = 500
        control_texts = [
            "左/右: 移动",
            "上: 旋转",
            "下: 加速下落",
            "空格: 硬降",
            "P: 暂停",
            "R: 重新开始"
        ]

        for text in control_texts:
            control_surface = FONT_SMALL.render(text, True, BLACK)
            self.screen.blit(control_surface, (sidebar_x + 10, controls_y))
            controls_y += 30

    def draw_game_over(self) -> None:
        """绘制游戏结束画面"""
        # 创建半透明遮罩
        s = pygame.Surface((self.game_width, self.game_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (0, 0))

        # 绘制游戏结束文本
        game_over_text = FONT_LARGE.render("游戏结束", True, WHITE)
        restart_text = FONT_MEDIUM.render("按R重新开始", True, WHITE)

        text_x = self.game_width // 2 - game_over_text.get_width() // 2
        text_y = self.game_height // 2 - 50
        self.screen.blit(game_over_text, (text_x, text_y))

        text_x = self.game_width // 2 - restart_text.get_width() // 2
        text_y = self.game_height // 2 + 50
        self.screen.blit(restart_text, (text_x, text_y))

    def draw_paused(self) -> None:
        """绘制暂停画面"""
        # 创建半透明遮罩
        s = pygame.Surface((self.game_width, self.game_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (0, 0))

        # 绘制暂停文本
        paused_text = FONT_LARGE.render("已暂停", True, WHITE)
        continue_text = FONT_MEDIUM.render("按P继续", True, WHITE)

        text_x = self.game_width // 2 - paused_text.get_width() // 2
        text_y = self.game_height // 2 - 50
        self.screen.blit(paused_text, (text_x, text_y))

        text_x = self.game_width // 2 - continue_text.get_width() // 2
        text_y = self.game_height // 2 + 50
        self.screen.blit(continue_text, (text_x, text_y))

    def draw_check_screen(self):
        """绘制验证挑战界面"""
        # 绘制渐变背景
        for y in range(self.window_height):
            color = (0, 0, int(50 + y * 200 / self.window_height))
            pygame.draw.line(self.screen, color, (0, y), (self.window_width, y))

        # 绘制标题
        title_text = FONT_XLARGE.render("挑战验证", True, GOLD)
        title_rect = title_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 120))
        # 添加文字阴影
        shadow_rect = title_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        self.screen.blit(FONT_XLARGE.render("挑战验证", True, (50, 50, 100)), shadow_rect)
        self.screen.blit(title_text, title_rect)

        # 绘制提示文字
        prompt_lines = [
            "请先完成以下任一项挑战：",
            "1. 五次二十四点游戏",
            "2. 十次速算挑战"
        ]

        # 计算文本总高度
        total_height = len(prompt_lines) * 35
        start_y = self.window_height // 2 - total_height // 2

        for i, line in enumerate(prompt_lines):
            text = FONT_MEDIUM.render(line, True, WHITE)
            text_rect = text.get_rect(center=(self.window_width // 2, start_y + i * 35))
            # 添加轻微阴影
            shadow_rect = text_rect.copy()
            shadow_rect.x += 1
            shadow_rect.y += 1
            self.screen.blit(FONT_MEDIUM.render(line, True, (100, 100, 150)), shadow_rect)
            self.screen.blit(text, text_rect)

        # 绘制按钮
        self.check_button.draw(self.screen)

        # 绘制操作提示
        hint_text = FONT_SMALL.render("或按空格键继续游戏", True, (200, 200, 255))
        hint_rect = hint_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 140))
        self.screen.blit(hint_text, hint_rect)

    def render(self) -> None:
        """渲染游戏画面"""
        # 如果需要验证，绘制验证界面
        if self.engine.need_check:
            self.draw_check_screen()
        else:
            # 绘制游戏板
            self.draw_board()

            # 绘制侧边栏
            self.draw_sidebar()

            # 如果游戏结束，绘制游戏结束画面
            if self.engine.game_over:
                self.draw_game_over()

            # 如果暂停，绘制暂停画面
            if self.engine.paused:
                self.draw_paused()

        # 更新显示
        pygame.display.flip()

        # 控制帧率
        self.clock.tick(FPS)


def main():
    """游戏主函数"""
    # 创建游戏引擎
    engine = GameEngine(GRID_WIDTH, GRID_HEIGHT)

    # 创建渲染器
    renderer = Renderer(engine, GAME_AREA_WIDTH, GAME_AREA_HEIGHT, SIDEBAR_WIDTH)

    # 游戏主循环
    running = True
    while running:
        # 处理事件
        mouse_pos = pygame.mouse.get_pos()

        # 更新按钮悬停状态
        if engine.need_check:
            renderer.check_button.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                engine.handle_input(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    if engine.need_check and renderer.check_button.is_clicked(mouse_pos):
                        engine.need_check = False

        # 更新游戏状态
        engine.update()

        # 渲染游戏画面
        renderer.render()

    # 退出游戏
    pygame.quit()


if __name__ == "__main__":
    main()