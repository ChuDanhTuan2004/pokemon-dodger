import pygame
import random
from .config import *

class Ground:
    def __init__(self):
        self.y = HEIGHT - GROUND_HEIGHT
        self.rect = pygame.Rect(0, self.y, WIDTH, GROUND_HEIGHT)
    
    def draw(self, screen):
        pygame.draw.rect(screen, GROUND_COLOR, self.rect)
        pygame.draw.line(screen, (100, 50, 10), (0, self.y), (WIDTH, self.y), 3)

class Player:
    def __init__(self, x, y, sprites, player_type="blue"):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED
        self.sprites = sprites
        self.hp = INITIAL_HP
        self.direction = "idle"  # "idle", "left", "right"
        self.player_type = player_type
        
        # Ability system
        self.ability_cooldown = 0.0
        self.ability_active = False
        self.ability_duration = 0.0
        self.invulnerable = False
        self.dash_speed_modifier = 1.0
    
    def move_left(self):
        if self.rect.left > 0:
            effective_speed = self.speed * self.dash_speed_modifier
            self.rect.x -= effective_speed
            self.direction = "left"
    
    def move_right(self, screen_width):
        if self.rect.right < screen_width:
            effective_speed = self.speed * self.dash_speed_modifier
            self.rect.x += effective_speed
            self.direction = "right"
    
    def stop(self):
        self.direction = "idle"
    
    def reset_position(self):
        self.rect.x = WIDTH // 2 - PLAYER_SIZE // 2
        self.rect.y = HEIGHT - GROUND_HEIGHT - PLAYER_SIZE
        self.hp = INITIAL_HP
        self.ability_cooldown = 0.0
        self.ability_active = False
        self.ability_duration = 0.0
        self.invulnerable = False
        self.dash_speed_modifier = 1.0
    
    def take_damage(self):
        if self.invulnerable:
            return False
        self.hp -= 1
        return self.hp <= 0
    
    def update_abilities(self, dt):
        if self.ability_cooldown > 0:
            self.ability_cooldown -= dt
            
        if self.ability_active and self.ability_duration > 0:
            self.ability_duration -= dt
            if self.ability_duration <= 0:
                self.deactivate_ability()
    
    def can_use_ability(self):
        from .config import PLAYER_ABILITIES
        return self.ability_cooldown <= 0 and not self.ability_active
    
    def use_ability(self):
        from .config import PLAYER_ABILITIES
        if not self.can_use_ability():
            return False
            
        ability_info = PLAYER_ABILITIES[self.player_type]
        
        if self.player_type == "blue":  # Lightning Dash
            self.dash_speed_modifier = 4.0
            self.ability_active = True
            self.ability_duration = 0.3
            
        elif self.player_type == "red":  # Phoenix Shield
            self.invulnerable = True
            self.ability_active = True
            self.ability_duration = ability_info["duration"]
            
        elif self.player_type == "gray":  # Time Warp
            self.ability_active = True
            self.ability_duration = ability_info["duration"]
        
        self.ability_cooldown = ability_info["cooldown"]
        return True
    
    def deactivate_ability(self):
        self.ability_active = False
        self.ability_duration = 0.0
        self.invulnerable = False
        self.dash_speed_modifier = 1.0
    
    def draw(self, screen):
        if self.sprites and any(self.sprites):
            frame_index = 0
            
            if self.direction == "left":
                frame_index = 6
            elif self.direction == "right":
                frame_index = 7
            
            if self.sprites[frame_index]:
                screen.blit(self.sprites[frame_index], self.rect)
            else:
                pygame.draw.rect(screen, BLUE, self.rect)
        else:
            pygame.draw.rect(screen, BLUE, self.rect)
        
        if self.ability_active:
            effect_color = None
            if self.player_type == "blue":  # Lightning Dash - Yellow glow
                effect_color = (255, 255, 0, 100)
            elif self.player_type == "red":  # Phoenix Shield - Red glow
                effect_color = (255, 100, 100, 150)
            elif self.player_type == "gray":  # Time Warp - Purple glow
                effect_color = (200, 100, 255, 100)
            
            if effect_color:
                glow_rect = pygame.Rect(self.rect.x - 5, self.rect.y - 5, 
                                      self.rect.width + 10, self.rect.height + 10)
                pygame.draw.rect(screen, effect_color[:3], glow_rect, 3)

class Enemy:
    def __init__(self, x, y, enemy_type, sprites, difficulty):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.type = enemy_type
        self.sprites = sprites
        self.base_speed = random.uniform(1 + difficulty * 0.5, 2 + difficulty * 0.8)
        self.speed = self.base_speed
        self.speed_modifier = 1.0
        
        self.num_frames = 4 if enemy_type == "blue" else 6
        self.frame = 0
        self.animation_speed = random.uniform(ANIMATION_SPEED_MIN, ANIMATION_SPEED_MAX)
        self.animation_counter = 0
    
    def update(self):
        self.speed = self.base_speed * self.speed_modifier
        self.rect.y += self.speed
        
        self.animation_counter += self.animation_speed * self.speed_modifier
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.frame = (self.frame + 1) % self.num_frames
    
    def set_speed_modifier(self, modifier):
        self.speed_modifier = modifier
    
    def reset_position(self):
        self.rect.y = random.randint(-200, -50)
        self.rect.x = random.randint(0, WIDTH - PLAYER_SIZE)
    
    def is_off_screen(self):
        return self.rect.y > HEIGHT
    
    def increase_speed(self, difficulty):
        if random.random() < 0.1:
            self.speed += 0.1 * difficulty
    
    def draw(self, screen, ground_y):
        if self.rect.y < ground_y:
            visible_height = min(self.rect.height, ground_y - self.rect.y)
            if visible_height > 0:
                if self.sprites and self.sprites[self.frame]:
                    sprite_surface = self.sprites[self.frame]
                    visible_rect = pygame.Rect(0, 0, self.rect.width, visible_height)
                    cropped_sprite = sprite_surface.subsurface(visible_rect)
                    screen.blit(cropped_sprite, (self.rect.x, self.rect.y))
                else:
                    visible_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, visible_height)
                    pygame.draw.rect(screen, RED, visible_rect)

class EnemyManager:
    def __init__(self):
        self.enemies = []
    
    def create_enemies(self, difficulty, selected_enemies, enemy_sprites):
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
        score_gained = 0
        
        for enemy in self.enemies:
            enemy.update()
            
            if enemy.is_off_screen():
                enemy.reset_position()
                score_gained += 1
                enemy.increase_speed(difficulty)
        
        return score_gained
    
    def check_collisions(self, player):
        for enemy in self.enemies:
            if player.rect.colliderect(enemy.rect):
                enemy.reset_position()
                return True
        return False
    
    def draw_all(self, screen, ground_y):
        for enemy in self.enemies:
            enemy.draw(screen, ground_y)
    
    def set_all_speed_modifier(self, modifier):
        for enemy in self.enemies:
            enemy.set_speed_modifier(modifier)