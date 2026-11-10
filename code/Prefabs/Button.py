import pygame

class Button:
    def __init__(self, sprite, rect = pygame.Rect(0, 0, 0, 0), matchWidth = True):
        self.sprite = sprite
        self.rect = rect
        self.matchWidth = matchWidth
    def Render(self, screen):
        scale = None
        if self.matchWidth:
            scale = self.rect.width / self.sprite.get_width()
        else:
            scale = self.rect.height / self.sprite.get_height()
        screen.blit(pygame.transform.scale_by(self.sprite, scale), self.rect)
    def SetRect(self, rect):
        self.rect = rect
    def IsHoveringOver(self) -> bool:
        mousePos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mousePos)