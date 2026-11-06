# A rudimentary file replicating Vector2 in Unity
# I use this instead of tuples because I can add functions to add and subtract
import math

class Vector2:
    def __init__(self, x, y):
        if not (isinstance(x, (int, float)) and isinstance(y, (float, int))):
            raise TypeError("Vector2 requires two numbers!")
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)
    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)
    def __str__(self) -> str:
        return f"<{self.x}, {self.y}>"
    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    def __getitem__(self, index):
        match index:
            case 0:
                return self.x
            case 1:
                return self.y
            case _:
                raise IndexError(f"Index {index} out of range!")
    def SqrMagnitude(self) -> float:
        return self.x ** 2 + self.y ** 2
    def Magnitude(self) -> float:
        return math.sqrt(self.SqrMagnitude())
    def AsTuple(self) -> tuple:
        return (self.x, self.y)
    def AsList(self) -> list:
        return [self.x, self.y]
    @staticmethod
    def Zero():
        return Vector2(0, 0)
    @staticmethod
    def One():
        return Vector2(1, 1)
    @staticmethod
    def Up():
        return Vector2(0, 1)
    @staticmethod
    def Down():
        return Vector2(0, -1)
    @staticmethod
    def Left():
        return Vector2(-1, 0)
    @staticmethod
    def Right():
        return Vector2(1, 0)