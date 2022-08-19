import pygame
from sprites import *
from config import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.Font('Arial', 32)
        self.running = True

    def new_game(self):
        # A new game starts.
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 1, 2)
        self.create_tilemap()

    # For the walls coliders:
    def create_tilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == 'B':
                    Block(self, j, i)
                if column == 'P':
                    Player(self, j, i)

    def events(self):
        # Game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

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
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass


g = Game()
g.intro_screen()
g.new_game()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
