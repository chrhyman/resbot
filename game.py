from random import shuffle
from constants import *
from classes import Numbers, Role, Player, Team, Vote

class Game:
    MINPLAYERS = Numbers.MINPLAYERS
    MAXPLAYERS = Numbers.MAXPLAYERS

    def __init__(self):
        self.players = {} # dict of {name: <Player object>} who are in the game
        self.has_started = False # set to True when it's too late to join game
        self.ready_players = []
        self.number = None
        self.order = []

    def add_player(self, player):
        self.players[player.name] = player # overwrites if duplicate name

    def list_players(self):
        return [name for name in self.players]

    def list_players_str(self):
        return ", ".join(self.list_players())

    def check_all_ready(self):
        return set(self.list_players()) == set(self.ready_players)

    def start(self):
        self.number = Number(len(self.players)) # change class Numbers to Number
        self.order = self.list_players()
        shuffle(self.order)
        self.has_started = True

    def get_status(self):
        '''Returns the game state details at any given point as a string.'''
        if not self.has_started:
            return "Game is waiting for all players to be ready. Current players: %s" % self.list_players_str()
        elif True: # flesh out as class methods develop
            return "Not yet implemented"
