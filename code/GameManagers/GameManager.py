import pygame
from ResourceManager import ResourceManager

# This script is a base class. Menus, gameplay, etc. can inherit from this class.
class GameManager:
    # Define all the variables associated with the game
    def __init__(self, screen, fps = 60):
        self.fps = fps
        self.screen = screen
        self.clock = pygame.time.Clock()
        # Set this to false to end this state of the game.
        self.inGameLoop = True
        # How many GameManagers should be removed from the stack after this ends
        self.removeFromStack = 1
        # This says whether the GameManager ended because the user quit. If so, we should end the program ASAP.
        self.EndedInQuit = False
        # Set this to True to pause execution of this manager without ending it.
        self.surrenderControl = False
        self.resourceManager = ResourceManager()
        self.owner = None
        self.timeSinceLastTick = 0
    def Run(self):
        self.surrenderControl = False
        while self.inGameLoop and not self.surrenderControl:
            # Do anything specific to this manager
            self.RunInternal()
            # Update the rendering
            pygame.display.flip()
            # Update the PyGame clock
            self.timeSinceLastTick = self.clock.tick(self.fps)
    def HandleSingleEvent(self, event: pygame.event.Event) -> None:
        # Detect quitters
        # Subclasses can amend this function as they deem fit.
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.inGameLoop = False
            self.EndedInQuit = True
    def ProcessInputs(self) -> None:
        # The loop for inputs
        for event in pygame.event.get():
            self.HandleSingleEvent(event)
    def RunInternal(self) -> None:
        # If subclasses alter this function, they should call the base classes function at the start.
        # Handle all inputs
        self.ProcessInputs()
        # Erase all rendering from the previous frame.
        self.screen.fill((0, 0, 0))
    def SetOwner(self, owner):
        self.owner = owner
    def Render(self):
        # This should never be invoked
        pass