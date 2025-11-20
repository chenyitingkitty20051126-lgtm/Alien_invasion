import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
import time 


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # [新增] 初始化 Pygame 混音器
        pygame.mixer.init()
        self._load_sounds()

        # Create an instance to store game statistics,
        # 	 and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # [修改] 实例化 Play 按钮并进行位置调整。(向上偏移40像素)
        self.play_button = Button(self, "Play", y_offset=-40) 
        
        # [新增] 实例化 Reset High Score 按钮 (向下偏移40像素, 使用红色以示区别)。
        self.reset_score_button = Button(self, "Reset High Score", 
                                             y_offset=40, width=300, 
                                             button_color=(200, 50, 50))

    def _load_sounds(self):
        """加载所有游戏音频文件，使用用户提供的文件名。"""
        # 假设声音文件位于游戏根目录下的 'sound' 文件夹中
        try:
            # 对应用户的 laser1.wav 文件
            self.sound_shoot = pygame.mixer.Sound('sound/laser1.wav')
            # 对应用户的 DeathFlash.flac 文件 (注意：flac兼容性可能不如wav或ogg)
            self.sound_explosion = pygame.mixer.Sound('sound/DeathFlash.flac')
        except pygame.error as e:
            print(f"警告: 无法加载音频文件。请确保 'sound' 文件夹存在并包含 laser1.wav 和 DeathFlash.flac。错误: {e}")
            print("提示: 如果 DeathFlash.flac 加载失败，请尝试将其转换为 .wav 或 .ogg 格式。")
            # 如果加载失败，将声音对象设为 None，防止程序崩溃
            self.sound_shoot = None
            self.sound_explosion = None

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)
            
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # [修改] 退出前保存最高分，确保持久化
                self.stats.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                # [新增] 检查 Reset High Score 按钮是否被点击
                self._check_reset_score_button(mouse_pos)
                
    def _check_reset_score_button(self, mouse_pos):
        """检查玩家是否点击了 Reset High Score 按钮。"""
        button_clicked = self.reset_score_button.rect.collidepoint(mouse_pos)
        
        # 只有在游戏处于非活动状态（主菜单）时才能点击重置按钮
        if button_clicked and not self.game_active:
            # 执行重置逻辑 (调用 GameStats 中的方法)
            self.stats.reset_high_score()
            
            # 更新计分板显示，反映最高分已归零
            self.sb.prep_high_score()
            
            # 确保鼠标是可见的
            pygame.mouse.set_visible(True)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        is_reset_button_area = self.reset_score_button.rect.collidepoint(mouse_pos)
        
        # [修改] 确保点击 Play 按钮区域，且游戏处于非活动状态，且没有同时点击 Reset 按钮
        if button_clicked and not self.game_active and not is_reset_button_area:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            # [修改] 退出前保存最高分
            self.stats.save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
            # [新增] 播放射击声
            if self.sound_shoot:
                self.sound_shoot.play()


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # [修改] 碰撞处理和检查舰队是否清空被拆分
        self._check_bullet_alien_collisions()
        # [新增] 检查是否有需要生成新舰队
        self._check_fleet_empty() 


    def _check_fleet_empty(self):
        """检查外星人舰队是否被清空，如果清空则创建新的舰队。"""
        # 注意：外星人在爆炸完成后由自身计时器移除
        # 因此，只有当 group 中所有外星人（包括爆炸中的）都被移除时才创建新舰队
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()
    
    def _check_bullet_alien_collisions(self):
        """响应子弹-外星人碰撞。"""
        # [关键修改] True, False：子弹被移除 (True)，但外星人不会立即被移除 (False)
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, False)

        if collisions:
            # 使用 set 确保同一个外星人只被处理一次（虽然不太可能，但更安全）
            aliens_to_explode = set()
            for aliens_hit in collisions.values():
                for alien in aliens_hit:
                    aliens_to_explode.add(alien)

            for alien in aliens_to_explode:
                # 只有未爆炸的外星人才开始爆炸和加分
                if not alien.exploding:
                    alien.start_explosion() # 切换状态并设置计时器
                    
                    # [新增] 播放爆炸声
                    if self.sound_explosion:
                        self.sound_explosion.play()
                        
                    # 加分逻辑
                    self.stats.score += self.settings.alien_points
                    self.sb.prep_score()
                    self.sb.check_high_score()
        # [旧逻辑已移除] if not self.aliens: ... 现在由 _check_fleet_empty 处理


    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            # [修改] 游戏结束时保存最高分
            self.stats.save_high_score() 

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        # [修改] self.aliens.update() 现在会同时处理移动和爆炸计时
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            # [修改] 只有未爆炸的外星人才会下落和转向
            if not alien.exploding: 
                alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        
        # 外星人 group 会自动绘制所有 sprite，包括爆炸中的
        self.aliens.draw(self.screen) 

        self.sb.show_score()

        if not self.game_active:
            self.play_button.draw_button()
            # [新增] 绘制重置按钮
            self.reset_score_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()