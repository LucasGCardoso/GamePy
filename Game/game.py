import pygame
from sprites import *
from config import *
from random import randint


class Game:
    """Game main class."""

    def __init__(self):
        """The game constructor. Initializes the screen, fonts, images for the sprites and the game clock."""
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
        """Generates the map for the level. 
           Uses procedural generation using a 'drunk' agent, that walks around in a random way removing the walls.
           We have:
           - B for walls
           - . for free spaces
           - P for player
           - E for Enemies
           - S for stairs

        Returns:
            list: A matrix representing the tilemap for the level.
        """

        tilemap = [['B' for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        percentage_of_floor = 0.6
        wall_count_down = int(MAP_WIDTH * MAP_HEIGHT * percentage_of_floor)

        drunk_agent = {
            'wallCountdown': wall_count_down,
            'padding': 1,
            'x': MAP_WIDTH // 2,
            'y': MAP_HEIGHT // 2
        }

        free_tiles = []

        while drunk_agent['wallCountdown'] >= 0:
            x = drunk_agent['x']
            y = drunk_agent['y']

            if tilemap[y][x] == 'B':
                tilemap[y][x] = '.'
                drunk_agent['wallCountdown'] -= 1
                free_tiles.append((y, x))

            roll = randint(1, 4)

            if roll == 1 and x > drunk_agent['padding']:
                drunk_agent['x'] -= 1

            if roll == 2 and x < MAP_WIDTH - 1 - drunk_agent['padding']:
                drunk_agent['x'] += 1

            if roll == 3 and y > drunk_agent['padding']:
                drunk_agent['y'] -= 1

            if roll == 4 and y < MAP_HEIGHT - 1 - drunk_agent['padding']:
                drunk_agent['y'] += 1

        player_y = MAP_WIDTH // 2
        player_x = MAP_HEIGHT // 2
        tilemap[player_y][player_x] = 'P'

        # Spawn enemies
        enemy_count = 5
        for _ in range(0, enemy_count):
            index = randint(0, len(free_tiles) - 1)
            y = free_tiles[index][0]
            x = free_tiles[index][1]
            tilemap[y][x] = 'E'

        # Spawn stairs
        # Tries 30 times to spawn a random stair that is some percentage away from the player.
        tentatives = 30
        stair_distance = 0.7
        while tentatives >= 0:
            tentatives = tentatives - 1
            index = randint(0, len(free_tiles) - 1)
            y = free_tiles[index][0]
            x = free_tiles[index][1]
            if (y - player_y >= MAP_WIDTH * stair_distance) and (x - player_x >= MAP_HEIGHT * stair_distance):
                tilemap[y][x] = 'S'
                break
            if tentatives == 0:
                tilemap[y][x] = 'S'
                break

        return tilemap

    def create_tilemap(self):
        """Create the tilemap, calling the map generation method and rendering the result."""
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
                if column == "S":
                    Stair(self, j, i)

    def new(self):
        """Method responsible for starting a new game, initializing the sprites and camera."""
        self.playing = True

        self.camera_group = CameraGroup(self)

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.interactable = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.create_tilemap()

    def events(self):
        """Method that loops on the events of the game, for each frame.."""
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
        """Method that updates all the sprites in the game, for each frame."""
        # This goes to all the sprites contained in the group and call their update method.
        self.all_sprites.update()

    def draw(self):
        """Method that draws everything on the screen for each frame."""
        self.camera_group.update()
        self.camera_group.custom_draw(self.player)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        """The main loop of the game. Calls all the other methods.
            It:
            1 - Checks for events and take action
            2 - Updates everything
            3 - Draws the results of the frame
        """
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        """Displays the Game Over screen."""
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
        """Displays the Intro screen."""
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
