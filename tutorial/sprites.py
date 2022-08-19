import pygame
from config import *
import math
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self_layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        # super
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        # Enum
        self.facing = 'down'

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        # Hitbox.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        # Temp variables, mayber return from method movement
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        # List of all pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'


class Block(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        # super
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLUE)

        # Hitbox.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
