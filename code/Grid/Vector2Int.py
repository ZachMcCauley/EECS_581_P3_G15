# A rudimentary file replicating Vector2Int in Unity
# I use this instead of tuples because I can add functions to add and subtract
from Grid.Vector2 import Vector2

class Vector2Int(Vector2):
    def __init__(self, x, y):
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError("Vector2Int requires two integers!")
        super().__init__(x, y)
    def __add__(self, other):
        return Vector2Int(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector2Int(self.x - other.x, self.y - other.y)
    def __mul__(self, other):
        return Vector2Int(int(self.x * other), int(self.y * other))
    def __truediv__(self, other):
        return Vector2Int(self.x // other, self.y // other)
    def __repr__(self):
        return f"Vector2Int({self.x}, {self.y})"
    @staticmethod
    def Zero():
        return Vector2Int(0, 0)
    @staticmethod
    def One():
        return Vector2Int(1, 1)
    @staticmethod
    def Up():
        return Vector2Int(0, 1)
    @staticmethod
    def Down():
        return Vector2Int(0, -1)
    @staticmethod
    def Left():
        return Vector2Int(-1, 0)
    @staticmethod
    def Right():
        return Vector2Int(1, 0)