import os
import pygame

class ResourceManager:
    def __init__(self, path = "./Resources/Items"):
        self.resources = dict()
        ResourceManager.Instance = self
        for filename in os.listdir(path):
            noAffix = filename.split('.')[0]
            self.resources[noAffix] = pygame.image.load(f"{path}/{filename}").convert_alpha()
    def AllItemNames(self) -> list:
        return list(self.resources.keys())
    def GetItem(self, name) -> pygame.sprite.Sprite:
        return self.resources[name]