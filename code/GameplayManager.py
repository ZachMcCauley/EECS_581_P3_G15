from GameManager import GameManager
from Grid.Grid import Grid

class GameplayManager(GameManager):
    def __init__(self, screen, fps = 60):
        super().__init__(screen, fps)
        self.grid = Grid.FormFromDims((8, 8))
        # Percentage of the window that the grid occupies for rendering
        self.gridSpace = (0.6, 0.8)
    def RunInternal(self):
        super().RunInternal()
        self.grid.Render(self.screen, self.gridSpace)