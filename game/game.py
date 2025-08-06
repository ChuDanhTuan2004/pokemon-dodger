import pygame
import sys
from .config import *
from .assets import AssetManager
from .game_objects import Player, EnemyManager
from .screens import ScreenManager

class Game:
    def __init__(self):
        # Khởi tạo pygame
        pygame.init()
        pygame.mixer.init()
        
        # Tạo màn hình
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pokemon Dodger")
        self.clock = pygame.time.Clock()
        
        # Tải assets
        self.assets = AssetManager()
        
        # Quản lý màn hình
        self.screen_manager = ScreenManager(self.assets)
        
        # Quản lý kẻ thù
        self.enemy_manager = EnemyManager()
        
        # Trạng thái game
        self.game_state = "start"
        self.selected_player = "blue"
        self.selected_enemies = ENEMY_TYPES.copy()
        self.score = 0
        self.current_music = None
        
        # Tạo người chơi
        self.player = None
    
    def play_background_music(self, music_type):
        """Phát nhạc nền"""
        music_path = self.assets.music_paths[music_type]
        if self.current_music != music_path:
            if self.assets.load_music(music_path):
                pygame.mixer.music.play(-1)
                self.current_music = music_path
    
    def play_sound_effect(self, sound_name):
        """Phát hiệu ứng âm thanh"""
        sound = self.assets.sounds.get(sound_name)
        if sound:
            sound.play()
    
    def reset_game(self):
        """Reset game về trạng thái ban đầu"""
        self.score = 0
        
        # Tạo người chơi mới
        self.player = Player(
            WIDTH // 2 - PLAYER_SIZE // 2,
            HEIGHT - 2 * PLAYER_SIZE,
            self.assets.player_sprites[self.selected_player]
        )
        
        # Tạo kẻ thù
        self.enemy_manager.create_enemies(
            self.screen_manager.difficulty_level,
            self.selected_enemies,
            self.assets.enemy_sprites
        )
    
    def handle_events(self):
        """Xử lý sự kiện"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
        
        return True
    
    def handle_keydown(self, key):
        """Xử lý sự kiện nhấn phím"""
        if self.game_state == "start":
            if key == pygame.K_RETURN:
                self.play_sound_effect('click')
                self.game_state = "select_player"
        
        elif self.game_state == "select_player":
            if key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.play_sound_effect('click')
                new_player = self.screen_manager.handle_player_selection_input(key)
                if new_player:
                    self.selected_player = new_player
            elif key == pygame.K_RETURN:
                self.play_sound_effect('click')
                self.game_state = "select_difficulty"
        
        elif self.game_state == "select_difficulty":
            if key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.play_sound_effect('click')
                self.screen_manager.handle_difficulty_selection_input(key)
            elif key == pygame.K_RETURN:
                self.play_sound_effect('click')
                self.game_state = "playing"
                self.reset_game()
        
        elif self.game_state == "game_over":
            if key == pygame.K_RETURN:
                self.play_sound_effect('click')
                self.game_state = "start"
    
    def handle_player_input(self):
        """Xử lý input của người chơi trong game"""
        if self.game_state != "playing" or not self.player:
            return
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT]:
            self.player.move_right(WIDTH)
        else:
            self.player.stop()
    
    def update_game(self):
        """Cập nhật logic game"""
        if self.game_state != "playing":
            return
        
        # Cập nhật kẻ thù và tính điểm
        score_gained = self.enemy_manager.update_enemies(self.screen_manager.difficulty_level)
        self.score += score_gained
        
        # Kiểm tra va chạm
        if self.enemy_manager.check_collisions(self.player):
            self.play_sound_effect('collision')
            if self.player.take_damage():
                self.game_state = "game_over"
    
    def render(self):
        """Vẽ màn hình"""
        self.screen.fill(WHITE)
        
        if self.game_state == "start":
            self.play_background_music('menu')
            self.screen_manager.draw_start_screen(self.screen)
        
        elif self.game_state == "select_player":
            self.play_background_music('menu')
            self.screen_manager.draw_player_selection(self.screen)
        
        elif self.game_state == "select_difficulty":
            self.play_background_music('menu')
            self.screen_manager.draw_difficulty_selection(self.screen)
        
        elif self.game_state == "playing":
            self.play_background_music('playing')
            
            # Vẽ kẻ thù
            self.enemy_manager.draw_all(self.screen)
            
            # Vẽ người chơi
            if self.player:
                self.player.draw(self.screen)
            
            # Vẽ HUD
            hp = self.player.hp if self.player else 0
            self.screen_manager.draw_hud(self.screen, self.score, hp)
        
        elif self.game_state == "game_over":
            self.play_background_music('menu')
            self.screen_manager.draw_game_over(self.screen, self.score)
        
        pygame.display.flip()
    
    def run(self):
        """Vòng lặp chính của game"""
        running = True
        
        while running:
            running = self.handle_events()
            self.handle_player_input()
            self.update_game()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()