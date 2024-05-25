import pygame, sys
from settings import *
from level import Level
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Zelda Game")
        self.clock = pygame.time.Clock()
        self.level = Level()
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

#Checks if file is the main file, and if so runs the game
if __name__ == "__main__":
    game = Game()
    game.run()