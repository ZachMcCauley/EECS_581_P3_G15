import os
import pygame

class ResourceManager:
    def __init__(self, path = "./Resources/Items"):
        self.resources = dict()
        ResourceManager.Instance = self
        for filename in os.listdir(path):
            noAffix = filename.split('.')[0]
            self.resources[noAffix] = pygame.image.load(f"{path}/{filename}").convert_alpha()
        self.cursorSprite = pygame.image.load("./Resources/Menu/Selector.png").convert_alpha()
        self.menuSprites = dict()
        self.menuSprites["PLAY"] = pygame.image.load("./Resources/Menu/PlayButton.png").convert_alpha()
        self.menuSprites["QUIT"] = pygame.image.load("./Resources/Menu/QuitButton.png").convert_alpha()
        self.menuSprites["TITLE"] = pygame.image.load("./Resources/Menu/Title.png").convert_alpha()
    def AllItemNames(self) -> list:
        return list(self.resources.keys())
    def GetItem(self, name) -> pygame.sprite.Sprite:
        return self.resources[name]
    def GetMenuSprite(self, name):
        return self.menuSprites[name]
    def GetMenuCursor(self):
        return self.cursorSprite