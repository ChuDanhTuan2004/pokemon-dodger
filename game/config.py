import pygame

# Kích thước màn hình
WIDTH, HEIGHT = 1280, 720  # Tỷ lệ 16:9

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)

# Cấu hình game
PLAYER_SIZE = 50
PLAYER_SPEED = 12
INITIAL_HP = 3
MAX_DIFFICULTY = 10

# Cấu hình animation
ANIMATION_SPEED_MIN = 0.1
ANIMATION_SPEED_MAX = 0.2

# Danh sách nhân vật và kẻ thù
PLAYER_TYPES = ["blue", "red", "gray"]
ENEMY_TYPES = ["blue", "dark", "purple"]

# Cấu hình âm thanh
CLICK_VOLUME = 0.7
COLLISION_VOLUME = 0.8
MUSIC_VOLUME = 0.3