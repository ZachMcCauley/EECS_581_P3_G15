# A rudimentary file replicating Vector2 in Unity
# I use this instead of tuples because I can add functions to add and subtract
import math

class Vector2Int:
    def __init__(self, x, y):
        if not (isinstance(x, int) and isinstance(y, int)):
            raise TypeError("Vector2Int requires two integers!")
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector2Int(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector2Int(self.x - other.x, self.y - other.y)
    def __mul__(self, other):
        return Vector2Int(self.x * other, self.y * other)
    def __truediv__(self, other):
        return Vector2Int(self.x / other, self.y / other)
    def __str__(self):
        return f"<{self.x}, {self.y}>"
    def __repr__(self):
        return f"Vector2Int({self.x}, {self.y})"
    def __hash__(self):
        return hash((self.x, self.y))
    def SqrMagnitude(self):
        return self.x ** 2 + self.y ** 2
    def Magnitude(self):
        return math.sqrt(self.SqrMagnitude())
    def IsAdjacentTo(self, other):
        return 1 == (self - other).SqrMagnitude()
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