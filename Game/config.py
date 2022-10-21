"""Config Tiles."""
import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 640

TILESIZE = 32
MAP_WIDTH = 30
MAP_HEIGHT = 30

FPS = 60
# Layers determines who spawns first. First the blocks (floor and walls), then the player, in the top of the floor.
GROUND_LAYER = 1
BLOCK_LAYER = 2
ENEMY_LAYER = 3
PLAYER_LAYER = 4

PLAYER_SPEED = 2
ENEMY_SPEED = 1

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Each tile 32px, and height is 480px, and width is 640px so we have:
# - 480/32 = 15 rows
# - 640/32 = 20 columns
