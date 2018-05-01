from constants import *
from classes import Numbers, Role, Player, Team, Vote

class Game:
    MINPLAYERS = Numbers.MINPLAYERS
    MAXPLAYERS = Numbers.MAXPLAYERS
    def __init__(self):
        self.players = {} # dict of {name: <Player object>} who are in the game
        self.chatlog = [] # list of message lists [time, name, message]
        self.has_started = False # set to True when it's too late to join game

    def add_player(self, player):
        self.players[player.name] = player # overwrites if duplicate name

    def add_message(self, time, name, message):
        self.chatlog.append([time, name, message])

    def list_players(self):
        return [name for name in self.players]

    def list_players_str(self):
        return ", ".join(self.list_players())
