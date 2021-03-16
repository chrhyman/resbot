from cls.player import Player, PlayerList, GamePlayerList

class Game:
    def __init__(self, channel):
        self.chan = channel     # Discord messageable ABC
        self.players = GamePlayerList()
        self.number = None
