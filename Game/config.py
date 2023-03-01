"""Config Tiles."""
import pygame
import yaml
from yaml.loader import SafeLoader

# Open the file and load the file
with open('config.yaml') as f:
    cfg = yaml.load(f, Loader=SafeLoader)

SCREEN_WIDTH = cfg['screen_width']
SCREEN_HEIGHT = cfg['screen_height']

TILESIZE = 96  # 32
PLAYERSIZE = 64
MAP_WIDTH = 30
MAP_HEIGHT = 30

FPS = 60
# Layers determines who spawns first. First the blocks (floor and walls), then the player, in the top of the floor.
GROUND_LAYER = 1
BLOCK_LAYER = 2
ENEMY_LAYER = 3
PLAYER_LAYER = 4

PLAYER_SPEED = 3
ENEMY_SPEED = 3

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Each tile 32px, and height is 480px, and width is 640px so we have:
# - 480/32 = 15 rows
# - 640/32 = 20 columns
