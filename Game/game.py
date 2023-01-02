import pygame
from sprites import *
from config import *
from random import randint
from pygame import mixer
import yaml
from yaml.loader import SafeLoader


class Game:
    """Game main class."""

    def __init__(self):
        """The game constructor. Initializes the screen, fonts, images for the sprites and the game clock."""
        pygame.init()

        # Open the file and load the file
        with open('config.yaml') as f:
            self.cfg = yaml.load(f, Loader=SafeLoader)
            print(self.cfg)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('fonts/times_new_roman.ttf', 32)
        self.running = True

        self.character_spritesheet = SpriteSheet('img/chars/player-sheet.png')
        self.stair_spritesheet = SpriteSheet('img/tiles/stairs.png')
        self.wall_spritesheet = SpriteSheet('img/tiles/stone_wall.png')
        self.wall_spritesheet_detail1 = SpriteSheet(
            'img/tiles/stone_wall_detail1.png')
        self.wall_spritesheet_detail2 = SpriteSheet(
            'img/tiles/stone_wall_detail2.png')
        self.enemy_spritesheet = SpriteSheet('img/chars/enemy.png')
        self.attack_spritesheet = SpriteSheet('img/chars/attack-sheet.png')
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.game_over_background = pygame.image.load('img/gameover.png')

        # Floors
        self.floor_spritesheet = SpriteSheet('img/tiles/grass.png')
        self.floor_detail_spritesheet = SpriteSheet(
            'img/tiles/grass_flower.png')

        if self.cfg['difficulty'] == 'easy':
            self.enemy_qtd = 5
        elif self.cfg['difficulty'] == 'hard':
            self.enemy_qtd = 10
        elif self.cfg['difficulty'] == 'impossible':
            self.enemy_qtd = 20
        else:
            raise ValueError(
                "Difficulty provided does not exist. Try using 'easy', 'hard' or 'impossible'. ")

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

        # Spawn enemies from a certain distance from the player.
        enemy_count = self.enemy_qtd
        enemy_distance = 0.3
        while (enemy_count > 0):
            index = randint(0, len(free_tiles) - 1)
            y = free_tiles[index][0]
            x = free_tiles[index][1]

            y_distance = abs(y - player_y)
            x_distance = abs(x - player_x)

            if (y_distance >= MAP_WIDTH * enemy_distance) and (x_distance >= MAP_HEIGHT * enemy_distance):
                tilemap[y][x] = 'E'
                enemy_count -= 1

        # Spawn stairs
        # Tries 30 times to spawn a random stair that is some percentage away from the player.
        tentatives = 30
        stair_distance = 0.7
        greater_x_and_y = [0, 0]
        while tentatives >= 0:
            tentatives = tentatives - 1
            index = randint(0, len(free_tiles) - 1)
            y = free_tiles[index][0]
            x = free_tiles[index][1]
            y_distance = abs(y - player_y)
            x_distance = abs(x - player_x)
            if (y_distance >= MAP_WIDTH * stair_distance) and (x_distance >= MAP_HEIGHT * stair_distance):
                tilemap[y][x] = 'S'
                break
            # Saves the best X and Y values so far.
            if y_distance > greater_x_and_y[1] and x_distance > greater_x_and_y[0]:
                greater_x_and_y[1] = y
                greater_x_and_y[0] = x
            # Uses the best X and Y values to create the stairs if not created before.
            if tentatives == 0:
                tilemap[greater_x_and_y[1]][greater_x_and_y[0]] = 'S'
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
        self.is_in_range_of_interactable = False
        self.interactable_in_range = None
        self.current_level = 0

        self.attack_cooldown = 0
        self.cooldown_step = 0.2

        self.camera_group = CameraGroup(self)

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.interactables = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.create_tilemap()

        # Starts background song
        mixer.init()
        mixer.music.load('./sounds/background.wav')
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)

    def events(self):
        """Method that loops on the events of the game, for each frame.."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up' and self.attack_cooldown <= 0:
                        Attack(self, self.player.rect.x,
                               self.player.rect.y - TILESIZE)
                        self.attack_cooldown = 10
                    if self.player.facing == 'down' and self.attack_cooldown <= 0:
                        Attack(self, self.player.rect.x,
                               self.player.rect.y + TILESIZE)
                        self.attack_cooldown = 10
                    if self.player.facing == 'left' and self.attack_cooldown <= 0:
                        Attack(self, self.player.rect.x -
                               TILESIZE, self.player.rect.y)
                        self.attack_cooldown = 10
                    if self.player.facing == 'right' and self.attack_cooldown <= 0:
                        Attack(self, self.player.rect.x +
                               TILESIZE, self.player.rect.y)
                        self.attack_cooldown = 10
                if event.key == pygame.K_e and self.is_in_range_of_interactable:
                    # Clicks E to interact with the environment, and is in range.
                    # TODO test interactable type
                    if isinstance(self.interactable_in_range, Stair):
                        if self.all_enemies_killed():
                            print("All enemies killed")
                            self.descend()
                        else:
                            print("There are still enemies remaining.")

    def all_enemies_killed(self):
        """Tests if there are enemies alive in the current level."""
        return len(self.enemies) == 0

    def descend(self):
        self.current_level += 1
        print("Descending to level ", self.current_level)
        for sprite in self.all_sprites:
            sprite.kill()
        if self.current_level > 2:
            self.floor_spritesheet = SpriteSheet('img/tiles/dirt.png')
            self.floor_detail_spritesheet = SpriteSheet('img/tiles/mud.png')
        if self.current_level > 5:
            self.floor_spritesheet = SpriteSheet(
                'img/tiles/stone_brick_floor.png')
            self.floor_detail_spritesheet = SpriteSheet(
                'img/tiles/stone_brick_floor_detail.png')
        self.create_tilemap()

    def update(self):
        """Method that updates all the sprites in the game, for each frame."""
        # This goes to all the sprites contained in the group and call their update method.
        self.all_sprites.update()
        self.attack_cooldown -= self.cooldown_step

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

        # score = self.font.render(f'Score: {self.current_level}', True, RED)
        # score_rect = score.get_rect(
        #     center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.8))

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
            # self.screen.blit(score, score_rect)
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
