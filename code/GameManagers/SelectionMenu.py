from GameManagers.GameManager import GameManager

class SelectionMenu(GameManager):
    def __init__(self, screen, fps):
        super().__init__(screen, fps)
        self.hoveredRect = "NONE"
        self.buttons = dict()
    def RunInternal(self) -> None:
        super().RunInternal()
        # Render the title screen.
        self.Render()
    def ProcessInputs(self) -> None:
        self.hoveredRect = "NONE"
        for buttonKey in self.buttons.keys():
            if self.buttons[buttonKey].IsHoveringOver():
                self.hoveredRect = buttonKey
                break
        super().ProcessInputs()