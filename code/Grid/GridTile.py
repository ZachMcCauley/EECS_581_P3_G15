import pygame

G_SIZE = 10

class GridTile:
    def __init__(self, position):
        self.position = position
        self.item = None
    def IsAdjacentTo(self, other):
        return (self.position - other.position).SqrMagnitude() == 1
    def Render(self, screen):
        rect = pygame.Rect(self.position[0] * G_SIZE, self.position[1] * G_SIZE, G_SIZE, G_SIZE)
        pygame.draw.rect(screen, (255, 255, 255), rect)