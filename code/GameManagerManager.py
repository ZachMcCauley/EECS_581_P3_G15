from GameManagers import GameplayManager

class GameManagerManager:
    def __init__(self, screen, fps = 60):
        self.screen = screen
        self.fps = fps
        self.managerStack = []
    #extra arguments are passed to the manager (e.g. a level's moves and goal)
    def AddGameManager(self, manager, *args):
        gm = manager(self.screen, self.fps, *args)
        self.managerStack.append(gm)
        gm.SetOwner(self)
    def Run(self):
        while len(self.managerStack) > 0:
            # Get last element of manager stack
            manager = self.managerStack[-1]
            #level requirements are now set by the level screen when it starts gameplay (see Levels.py)
            manager.Run()
            if manager.EndedInQuit:
                print("Game Manager Ended By User Quit. Program should terminate now.")
                break
            if not manager.inGameLoop:
                # Repeat multiple times if necessary. By default, will repeat once
                for i in range(manager.removeFromStack):
                    self.managerStack.pop()