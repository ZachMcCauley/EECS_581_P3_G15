import pygame
from ResourceManager import ResourceManager

# This script is a base class. Menus, gameplay, etc. can inherit from this class.
class GameManager:
    # Define all the variables associated with the game
    def __init__(self, screen, fps = 60):
        self.fps = fps
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.inGameLoop = True
        self.resourceManager = ResourceManager()
    def Run(self):
        while self.inGameLoop:
            # Do anything specific to this manager
            state = self.RunInternal()
            if state != 0:
                self.inGameLoop = False
                if state == 2:
                    print("game lost")
            # Update the rendering
            pygame.display.flip()
            # Update the PyGame clock
            self.clock.tick(self.fps)
    def HandleSingleEvent(self, event: pygame.event.Event) -> None:
        # Detect quitters
        # Subclasses can amend this function as they deem fit.
        if event.type == pygame.QUIT:
            self.inGameLoop = False
    def ProcessInputs(self) -> None:
        # The loop for inputs
        # This should not be altered by subclasses
        for event in pygame.event.get():
            self.HandleSingleEvent(event)
    def RunInternal(self) -> None:
        # If subclasses alter this function, they should call the base classes function at the start.
        # Handle all inputs
        self.ProcessInputs()
        # Erase all rendering from the previous frame.
        self.screen.fill((0, 0, 0))