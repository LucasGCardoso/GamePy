"""Config Tiles."""
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

TILESIZE = 32
FPS = 60
# Layers determines who spawns first. First the blocks (floor and walls), then the player, in the top of the floor.
GROUND_LAYER = 1
BLOCK_LAYER = 2
PLAYER_LAYER = 3
PLAYER_SPEED = 3

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Each tile 32px, and height is 480px, and width is 640px so we have:
# - 480/32 = 15 rows
# - 640/32 = 20 columns

# We have:
# - B for walls
# - . for free spaces
# - P for player
tilemap = [
    'BBBBBBBBBBBBBBBBBBBB',
    'B..................B',
    'B.....BBB..........B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..........BBB.....B',
    'B..........B..P....B',
    'B..........B.......B',
    'B..........B.......B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'BBBBBBBBBBBBBBBBBBBB',
]
