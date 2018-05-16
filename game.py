from random import shuffle
from constants import *
from classes import Number, Role, Player, Team, Vote

class GameError(Exception):
    pass

class Game:
    MINPLAYERS = Number.MINPLAYERS
    MAXPLAYERS = Number.MAXPLAYERS

    def __init__(self):
        self.players = {} # dict of {name#id: <Player object>} who are in the game
        self.has_started = False # set to True when it's too late to join game
        self.ready_players = [] # list of name#id players who are ready to start
        self.number = None # holds the Number object, see classes.Number
        self.order = [] # turn order
        self.nick_dict = {} # in-game nicknames
        self.unique_num = 0 # use .get_unique_num() method to generate a Unique#
        self.special_roles = []
        self.all_roles = []

    def get_unique_num(self):
        # always returns a unique number for the current game
        self.unique_num += 1
        return self.unique_num

    def add_player(self, player):
        self.players[player.name] = player # overwrites if duplicate name

    def list_players(self):
        return [self.swap_names(name) for name in self.players]

    def list_players_str(self):
        return ", ".join(self.list_players())

    def check_all_ready(self):
        return set([name for name in self.players]) == set(self.ready_players)

    def unready_all_players(self):
        self.ready_players = []

    def assign_nick(self, full_name, nick_name):
        if full_name not in self.players:
            pass
        elif nick_name in list(self.nick_dict.values()):
            self.nick_dict[full_name] = nick_name + str(self.get_unique_num())
        else:
            self.nick_dict[full_name] = nick_name

    def swap_names(self, full_name):
        if full_name not in self.nick_dict:
            return full_name
        else:
            return self.nick_dict[full_name]

    def generate_roles(self):
        '''uses self.special_roles (a list of up to four optional roles)
        and self.number (object that handles the numbers of types of players)
        to generate a list of all roles in game'''
        def role_swap(l, search_for, replace_with):
            for i, val in enumerate(l):
                if val == search_for:
                    l[i] = replace_with
                    return l # only replace the first instance
            return -1 # if search_for wasn't found in l
        result = [VANSPY] * self.number.getSpies() + [VANRES] * self.number.getRes()
        if MERLIN in self.special_roles:
            result = role_swap(result, VANRES, MERLIN)
            result = role_swap(result, VANSPY, ASSASSIN)
        if PERCIVAL in self.special_roles:
            result = role_swap(result, VANRES, PERCIVAL)
            result = role_swap(result, VANSPY, MORGANA)
        if MORDRED in self.special_roles:
            if VANSPY in result:
                result = role_swap(result, VANSPY, MORDRED)
            elif ASSASSIN in result:
                result = role_swap(result, ASSASSIN, MORDASS)
            else:
                raise GameError("Invalid roles; wrong number of spies")
        if OBERON in self.special_roles:
            if VANSPY in result:
                result = role_swap(result, VANSPY, OBERON)
            elif ASSASSIN in result and MORDRED in result:
                result = role_swap(result, MORDRED, MORDASS)
                result = role_swap(result, ASSASSIN, OBERON)
        return result

    def start(self): #### IN PROGRESS
        self.has_started = True
        self.number = Number(len(self.players))
        self.order = [name for name in self.players] # with ID#
        shuffle(self.order)
        self.all_roles = self.generate_roles()
        self.special_roles = [r for r in self.all_roles if r not in VANROLES]
        shuffle(self.all_roles)
        for i, player in enumerate(self.order):
            self.players[player].assign_role(self.all_roles[i])
        # shuffle(self.all_roles) # hide this information

    def get_status(self): #### INCOMPLETE
        '''Returns the game state details at any given point as a string.'''
        if not self.has_started:
            return "Game is waiting for all players to be ready. Current players: %s" % self.list_players_str()
        elif True: # flesh out as class methods develop
            return "Not yet implemented"
