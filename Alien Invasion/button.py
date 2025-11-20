import pygame.font

class Button:

    def __init__(self, ai_game, msg, y_offset=0, width=200, height=50, button_color=(0, 255, 0), text_color=(255, 255, 255)):
        """初始化按钮的属性。"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和其他属性。
        self.width, self.height = width, height
        self.button_color = button_color
        self.text_color = text_color
        # 使用默认系统字体，大小48
        self.font = pygame.font.SysFont(None, 48) 

        # 创建按钮的 rect 对象，并使其居中。
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # 按钮水平居中
        self.rect.centerx = self.screen_rect.centerx
        # 按钮垂直居中，并应用偏移量 (用于将 Play 和 Reset 按钮分开)
        self.rect.centery = self.screen_rect.centery + y_offset 

        # 按钮的标签只需要创建一次。
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将 msg 渲染为图像，并在按钮上居中。"""
        # 不设置背景色，让按钮的背景色决定文字的背景色
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本。
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)