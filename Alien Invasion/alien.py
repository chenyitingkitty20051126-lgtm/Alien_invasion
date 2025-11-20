import pygame
from pygame.sprite import Sprite
import time # 导入 time 模块用于计时

class Alien(Sprite):
    """表示单个外星人的类，带有爆炸动画逻辑。"""

    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置。"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # 加载外星人图像 (假设名为 alien.bmp)
        self.image_alien = pygame.image.load('images/alien.bmp')
        
        # [重要] 加载爆炸图像 (请确保 'images/exploded_alien.png' 路径正确)
        try:
            self.image_explosion = pygame.image.load('images/exploded_alien.jpg')
        except pygame.error:
            # 如果图片不存在，使用一个红色方块作为占位符
            print("警告: 无法加载 'images/exploded_alien.png'。使用占位符。")
            self.image_explosion = pygame.Surface((50, 50))
            self.image_explosion.fill((255, 0, 0))
            self.image_explosion.set_colorkey((255, 0, 0)) # 避免红色方块挡住其他元素

        # 默认使用外星人图像的矩形
        self.image = self.image_alien
        self.rect = self.image.get_rect()

        # 每个新外星人都在屏幕左上角附近。
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置。
        self.x = float(self.rect.x)
        
        # [新增] 爆炸状态追踪
        self.exploding = False
        self.explosion_time = 0.0 # 记录开始爆炸的时间戳

    def check_edges(self):
        """如果外星人位于屏幕边缘，返回 True。"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """更新外星人的位置或处理爆炸计时。"""
        # 如果外星人处于爆炸状态，只需检查时间
        if self.exploding:
            # 检查爆炸持续时间是否已过
            current_time_ms = time.time() * 1000 # 转换为毫秒
            if current_time_ms - self.explosion_time > self.settings.explosion_duration_ms:
                # 持续时间已过，从 group 中移除
                self.kill() 
            # 处于爆炸状态时不进行水平移动
            return

        # 正常移动逻辑
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
        
    def start_explosion(self):
        """将外星人切换到爆炸状态。"""
        if not self.exploding:
            self.exploding = True
            self.explosion_time = time.time() * 1000 # 记录开始爆炸的毫秒时间戳
            self.image = self.image_explosion # 切换图像到爆炸图片
            
    def blitme(self):
        """在当前位置绘制外星人。"""
        self.screen.blit(self.image, self.rect)