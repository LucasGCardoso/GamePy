from turtle import width
import pygame
from sprites import *
from config import *
from random import randint


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('fonts/times_new_roman.ttf', 32)
        self.running = True

        self.character_spritesheet = SpriteSheet('img/character.png')
        self.terrain_spritesheet = SpriteSheet('img/terrain.png')
        self.enemy_spritesheet = SpriteSheet('img/enemy.png')
        self.attack_spritesheet = SpriteSheet('img/attack.png')
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.game_over_background = pygame.image.load('img/gameover.png')

    def generate_map(self):
        # We have:
        # - B for walls
        # - . for free spaces
        # - P for player
        # - E for Enemies
        # tilemap = [
        #     'BBBBBBBBBBBBBBBBBBBB',
        #     'B..................B',
        #     'B.....BBB..........B',
        #     'B...E..............B',
        #     'B..................B',
        #     'B..................B',
        #     'B..........BBB.....B',
        #     'B..........B..P....B',
        #     'B..........B.......B',
        #     'B..........B.......B',
        #     'B..................B',
        #     'B..................B',
        #     'B....E.............B',
        #     'B..................B',
        #     'BBBBBBBBBBBBBBBBBBBB',
        # ]

        number_of_floors = MAP_WIDTH * MAP_HEIGHT // 2
        tilemap = [['B' for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

        # For now, replace half the walls by floors
        # m[r//h][r - (r//h*w)] --> to access the correct tile
        for i in range(number_of_floors):
            random_num = randint(0, MAP_WIDTH * MAP_HEIGHT)
            tilemap[random_num//MAP_HEIGHT][random_num -
                                            (random_num//MAP_HEIGHT*MAP_WIDTH)] = '.'
        tilemap[0][0] = 'P'
        return tilemap

    # For the walls coliders:
    def create_tilemap(self):
        tilemap = self.generate_map()
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "E":
                    Enemy(self, j, i)

    def new(self):
        # A new game starts.
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_tilemap()

    def events(self):
        # Game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x,
                               self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x,
                               self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x -
                               TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x +
                               TILESIZE, self.player.rect.y)

    def update(self):
        # Game loop updates
        # This goes to all the sprites contained in the group and call their update method.
        self.all_sprites.update()

    def draw(self):
        # Game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # Game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('Game Over', True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        restart_button = Button(10, SCREEN_HEIGHT - 60,
                                120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.game_over_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True

        title = self.font.render('GamePy Project', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
