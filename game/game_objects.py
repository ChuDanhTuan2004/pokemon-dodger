import pygame
import random
from .config import *

class Player:
    def __init__(self, x, y, sprites):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED
        self.sprites = sprites
        self.hp = INITIAL_HP
        self.direction = "idle"  # "idle", "left", "right"
    
    def move_left(self):
        """Di chuyển sang trái"""
        if self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = "left"
    
    def move_right(self, screen_width):
        """Di chuyển sang phải"""
        if self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = "right"
    
    def stop(self):
        """Dừng di chuyển"""
        self.direction = "idle"
    
    def reset_position(self):
        """Đặt lại vị trí ban đầu"""
        self.rect.x = WIDTH // 2 - PLAYER_SIZE // 2
        self.rect.y = HEIGHT - 2 * PLAYER_SIZE
        self.hp = INITIAL_HP
    
    def take_damage(self):
        """Nhận sát thương"""
        self.hp -= 1
        return self.hp <= 0  # Trả về True nếu chết
    
    def draw(self, screen):
        """Vẽ nhân vật"""
        if self.sprites and any(self.sprites):
            frame_index = 0  # Mặc định là frame đứng yên
            
            if self.direction == "left":
                frame_index = 6  # Frame cho di chuyển sang trái
            elif self.direction == "right":
                frame_index = 7  # Frame cho di chuyển sang phải
            
            if self.sprites[frame_index]:
                screen.blit(self.sprites[frame_index], self.rect)
            else:
                pygame.draw.rect(screen, BLUE, self.rect)
        else:
            pygame.draw.rect(screen, BLUE, self.rect)

class Enemy:
    def __init__(self, x, y, enemy_type, sprites, difficulty):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.type = enemy_type
        self.sprites = sprites
        self.speed = random.uniform(1 + difficulty * 0.5, 2 + difficulty * 0.8)
        
        # Animation
        self.num_frames = 4 if enemy_type == "blue" else 6
        self.frame = 0
        self.animation_speed = random.uniform(ANIMATION_SPEED_MIN, ANIMATION_SPEED_MAX)
        self.animation_counter = 0
    
    def update(self):
        """Cập nhật vị trí và animation"""
        # Di chuyển xuống
        self.rect.y += self.speed
        
        # Cập nhật animation
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.frame = (self.frame + 1) % self.num_frames
    
    def reset_position(self):
        """Đặt lại vị trí ở trên đầu màn hình"""
        self.rect.y = random.randint(-200, -50)
        self.rect.x = random.randint(0, WIDTH - PLAYER_SIZE)
    
    def is_off_screen(self):
        """Kiểm tra xem kẻ thù có ra khỏi màn hình không"""
        return self.rect.y > HEIGHT
    
    def increase_speed(self, difficulty):
        """Tăng tốc độ dựa trên độ khó"""
        if random.random() < 0.1:
            self.speed += 0.1 * difficulty
    
    def draw(self, screen):
        """Vẽ kẻ thù"""
        if self.sprites and self.sprites[self.frame]:
            screen.blit(self.sprites[self.frame], self.rect)
        else:
            pygame.draw.rect(screen, RED, self.rect)

class EnemyManager:
    def __init__(self):
        self.enemies = []
    
    def create_enemies(self, difficulty, selected_enemies, enemy_sprites):
        """Tạo kẻ thù dựa trên độ khó"""
        self.enemies = []
        num_enemies = difficulty * 2
        
        for _ in range(num_enemies):
            enemy_type = random.choice(selected_enemies)
            enemy = Enemy(
                random.randint(0, WIDTH - PLAYER_SIZE),
                random.randint(-800, -50),
                enemy_type,
                enemy_sprites[enemy_type],
                difficulty
            )
            self.enemies.append(enemy)
    
    def update_enemies(self, difficulty):
        """Cập nhật tất cả kẻ thù"""
        score_gained = 0
        
        for enemy in self.enemies:
            enemy.update()
            
            # Nếu kẻ thù ra khỏi màn hình
            if enemy.is_off_screen():
                enemy.reset_position()
                score_gained += 1
                enemy.increase_speed(difficulty)
        
        return score_gained
    
    def check_collisions(self, player):
        """Kiểm tra va chạm với người chơi"""
        for enemy in self.enemies:
            if player.rect.colliderect(enemy.rect):
                enemy.reset_position()  # Di chuyển kẻ thù để tránh va chạm liên tục
                return True
        return False
    
    def draw_all(self, screen):
        """Vẽ tất cả kẻ thù"""
        for enemy in self.enemies:
            enemy.draw(screen)