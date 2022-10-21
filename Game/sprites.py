import pygame
from config import *
import math
import random


class SpriteSheet:
    """Class that holds a spritesheet image."""

    def __init__(self, file):
        """Loads the image containing the sprites.

        Args:
            file (str): The path of the file containing the sprites.
        """
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        """Returns a single sprite of the spritesheet based on position.

        Args:
            x (int): The X axis of the spritesheet for the top left corner of a specific sprite.
            y (int): The Y axis of the spritesheet for the top left corner of a specific sprite.
            width (int): The width of the specific sprite.
            height (int): The height of the specific sprite.

        Returns:
            pygame.Surface: The specific sprite requested.
        """
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class CameraGroup(pygame.sprite.Group):
    """Class responsible for the game camera logic. Inherits from pygame.sprite.Group."""

    def __init__(self, game):
        """Constructor of the Camera class.

        Args:
            game (game.Game): A reference for the Game class.
        """
        super().__init__()
        self.game = game
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def center_target_camera(self, target):
        """Camera that puts the target sprite on the center of the screen and follows it.

        Args:
            target (pygame.sprite.Sprite): The sprite for the camera to follow.
        """
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player):
        """Draws every sprite of the game depending on the passed sprite position, creating the camera logic.

        Args:
            player (pygame.sprite.Sprite): The sprite that the camera will follow. Should be a Player class.
        """

        self.center_target_camera(player)
        self.display_surface.fill(BLACK)

        for sprite in self.game.all_sprites:
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


class Player(pygame.sprite.Sprite):
    """The main Player class. Inherits from pygame.sprite.Sprite."""

    def __init__(self, game, x, y):
        """Constructor for the player.

        Args:
            game (game.Game): A reference for the Game class.
            x (int): The X position of the screen where the player will spawn.
            y (int): The Y position of the screen where the player will spawn.
        """
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        super().__init__(self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        # TODO: Enum
        self.facing = 'down'

        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(
            3, 2, self.width, self.height)

        # Hitbox.
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # TODO: Must have a better way
        self.down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(
            35, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(
            35, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(
            35, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                                 self.game.character_spritesheet.get_sprite(
            35, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]

    def update(self):
        """Updates the player sprite. Moves, animates and check collisions."""
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        """Method that makes the player movements."""
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

    def collide_blocks(self, direction):
        """Checks for collisions with blocks.

        Args:
            direction (str): The orientation of the collision.
        """
        # TODO: ENUM
        if direction == "x":
            # Checks if a rect of a sprite is inside another rect
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                # If moving right
                if self.x_change > 0:
                    # Lines the top left corner of the sprites and then moves it to the left width amount, rewriting the player's position.
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                # If moving left
                if self.x_change < 0:
                    # Lines the top left corner of the sprites.
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                # If moving down
                if self.y_change > 0:
                    # Lines the top left corner of the sprites and then moves it to the left width amount, rewriting the player's position.
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                # If moving left
                if self.y_change < 0:
                    # Lines the top left corner of the sprites.
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_enemy(self):
        """Checks for collisions with enemies."""
        # TODO: Lose HP.
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def animate(self):
        """Animates the player sprite."""
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(
                    3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(
                    3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(
                    3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(
                    3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        super().__init__(self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(
            3, 2, self.width, self.height)
        # self.image.set_colorkey(BLACK)

        # Hitbox.
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Must have a better way
        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.enemy_spritesheet.get_sprite(
            35, 98, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                                 self.game.enemy_spritesheet.get_sprite(
            35, 66, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(
                    3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(
                    3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Block(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        super().__init__(self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(
            960, 448, self.width, self.height)

        # Hitbox.
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Stair(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.interactable
        super().__init__(self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(
            193, 578, self.width, self.height)

        # Hitbox.
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        super().__init__(self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(
            64, 352, self.width, self.height)

        # Hitbox.
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('fonts/times_new_roman.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(
            center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        # Tests if the mouse collided to the button AND it is pressed.
        if self.rect.collidepoint(pos):
            # Mouse pressed[0] means the left button was clicked.
            if pressed[0]:
                return True
        return False


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game

        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        super().__init__(self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(
            0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                                 self.game.attack_spritesheet.get_sprite(
            32, 64, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
            64, 64, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
            96, 64, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(
            32, 32, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
            64, 32, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
            96, 32, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                                self.game.attack_spritesheet.get_sprite(
            32, 96, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
            64, 96, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
            96, 96, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                              self.game.attack_spritesheet.get_sprite(
            32, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
            64, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
            96, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing
        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
