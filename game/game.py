import pygame
import sys
from .config import *
from .assets import AssetManager
from .game_objects import Player, EnemyManager, Ground
from .screens import ScreenManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pokemon Dodger")
        self.clock = pygame.time.Clock()
        
        self.assets = AssetManager()
        
        self.screen_manager = ScreenManager(self.assets)
        
        self.enemy_manager = EnemyManager()
        
        self.ground = Ground()
        
        self.game_state = "start"
        self.selected_player = "blue"
        self.selected_enemies = ENEMY_TYPES.copy()
        self.score = 0
        self.current_music = None
        
        self.player = None
    
    def play_background_music(self, music_type):
        music_path = self.assets.music_paths[music_type]
        if self.current_music != music_path:
            if self.assets.load_music(music_path):
                pygame.mixer.music.play(-1)
                self.current_music = music_path
    
    def play_sound_effect(self, sound_name):
        sound = self.assets.sounds.get(sound_name)
        if sound:
            sound.play()
    
    def reset_game(self):
        self.score = 0
        
        self.player = Player(
            WIDTH // 2 - PLAYER_SIZE // 2,
            HEIGHT - GROUND_HEIGHT - PLAYER_SIZE,
            self.assets.player_sprites[self.selected_player],
            self.selected_player
        )
        
        self.enemy_manager.create_enemies(
            self.screen_manager.difficulty_level,
            self.selected_enemies,
            self.assets.enemy_sprites
        )
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
        
        return True
    
    def handle_keydown(self, key):
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
        if self.game_state != "playing" or not self.player:
            return
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT]:
            self.player.move_right(WIDTH)
        else:
            self.player.stop()
        
        if keys[pygame.K_SPACE]:
            if self.player.use_ability():
                self.play_sound_effect('click')
    
    def update_game(self):
        if self.game_state != "playing":
            return
        
        dt = self.clock.get_time() / 1000.0
        self.player.update_abilities(dt)
        
        if self.player.player_type == "gray" and self.player.ability_active:
            self.enemy_manager.set_all_speed_modifier(0.3)
        else:
            self.enemy_manager.set_all_speed_modifier(1.0)
        
        score_gained = self.enemy_manager.update_enemies(self.screen_manager.difficulty_level)
        self.score += score_gained
        
        if self.enemy_manager.check_collisions(self.player):
            self.play_sound_effect('collision')
            if self.player.take_damage():
                self.game_state = "game_over"
    
    def render(self):
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
            
            self.enemy_manager.draw_all(self.screen, self.ground.y)
            
            if self.player:
                self.player.draw(self.screen)
            
            self.ground.draw(self.screen)
            
            hp = self.player.hp if self.player else 0
            self.screen_manager.draw_hud(self.screen, self.score, hp, self.player)
        
        elif self.game_state == "game_over":
            self.play_background_music('menu')
            self.screen_manager.draw_game_over(self.screen, self.score)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            running = self.handle_events()
            self.handle_player_input()
            self.update_game()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()