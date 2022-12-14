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

        self.x = x * PLAYERSIZE
        self.y = y * PLAYERSIZE
        self.width = PLAYERSIZE
        self.height = PLAYERSIZE

        self.x_change = 0
        self.y_change = 0

        # TODO: Enum
        self.facing = 'down'

        self.animation_loop = 1
        self.idle_animation_change = 0.08
        self.animation_change = 0.08

        self.image = self.game.character_spritesheet.get_sprite(
            0, 0, self.width, self.height)

        # Hitbox.
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # TODO: Must have a better way
        self.down_animations = [
            self.game.character_spritesheet.get_sprite(
                0, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                64, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                128, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                192, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                256, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                320, 0, self.width, self.height)
        ]

        self.up_animations = [
            self.game.character_spritesheet.get_sprite(
                384, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                448, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                512, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                576, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                640, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                704, 0, self.width, self.height)
        ]

        self.right_animations = [
            self.game.character_spritesheet.get_sprite(
                768, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                832, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                896, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                960, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1024, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1088, 0, self.width, self.height)
        ]

        self.left_animations = [
            self.game.character_spritesheet.get_sprite(
                1152, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1216, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1280, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1344, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1408, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1472, 0, self.width, self.height)
        ]

        # Idle animations
        self.idle_down_animations = [
            self.game.character_spritesheet.get_sprite(
                1536, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1600, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1664, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1728, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1792, 0, self.width, self.height)
        ]

        self.idle_up_animations = [
            self.game.character_spritesheet.get_sprite(
                1856, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1920, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                1984, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                2048, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                2112, 0, self.width, self.height)
        ]

        self.idle_right_animations = [
            self.game.character_spritesheet.get_sprite(
                2176, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                2240, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                2304, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                2368, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                2432, 0, self.width, self.height)
        ]

        self.idle_left_animations = [
            self.game.character_spritesheet.get_sprite(
                2496, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                2560, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                2624, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                2688, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(
                2752, 0, self.width, self.height)
        ]

    def update(self):
        """Updates the player sprite. Moves, animates and check collisions."""
        self.movement()
        self.animate()
        self.collide_enemy()
        self.collide_interactables()

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

    def collide_interactables(self):
        """Tests if the player is in range of and interactable object."""
        for i in self.game.interactables:
            if self.rect.colliderect(i.rect):
                self.game.is_in_range_of_interactable = True
                self.game.interactable_in_range = i
            else:
                self.game.is_in_range_of_interactable = False
                self.game.interactable_in_range = None

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
            # Test if the enemy is already dead (playing death animation).
            if not hits[0].died:
                self.kill()
                self.game.playing = False

    def animate(self):
        """Animates the player sprite."""
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.idle_down_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += self.idle_animation_change
                if self.animation_loop >= 5:
                    self.animation_loop = 1
            else:
                self.image = self.down_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += self.animation_change
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.idle_up_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += self.idle_animation_change
                if self.animation_loop >= 5:
                    self.animation_loop = 1
            else:
                self.image = self.up_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += self.animation_change
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.idle_left_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += self.idle_animation_change
                if self.animation_loop >= 5:
                    self.animation_loop = 1
            else:
                self.image = self.left_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += self.animation_change
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.idle_right_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += self.idle_animation_change
                if self.animation_loop >= 5:
                    self.animation_loop = 1
            else:
                self.image = self.right_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += self.animation_change
                if self.animation_loop >= 4:
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

        self.facing = random.choice(['up', 'down'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(
            3, 2, self.width, self.height)
        # self.image.set_colorkey(BLACK)
        self.died = False

        # Hitbox.
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.played_dead_sound = False
        self.dead_sound = pygame.mixer.Sound("./sounds/vampire_dead.mp3")

        self.down_animations = [
            self.game.enemy_spritesheet.get_sprite(
                0, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                96, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                192, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                288, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                384, 0, self.width, self.height)
        ]

        self.up_animations = [
            self.game.enemy_spritesheet.get_sprite(
                480, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                576, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                672, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                768, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                864, 0, self.width, self.height)
        ]

        self.right_animations = [
            self.game.enemy_spritesheet.get_sprite(
                960, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                1056, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                1152, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                1248, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                1344, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                1440, 0, self.width, self.height)
        ]

        self.left_animations = [
            self.game.enemy_spritesheet.get_sprite(
                1536, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                1632, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                1728, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                1824, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                1920, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                2016, 0, self.width, self.height)
        ]

        self.die_animations = [
            self.game.enemy_spritesheet.get_sprite(
                2112, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                2208, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                2304, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                2400, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                2496, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                2592, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                2688, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                2784, 0, self.width, self.height),
            self.game.enemy_spritesheet.get_sprite(
                2880, 0, self.width, self.height),
        ]

    def update(self):
        if not self.died:
            self.movement()
            self.animate()
            self.rect.x += self.x_change
            self.collide_blocks('x')
            self.rect.y += self.y_change
            self.collide_blocks('y')
            self.x_change = 0
            self.y_change = 0
        else:
            if not self.played_dead_sound:
                pygame.mixer.Sound.play(self.dead_sound)
                self.played_dead_sound = True
            self.facing = 'death'
            self.animate()

    def movement(self):
        if self.facing == 'up':
            self.y_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['down', 'right', 'left'])

        if self.facing == 'down':
            self.y_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['up', 'right', 'left'])

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['down', 'up', 'left'])

        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['down', 'up', 'right'])

    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(
                    0, 0, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 5:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(
                    480, 0, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 5:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(
                    960, 0, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 5:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(
                    1536, 0, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(
                    self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 5:
                    self.animation_loop = 1

        if self.facing == "death":
            self.image = self.die_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 9:
                self.animation_loop = 1
                self.kill()

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
                        sprite.rect.x += ENEMY_SPEED
                # If moving left
                if self.x_change < 0:
                    # Lines the top left corner of the sprites.
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= ENEMY_SPEED
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                # If moving down
                if self.y_change > 0:
                    # Lines the top left corner of the sprites and then moves it to the left width amount, rewriting the player's position.
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += ENEMY_SPEED
                # If moving left
                if self.y_change < 0:
                    # Lines the top left corner of the sprites.
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= ENEMY_SPEED


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

        self.image = self.game.wall_spritesheet.get_sprite(
            0, 0, self.width, self.height)

        index = random.randint(0, 100)
        if index < 90:
            self.image = self.game.wall_spritesheet.get_sprite(
                0, 0, self.width, self.height)
        elif index >= 90 and index <= 95:
            self.image = self.game.wall_spritesheet_detail1.get_sprite(
                0, 0, self.width, self.height)
        else:
            self.image = self.game.wall_spritesheet_detail2.get_sprite(
                0, 0, self.width, self.height)

        # Hitbox.
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Stair(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.interactables
        super().__init__(self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.stair_spritesheet.get_sprite(
            0, 0, self.width, self.height)

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

        # self.image = self.game.floor_spritesheet.get_sprite(
        #     0, 0, self.width, self.height)

        index = random.randint(0, 100)
        if index < 97:
            self.image = self.game.floor_spritesheet.get_sprite(
                0, 0, self.width, self.height)
        else:
            self.image = self.game.floor_detail_spritesheet.get_sprite(
                0, 0, self.width, self.height)

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
        self.width = PLAYERSIZE
        self.height = PLAYERSIZE

        self.animation_loop = 0
        self.animation_change = 0.2

        self.image = self.game.attack_spritesheet.get_sprite(
            0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.sword_sound = pygame.mixer.Sound("./sounds/sword.mp3")

        self.down_animations = [
            self.game.attack_spritesheet.get_sprite(
                0, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                64, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                128, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                192, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                256, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                320, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                384, 0, self.width, self.height)
        ]

        self.up_animations = [
            self.game.attack_spritesheet.get_sprite(
                448, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                512, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                576, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                640, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                704, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                768, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                832, 0, self.width, self.height)
        ]

        self.left_animations = [
            self.game.attack_spritesheet.get_sprite(
                896, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                960, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                1024, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                1088, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                1152, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                1216, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                1280, 0, self.width, self.height)
        ]

        self.right_animations = [
            self.game.attack_spritesheet.get_sprite(
                1344, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                1408, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                1472, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                1536, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                1600, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                1664, 0, self.width, self.height),
            self.game.attack_spritesheet.get_sprite(
                1728, 0, self.width, self.height)
        ]

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            enemy_died = hits[0]
            enemy_died.died = True

    def animate(self):
        direction = self.game.player.facing
        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += self.animation_change
            if self.animation_loop >= 7:
                self.kill()
            if self.animation_loop == 1:
                pygame.mixer.Sound.play(self.sword_sound)
        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += self.animation_change
            if self.animation_loop >= 7:
                self.kill()
            if self.animation_loop == 1:
                pygame.mixer.Sound.play(self.sword_sound)
        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += self.animation_change
            if self.animation_loop >= 7:
                self.kill()
            if self.animation_loop == 1:
                pygame.mixer.Sound.play(self.sword_sound)
        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += self.animation_change
            if self.animation_loop >= 7:
                self.kill()
            if self.animation_loop == 1:
                pygame.mixer.Sound.play(self.sword_sound)
