import pygame
import os
from .config import *

class AssetManager:
    def __init__(self):
        self.fonts = {}
        self.images = {}
        self.sounds = {}
        self.player_sprites = {}
        self.enemy_sprites = {}
        self.load_all_assets()
    
    def load_font(self, size, font_name="vietnam-black-font.ttf"):
        """Tải font với kích thước chỉ định"""
        try:
            font_path = os.path.join('assets', 'font', font_name)
            return pygame.font.Font(font_path, size)
        except:
            return pygame.font.SysFont(None, size)
    
    def load_image(self, name, size=(50, 50)):
        """Tải hình ảnh từ thư mục assets/images"""
        path = os.path.join('assets', 'images', name)
        try:
            image = pygame.image.load(path)
            return pygame.transform.scale(image, size)
        except:
            print(f"Không thể tải hình ảnh: {path}")
            return None
    
    def load_sound(self, path, volume=0.5):
        """Tải âm thanh"""
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except Exception as e:
            print(f"Không thể tải âm thanh: {path}, lỗi: {e}")
            return None
    
    def load_music(self, path, volume=0.3):
        """Tải nhạc nền"""
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            return True
        except Exception as e:
            print(f"Không thể tải nhạc nền: {path}, lỗi: {e}")
            return False
    
    def load_player_spritesheet(self, name):
        """Tải sprite sheet cho nhân vật"""
        path = os.path.join('assets', 'images', name)
        try:
            spritesheet = pygame.image.load(path)
            width = spritesheet.get_width() // 8  # 8 frames trong sprite sheet
            height = spritesheet.get_height()
            frames = []
            
            for i in range(8):
                frame = pygame.Surface((width, height), pygame.SRCALPHA)
                frame.blit(spritesheet, (0, 0), (i * width, 0, width, height))
                frames.append(pygame.transform.scale(frame, (PLAYER_SIZE, PLAYER_SIZE)))
            
            return frames
        except Exception as e:
            print(f"Không thể tải sprite sheet: {path}, lỗi: {e}")
            return [None] * 8
    
    def load_enemy_spritesheet(self, name):
        """Tải sprite sheet cho kẻ thù"""
        path = os.path.join('assets', 'images', name)
        try:
            spritesheet = pygame.image.load(path)
            
            num_frames = 4 if "blue" in name else 6  # blue_enemy có 4 frame, dark và purple có 6 frame
            
            width = spritesheet.get_width()
            height = spritesheet.get_height() // num_frames
            frames = []
            
            for i in range(num_frames):
                frame = pygame.Surface((width, height), pygame.SRCALPHA)
                frame.blit(spritesheet, (0, 0), (0, i * height, width, height))
                frames.append(pygame.transform.scale(frame, (PLAYER_SIZE, PLAYER_SIZE)))
            
            return frames
        except Exception as e:
            print(f"Không thể tải sprite sheet kẻ thù: {path}, lỗi: {e}")
            return [None] * (4 if "blue" in name else 6)
    
    def load_all_assets(self):
        """Tải tất cả assets khi khởi tạo"""
        # Tải fonts
        self.fonts['small'] = self.load_font(18)
        self.fonts['normal'] = self.load_font(24)
        self.fonts['title'] = self.load_font(48)
        
        # Tải hình ảnh
        self.images['logo'] = self.load_image("logo.jpg", (1200, 900))
        self.images['heart'] = self.load_image("heart.png", (30, 30))
        
        # Tải sprite sheets cho nhân vật
        for player_type in PLAYER_TYPES:
            self.player_sprites[player_type] = self.load_player_spritesheet(f"{player_type}_player.png")
        
        # Tải sprite sheets cho kẻ thù
        for enemy_type in ENEMY_TYPES:
            self.enemy_sprites[enemy_type] = self.load_enemy_spritesheet(f"{enemy_type}_enemy.png")
        
        # Tải âm thanh
        self.sounds['click'] = self.load_sound(os.path.join('assets', 'sounds', 'click.ogg'), CLICK_VOLUME)
        self.sounds['collision'] = self.load_sound(os.path.join('assets', 'sounds', 'touch.ogg'), COLLISION_VOLUME)
        
        # Đường dẫn nhạc nền
        self.music_paths = {
            'menu': os.path.join('assets', 'musics', 'before_play.ogg'),
            'playing': os.path.join('assets', 'musics', 'playing.ogg')
        }
    
    def get_player_image(self, player_type):
        """Lấy hình ảnh mặc định của nhân vật"""
        if self.player_sprites[player_type] and self.player_sprites[player_type][0]:
            return self.player_sprites[player_type][0]
        return None
    
    def get_enemy_image(self, enemy_type):
        """Lấy hình ảnh mặc định của kẻ thù"""
        if self.enemy_sprites[enemy_type] and self.enemy_sprites[enemy_type][0]:
            return self.enemy_sprites[enemy_type][0]
        return None