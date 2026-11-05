import pygame
from ResourceManager import ResourceManager

class Item:
    def __init__(self, name: str):
        # OnClear can be reassigned to a function for the purpose of powerups.
        # Alternatively, we can make powerups inherit Item and give them their own
        # OnClear methods
        self.OnClear = lambda position: None
        self.name = name
        # You could also specify this in the parameters, but I would prefer to have this get the resource directly
        self.unscaledSprite = ResourceManager.GetResourceManager().GetResource(self.name)
    def __eq__(self, other) -> bool:
        return self.name == other.name
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return f"Item({self.name})"
    # This is NOT tested. Your computer MIGHT explode when you run this!!!
    def Render(self, screen, position, pixelSize, offset = (0, 0)):
        scaledSprite = pygame.transform.scale_by(self.unscaledSprite, pixelSize / 2048)
        rect = pygame.Rect(offset[0] + position[0] * pixelSize, offset[1] + position[1] * pixelSize, pixelSize, pixelSize)
        screen.blit(scaledSprite, rect)