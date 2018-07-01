from random import shuffle
from constants import *
from classes import Number, Role, Player

class GameError(Exception):
    pass

class Game:
    MINPLAYERS = Number.MINPLAYERS
    MAXPLAYERS = Number.MAXPLAYERS

    def __init__(self):
        self.players = {}           # dict {name#id: <Player obj>} in the game
        self.ids = {}               # dict of {name#id: ID_number}
        self.has_started = False    # True when it's too late to join game
        self.ready_players = []     # list of name#id players ready to start
        self.number = None          # holds Number object, see classes.Number
        self.order = []             # turn order
        self.nick_dict = {}         # in-game nicknames
        self.unique_num = 0         # use .get_unique_num() to get a unique #
        self.special_roles = []     # list of Avalon roles in game
        self.all_roles = []         # list of all roles in game
        self.current_status = 0     # see .get_status() for handler

    def get_unique_num(self):
        # always returns a unique number for the current game
        self.unique_num += 1
        return self.unique_num

    def add_player(self, sender):
        '''Takes a discord.py User obj and:
        * Adds player to self.players as {name#id: <Player obj>} dict entry
        * Adds ID# to self.ids as {name#id: Int Discord_Unique_ID} dict entry
        * Assigns name w/o ID as default nick (e.g. wugs instead of wugs#1234)

        Note: name#id means visible, e.g. wugs#1234, whereas Discord_Unique_ID
        refers to the internal longform ID number used by Discord. This is used
        to send PMs to specific users instead of the global chat.'''

        self.players[str(sender)] = Player(name=str(sender))
        self.ids[str(sender)] = sender.id
        self.assign_nick(str(sender), sender.name)

    def remove_player(self, sender):
        if self.has_started:
            raise GameError("Cannot remove player from game in progress!")
        del self.players[str(sender)]
        del self.ids[str(sender)]
        del self.nick_dict[str(sender)]

    def link_id(self, user, id):
        self.ids[user] = id

    def list_players(self):
        return [self.get_nick(name) for name in self.players]

    def list_players_str(self):
        tmp = self.list_players()
        return "None" if tmp == [] else ", ".join(tmp)

    def check_all_ready(self):
        return set([name for name in self.players]) == set(self.ready_players)

    def check_num_players(self):
        return Game.MINPLAYERS <= len(self.players) <= Game.MAXPLAYERS

    def unready_all_players(self):
        self.ready_players = []

    def assign_nick(self, full_name, nick_name):
        if full_name not in self.players:
            pass
        elif nick_name in list(self.nick_dict.values()):
            self.nick_dict[full_name] = nick_name + str(self.get_unique_num())
        else:
            self.nick_dict[full_name] = nick_name

    def get_nick(self, full_name):
        if full_name not in self.nick_dict:
            return full_name
        else:
            return self.nick_dict[full_name]

    def interpret_roles(self, rlist):
        self.special_roles = []     # reset the list
        if 'm' in rlist:            # if you add Merlin you must add Assassin
            self.special_roles.extend([MERLIN, ASSASSIN])
            if 'p' in rlist:        # only use Perc if you have Merlin
                self.special_roles.append(PERCIVAL)
                if 'g' in rlist:    # only use Morgana if you have Perc
                    self.special_roles.append(MORGANA)
            if 'd' in rlist:        # only use Mord if you have Merlin
                self.special_roles.append(MORDRED)
        if 'o' in rlist:            # no restriction on Oberon
            self.special_roles.append(OBERON)

    def list_special_roles(self):
        tmp = ", ".join(self.special_roles)
        return tmp if tmp != "" else "None"

    def generate_roles(self):
        '''uses self.special_roles (a list of up to five optional roles)
        and self.number (object that handles the numbers of types of players)
        to generate a list of all roles in game'''
        def role_swap(lst, search_for, replace_with):
            for i, val in enumerate(lst):
                if val == search_for:
                    lst[i] = replace_with
                    return lst # only replace the first instance
            return -1 # if search_for wasn't found in lst
        result = [VANSPY] * self.number.spies + [VANRES] * self.number.res
        if MERLIN in self.special_roles:
            result = role_swap(result, VANRES, MERLIN)
            result = role_swap(result, VANSPY, ASSASSIN)
        if PERCIVAL in self.special_roles:
            result = role_swap(result, VANRES, PERCIVAL)
        if MORGANA in self.special_roles:
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
            else:
                pass # don't throw an error, just ignore Oberon
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
        shuffle(self.all_roles) # hide the role order info from assignment

    async def private_info(self, user, role):
        '''async function to send each player their relevant private
        information given their particular role in the game.
        Takes a discord.py User object and a Role object.'''
        await user.send("You are " + str(role))
        if role.can_see_spies:
            if role.is_res:         # Merlin
                known_spies = [self.get_nick(pl) for pl in self.players
                                if self.players[pl].role.spy_seen_by_merl]
            else:                   # fellow (non-Oberon) spies
                known_spies = [self.get_nick(pl) for pl in self.players
                                if self.players[pl].role.spy_seen_by_spies]
            if len(known_spies) == 0:
                known_spies = ["None"]
            await user.send("The following players are SPIES: " +
                            ", ".join(known_spies))
        if role.can_see_merl:       # Percival
            merls = [self.get_nick(pl) for pl in self.players
                        if self.players[pl].role.looks_like_merl]
            if len(merls) == 1:     # no Morgana in game
                await user.send("MERLIN is " + merls[0])
            elif len(merls) == 2:   # Merlin and Morgana
                await user.send("MERLIN is either {0} or {1}".format(*merls))
            else:
                raise GameError("Invalid number of Merlin(s)/Morgana(s)")



    def show_order(self, sep=", "):
        return sep.join([self.get_nick(pl) for pl in self.order])

    def get_status(self): #### INCOMPLETE
        '''Returns the game state details at any given point as a string.'''
        status_dict = {
            0: "Game has not been started.",
            1: ""
        }
        return status_dict[self.current_status]
