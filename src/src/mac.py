class mac:
    def __init__(self, scoreboard=None, mem=None):
        self.scoreboard = scoreboard
        self.mem = mem

    def calculate(self):
        self.scoreboard.mac_calc += 1