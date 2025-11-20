import pygame.font
from pygame.sprite import Group
from ship import Ship # 重新导入 Ship 类，用于显示飞船生命值图标


class Scoreboard:
    """显示得分信息的类。"""

    def __init__(self, ai_game):
        """初始化得分板属性。"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 得分显示的字体设置。
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分图像。
        self.prep_score()
        self.prep_high_score() # 确保在初始化时加载并显示最高分
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转换为渲染的图像。"""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True,
                                             self.text_color, self.settings.bg_color)
        
        # 将得分放在屏幕右上角。
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高分转换为渲染的图像。"""
        high_score = round(self.stats.high_score, -1)
        # 统一使用 'High Score: ' 前缀，更清晰
        high_score_str = f"High Score: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
                                                  self.text_color, self.settings.bg_color)

        # 将最高分放在屏幕顶部中央。
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """检查是否诞生了新的最高分。"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """将等级转换为渲染的图像。"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                             self.text_color, self.settings.bg_color)
        
        # 将等级放在得分下方。
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还剩下多少艘飞船。"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            # 放置飞船图标在左上角，保持 1.5 倍的间距
            ship.rect.x = 10 + ship_number * ship.rect.width * 1.5 
            ship.rect.y = 10 
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上绘制得分、最高分、等级和剩余飞船。"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)