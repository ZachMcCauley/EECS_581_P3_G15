class GridTile:
    def __init__(self, position):
        self.position = position
        self.item = None
    def IsAdjacentTo(self, other):
        return (self.position - other.position).SqrMagnitude() == 1