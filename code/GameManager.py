import pygame

# This script is a base class. Menus, gameplay, etc. can inherit from this class.
class GameManager:
    def __init__(self, screen, fps = 60):
        self.fps = fps
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.inGameLoop = True
    def Run(self):
        while self.inGameLoop:
            self.RunInternal()
            pygame.display.flip()
            self.clock.tick(self.fps)
    def HandleSingleEvent(self, event):
        if event.type == pygame.QUIT:
            self.inGameLoop = False
    def ProcessInputs(self):
        for event in pygame.event.get():
            self.HandleSingleEvent(event)
    def RunInternal(self):
        self.ProcessInputs()
        # Erase all rendering from the previous frame.
        self.screen.fill((0, 0, 0))