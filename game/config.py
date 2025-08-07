import pygame

WIDTH, HEIGHT = 1280, 720


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)


PLAYER_SIZE = 50
PLAYER_SPEED = 12
INITIAL_HP = 3
MAX_DIFFICULTY = 10


ANIMATION_SPEED_MIN = 0.1
ANIMATION_SPEED_MAX = 0.2


PLAYER_TYPES = ["blue", "red", "gray"]
ENEMY_TYPES = ["blue", "dark", "purple"]

PLAYER_ABILITIES = {
    "blue": {
        "name": "Lightning Dash",
        "description": "Tức thời di chuyển nhanh một khoảng cách xa",
        "cooldown": 3.0,
        "key": "SPACE"
    },
    "red": {
        "name": "Phoenix Shield", 
        "description": "Bất tử tạm thời trong 2 giây",
        "cooldown": 8.0,
        "duration": 2.0,
        "key": "SPACE"
    },
    "gray": {
        "name": "Time Warp",
        "description": "Làm chậm tất cả kẻ thù trong 3 giây", 
        "cooldown": 10.0,
        "duration": 3.0,
        "key": "SPACE"
    }
}

GROUND_HEIGHT = 80
GROUND_COLOR = (139, 69, 19)


CLICK_VOLUME = 0.7
COLLISION_VOLUME = 0.8
MUSIC_VOLUME = 0.3