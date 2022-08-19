"""Main game."""
import pygame
from sprite_sheet import SpriteSheet

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG = (50, 50, 50)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('GamePy')
sprite_sheet_image = pygame.image.load('doux.png').convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)

# Create animation list
animation_list = []
animation_steps = [4, 6, 3, 4]
# What is the action that is happening. Can be an enum
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 75
frame = 0


# Extracts all the animations from the sprite sheet
step_counter = 0
for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(
            step_counter, 24, 24, 3, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)

run = True
while run:

    # Update Background
    screen.fill(BG)

    # Update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        last_update = current_time
        frame += 1
        if frame >= len(animation_list[action]):
            frame = 0
    # Show frame image
    screen.blit(animation_list[action][frame], (0, 0))

    # Event handler:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and action > 0:
                action -= 1
                frame = 0
            if event.key == pygame.K_UP and action < len(animation_list) - 1:
                action += 1
                frame = 0

    pygame.display.update()

pygame.quit()
