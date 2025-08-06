import pygame
from .config import *

class ScreenManager:
    def __init__(self, assets):
        self.assets = assets
        self.player_selection_index = 0
        self.difficulty_level = 1
    
    def draw_text(self, screen, text, font_size, color, x, y):
        font = self.assets.fonts[font_size]
        img = font.render(text, True, color)
        text_rect = img.get_rect(center=(x, y))
        screen.blit(img, text_rect)
    
    def draw_start_screen(self, screen):
        if self.assets.images['logo']:
            logo_rect = self.assets.images['logo'].get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(self.assets.images['logo'], logo_rect)
        else:
            self.draw_text(screen, "POKEMON DODGER", 'title', BLUE, WIDTH // 2, HEIGHT // 2 - 50)
        
        self.draw_text(screen, "Nhấn ENTER để bắt đầu", 'normal', BLACK, WIDTH // 2, HEIGHT // 2 + 200)
    
    def draw_player_selection(self, screen):
        self.draw_text(screen, "Chọn nhân vật", 'title', BLACK, WIDTH // 2, 100)
        self.draw_text(screen, "Sử dụng mũi tên để chọn, ENTER để xác nhận", 'small', BLUE, WIDTH // 2, 150)
        
        player_positions = {
            "blue": (WIDTH // 4, HEIGHT // 2 + 50),
            "red": (WIDTH // 2, HEIGHT // 2 + 50),
            "gray": (WIDTH * 3 // 4, HEIGHT // 2 + 50)
        }
        
        for i, (player_type, pos) in enumerate(player_positions.items()):
            button = pygame.Rect(pos[0] - 60, pos[1] - 60, 120, 120)
            
            if i == self.player_selection_index:
                pygame.draw.rect(screen, GREEN, button, 4)
            else:
                pygame.draw.rect(screen, GRAY, button, 2)
            
            player_image = self.assets.get_player_image(player_type)
            if player_image:
                img_rect = player_image.get_rect(center=pos)
                screen.blit(player_image, img_rect)
            else:
                temp_rect = pygame.Rect(pos[0] - 25, pos[1] - 25, 50, 50)
                color = BLUE if player_type == "blue" else RED if player_type == "red" else GRAY
                pygame.draw.rect(screen, color, temp_rect)
            
            self.draw_text(screen, player_type.capitalize(), 'small', BLACK, pos[0], pos[1] + 70)
    
    def draw_difficulty_selection(self, screen):
        self.draw_text(screen, "Chọn cấp độ", 'title', BLACK, WIDTH // 2, 100)
        self.draw_text(screen, "Sử dụng mũi tên để chọn, ENTER để bắt đầu chơi", 'small', BLUE, WIDTH // 2, 150)
        
        self.draw_text(screen, f"Cấp độ hiện tại: {self.difficulty_level}", 'normal', RED, WIDTH // 2, 200)
        
        if self.difficulty_level == 1:
            info_text = "Dễ nhất - Ít quái vật, rơi chậm"
        elif self.difficulty_level <= 3:
            info_text = "Dễ - Ít quái vật, rơi hơi nhanh"
        elif self.difficulty_level <= 6:
            info_text = "Trung bình - Nhiều quái vật, rơi nhanh"
        elif self.difficulty_level <= 9:
            info_text = "Khó - Rất nhiều quái vật, rơi rất nhanh"
        else:
            info_text = "Cực khó - Không thể sống sót!"
        
        self.draw_text(screen, info_text, 'small', BLACK, WIDTH // 2, 250)
        
        self.draw_difficulty_slider(screen)
    
    def draw_difficulty_slider(self, screen):
        slider_width = 400
        slider_height = 10
        slider_x = WIDTH // 2 - slider_width // 2
        slider_y = HEIGHT // 2
        
        pygame.draw.rect(screen, GRAY, (slider_x, slider_y, slider_width, slider_height))
        
        for i in range(MAX_DIFFICULTY):
            level_x = slider_x + (i * (slider_width // (MAX_DIFFICULTY - 1)))
            level_color = GREEN if i + 1 == self.difficulty_level else WHITE
            
            pygame.draw.circle(screen, level_color, (level_x, slider_y + slider_height // 2), 15)
            self.draw_text(screen, str(i + 1), 'normal', BLACK, level_x, slider_y + slider_height // 2)
    
    def draw_game_over(self, screen, score):
        self.draw_text(screen, "GAME OVER", 'title', RED, WIDTH // 2, HEIGHT // 3)
        self.draw_text(screen, f"Điểm: {score}", 'normal', BLACK, WIDTH // 2, HEIGHT // 2)
        self.draw_text(screen, "Nhấn ENTER để tiếp tục", 'normal', BLACK, WIDTH // 2, HEIGHT * 2 // 3)
    
    def draw_hud(self, screen, score, hp):
        self.draw_text(screen, f"Điểm: {score}", 'normal', BLACK, WIDTH // 2, 30)
        
        heart_start_x = 20
        heart_y = 20
        
        for i in range(hp):
            if self.assets.images['heart']:
                screen.blit(self.assets.images['heart'], (heart_start_x + i * 35, heart_y))
            else:
                pygame.draw.circle(screen, RED, (heart_start_x + i * 35 + 15, heart_y + 15), 12)
    
    def handle_player_selection_input(self, key):
        if key == pygame.K_LEFT:
            self.player_selection_index = (self.player_selection_index - 1) % len(PLAYER_TYPES)
            return PLAYER_TYPES[self.player_selection_index]
        elif key == pygame.K_RIGHT:
            self.player_selection_index = (self.player_selection_index + 1) % len(PLAYER_TYPES)
            return PLAYER_TYPES[self.player_selection_index]
        return None
    
    def handle_difficulty_selection_input(self, key):
        if key == pygame.K_LEFT:
            self.difficulty_level = max(1, self.difficulty_level - 1)
        elif key == pygame.K_RIGHT:
            self.difficulty_level = min(MAX_DIFFICULTY, self.difficulty_level + 1)
        return self.difficulty_level