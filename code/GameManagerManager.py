from GameManagers import GameplayManager

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
            if isinstance(manager, GameplayManager.GameplayManager): #effectively level control
                #base loss condition is the user loses after 10 moves if objective has not been completed
                #base win condition is the user must score four mail pieces
                manager.SetRequirements(10, {"piece_mail":4}) #sets the win and loss conditions for the level
            manager.Run()
            if manager.EndedInQuit:
                print("Game Manager Ended By User Quit. Program should terminate now.")
                break
            if not manager.inGameLoop:
                # Repeat multiple times if necessary. By default, will repeat once
                for i in range(manager.removeFromStack):
                    self.managerStack.pop()