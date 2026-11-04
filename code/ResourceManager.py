import os
import pygame

class ResourceManager:
    def __init__(self, path):
        self.resources = dict()
        ResourceManager.Instance = self
        for filename in os.listdir(path):
            noAffix = filename.split('.')[0]
            self.resources[noAffix] = pygame.image.load(f"{path}/{filename}").convert_alpha()
    @staticmethod
    def GetResourceManager():
        if ResourceManager.Instance is None:
            return ResourceManager("./Resources/Items")
        else:
            return ResourceManager.Instance
    def __del__(self):
        if ResourceManager.Instance is self:
            ResourceManager.Instance = None
    def AllItemNames(self):
        return self.resources.keys()
    def GetItem(self, name):
        return self.resources[name]
    Instance = None