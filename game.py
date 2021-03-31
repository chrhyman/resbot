from cls.player import Player, PlayerList, GamePlayerList

class Game:
    def __init__(self, channel):
        self.chan = channel     # Discord messageable ABC
        self.players = PlayerList() # becomes GamePlayerList after game starts
        self.number = None
