class GameManagerManager:
    def __init__(self, screen, fps = 60):
        self.screen = screen
        self.fps = fps
        self.managerStack = []
    def AddGameManager(self, manager):
        gm = manager(self.screen, self.fps)
        self.managerStack.append(gm)
        gm.SetOwner(self)
    def Run(self):
        while len(self.managerStack) > 0:
            # Get last element of manager stack
            manager = self.managerStack[-1]
            manager.Run()
            if manager.EndedInQuit:
                print("Game Manager Ended By User Quit. Program should terminate now.")
                break
            if not manager.inGameLoop:
                self.managerStack.pop()