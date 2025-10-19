import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏常量
GRID_SIZE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 180, 255)
GOLD = (255, 215, 0)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 速度设置
SPEED_LEVELS = {'简单': 8, '中等': 12, '困难': 18}
LEVEL_UP_SCORE = 100


class Snake:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.reset()

    def reset(self):
        center_x = (self.grid_width // 2) * GRID_SIZE
        center_y = (self.grid_height // 2) * GRID_SIZE
        self.length = 3
        self.positions = [(center_x, center_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.color = GREEN
        self.head_color = DARK_GREEN

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction

    def move(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        self.length += 1

    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            color = self.head_color if i == 0 else self.color
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)


class Food:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = (0, 0)
        self.color = RED
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        while True:
            x = random.randint(0, self.grid_width - 1) * GRID_SIZE
            y = random.randint(0, self.grid_height - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in snake_positions:
                break

    def draw(self, surface):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


class Button:
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


class SnakeGame:
    def __init__(self, width=40, height=30):
        self.grid_width = width
        self.grid_height = height
        self.window_width = width * GRID_SIZE
        self.window_height = height * GRID_SIZE
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("贪吃蛇游戏")

        self.snake = Snake(width, height)
        self.food = Food(width, height)
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.speed_level = '中等'
        self.speed = SPEED_LEVELS[self.speed_level]
        self.frame_counter = 0
        self.clock = pygame.time.Clock()
        self._load_fonts()

        # 新增检验状态和按钮
        self.need_check = True  # 是否需要显示检验提示
        self._create_check_button()

    def _load_fonts(self):
        try:
            # 增加不同大小的字体用于层次显示
            self.title_font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Arial"], 40)
            self.subtitle_font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Arial"], 28)
            self.normal_font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Arial"], 24)
            self.small_font = pygame.font.SysFont(["SimHei", "WenQuanYi Micro Hei", "Arial"], 18)
        except:
            self.title_font = pygame.font.Font(None, 40)
            self.subtitle_font = pygame.font.Font(None, 28)
            self.normal_font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)

    def _create_check_button(self):
        button_width = 180
        button_height = 60
        x = self.window_width // 2 - button_width // 2
        y = self.window_height // 2 + 60
        self.check_button = Button(
            x, y, button_width, button_height,
            "已完成挑战", self.subtitle_font,
            BLUE, LIGHT_BLUE, WHITE
        )

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        # 更新按钮悬停状态
        if self.need_check:
            self.check_button.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.need_check:
                    # 检验状态下只响应空格键跳过
                    if event.key == pygame.K_SPACE:
                        self.need_check = False
                elif self.game_over:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        levels = ['简单', '中等', '困难']
                        self.speed_level = levels[event.key - pygame.K_1]
                        self.speed = SPEED_LEVELS[self.speed_level]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    if self.need_check and self.check_button.is_clicked(mouse_pos):
                        self.need_check = False

    def check_level_up(self):
        new_level = (self.score // LEVEL_UP_SCORE) + 1
        if new_level > self.level:
            self.level = new_level
            if self.level % 3 == 0:
                current_idx = list(SPEED_LEVELS.values()).index(self.speed)
                if current_idx < len(SPEED_LEVELS) - 1:
                    self.speed = list(SPEED_LEVELS.values())[current_idx + 1]
                    self.speed_level = list(SPEED_LEVELS.keys())[current_idx + 1]

    def check_collisions(self):
        head = self.snake.positions[0]
        if (head[0] < 0 or head[0] >= self.window_width or
                head[1] < 0 or head[1] >= self.window_height):
            self.game_over = True

        for segment in self.snake.positions[1:]:
            if head == segment:
                self.game_over = True

        if head == self.food.position:
            self.snake.grow()
            self.score += 10
            self.check_level_up()
            self.food.randomize_position(self.snake.positions)

    def update(self):
        if not self.need_check and not self.game_over and not self.paused:
            self.frame_counter += 1
            if self.frame_counter >= (60 // self.speed):
                self.snake.move()
                self.check_collisions()
                self.frame_counter = 0

    def draw_check_screen(self):
        # 绘制渐变背景
        for y in range(self.window_height):
            color = (0, 0, int(50 + y * 200 / self.window_height))
            pygame.draw.line(self.window, color, (0, y), (self.window_width, y))

        # 绘制标题
        title_text = self.title_font.render("挑战验证", True, GOLD)
        title_rect = title_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 120))
        # 添加文字阴影
        shadow_rect = title_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        self.window.blit(self.title_font.render("挑战验证", True, (50, 50, 100)), shadow_rect)
        self.window.blit(title_text, title_rect)

        # 绘制提示文字（使用更清晰的排版）
        prompt_lines = [
            "请先完成以下任一项挑战：",
            "1. 五次二十四点游戏",
            "2. 十次速算挑战"
        ]

        # 计算文本总高度
        total_height = len(prompt_lines) * 35
        start_y = self.window_height // 2 - total_height // 2

        for i, line in enumerate(prompt_lines):
            text = self.subtitle_font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(self.window_width // 2, start_y + i * 35))
            # 添加轻微阴影
            shadow_rect = text_rect.copy()
            shadow_rect.x += 1
            shadow_rect.y += 1
            self.window.blit(self.subtitle_font.render(line, True, (100, 100, 150)), shadow_rect)
            self.window.blit(text, text_rect)

        # 绘制按钮
        self.check_button.draw(self.window)

        # 绘制操作提示
        hint_text = self.small_font.render("或按空格键继续游戏", True, (200, 200, 255))
        hint_rect = hint_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 140))
        self.window.blit(hint_text, hint_rect)

    def draw(self):
        if self.need_check:
            self.draw_check_screen()
        else:
            self.window.fill(BLACK)
            if not self.game_over:
                self.snake.draw(self.window)
                self.food.draw(self.window)

                score_text = self.normal_font.render(f"分数: {self.score}", True, WHITE)
                self.window.blit(score_text, (10, 10))

                level_text = self.normal_font.render(f"等级: {self.level}", True, WHITE)
                self.window.blit(level_text, (10, 40))

                speed_text = self.normal_font.render(f"难度: {self.speed_level}", True, WHITE)
                self.window.blit(speed_text, (self.window_width - 150, 10))

                if self.paused:
                    pause_text = self.title_font.render("暂停中", True, WHITE)
                    self.window.blit(pause_text,
                                     (self.window_width // 2 - 80, self.window_height // 2 - 24))
            else:
                over_text = self.title_font.render("游戏结束", True, RED)
                score_text = self.normal_font.render(f"最终分数: {self.score}", True, WHITE)
                restart_text = self.normal_font.render("按 R 重新开始，按 Q 退出", True, WHITE)

                self.window.blit(over_text,
                                 (self.window_width // 2 - 120, self.window_height // 2 - 80))
                self.window.blit(score_text,
                                 (self.window_width // 2 - 80, self.window_height // 2 - 30))
                self.window.blit(restart_text,
                                 (self.window_width // 2 - 180, self.window_height // 2 + 20))

        pygame.display.update()

    def reset(self):
        self.snake.reset()
        self.food.randomize_position(self.snake.positions)
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.speed_level = '中等'
        self.speed = SPEED_LEVELS[self.speed_level]
        self.frame_counter = 0
        # 重置游戏时不重新显示检验提示

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)


# 供外部导入的函数
def run_snake_game():
    """启动贪吃蛇游戏的入口函数"""
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    run_snake_game()