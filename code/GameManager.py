import pygame
from Grid.Grid import Grid

# This script should cover anything specifically related to the main gameplay loop
# For menus, go create a separate class.
class GameManager:
    def __init__(self, screen, fps = 60):
        self.grid = Grid.FormFromDims((8, 8))
        self.fps = fps
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.inGameLoop = True
    def Run(self):
        while self.inGameLoop:
            self.RunInternal()
            pygame.display.flip()
            self.clock.tick(self.fps)
    def ProcessInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.inGameLoop = False
    def RunInternal(self):
        self.ProcessInputs()
        # Erase all rendering from the previous frame.
        self.screen.fill((0, 0, 0))
        self.grid.Render(self.screen)