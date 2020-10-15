from random import shuffle

from cls import GameError, Caseless, Number, Role, Player, Mission, Round
from constants import *     # replace * with explicit list once finalized

class Game:
    MINPLAYERS = Number.MINPLAYERS
    MAXPLAYERS = Number.MAXPLAYERS

    def __init__(self, chan):
        self.chan = chan            # holds messageable ABC for game in progress
        self.players = {}           # dict {name#id: <Player obj>} in the game
        self.ids = {}               # dict of {name#id: ID_number}
        self.has_started = False    # True when it's too late to join game
        self.ready_players = []     # list of name#id players ready to start
        self.number = None          # holds Number object, see classes.Number
        self.order = []             # ordered list for turn/leader order
        self.nick_dict = {}         # in-game nicknames
        self.special_roles = []     # list of Avalon roles in game
        self.all_roles = []         # list of all roles in game
        self.current_status = 0     # see Game.get_status() for handler
        self.missions = []          # ordered list of Mission objects
        self.li = 0                 # leader index, i.e. Game.order[li]
        self.need_team_vote = False # True=waiting for team approves/rejects
        self.has_voted = []         # reusable list for vote checking

    def add_mission(self, n, leader_index):
        if not (1 <= n <= 5):
            raise GameError("Invalid mission number: %s" % n)
        self.missions.append(Mission(n))
        self.missions[-1].add_round(leader_index)

    def add_player(self, sender):
        '''Takes a discord.py User obj and:
        * Adds player to self.players as {name#id: <Player obj>} dict entry
        * Adds ID# to self.ids as {name#id: Int Discord_Unique_ID} dict entry
        * Assigns name w/o ID as default nick (e.g. wugs instead of wugs#1234)

        Note: name#id means visible, e.g. wugs#1234, whereas Discord_Unique_ID
        refers to the internal longform ID number used by Discord. This is used
        to send PMs to specific users instead of the global chat.
        '''
        self.players[str(sender)] = Player(name=str(sender))
        self.ids[str(sender)] = sender.id
        self.assign_nick(str(sender), sender.name)

    def add_round(self):
        self.missions[-1].add_round(self.li)

    def assign_nick(self, full_name, nick_name):
        if full_name not in self.players:
            pass
        elif nick_name in Caseless(self.nick_dict.values()):
            raise GameError("Nick already in use. Defaulting to full name.")
        else:
            self.nick_dict[full_name] = nick_name

    def assign_team(self, team):
        team_full_names = [k for k, v in self.nick_dict.items()
                           if k in Caseless(team) or v in Caseless(team)]
        self.curr_round().make_team(team_full_names)
        self.need_team_vote = True

    def check_all_ready(self):
        return set([p for p in self.players]) == set(self.ready_players)

    def check_num_players(self):
        return Game.MINPLAYERS <= len(self.players) <= Game.MAXPLAYERS

    def curr_leader(self):
        return self.order[self.li]

    def curr_mission(self):
        if self.missions:
            return self.missions[-1]
        raise GameError("Game has not yet begun; no mission exists")

    def curr_round(self):
        if self.missions:
            return self.missions[-1].rounds[-1]
        raise GameError("Game has not yet begun; no mission exists")

    def curr_team(self):
        return self.curr_round().team

    def curr_team_size(self):
        return self.number.team_size(len(self.missions))

    def generate_roles(self):
        '''uses self.special_roles (a list of up to five optional roles)
        and self.number (object that handles the numbers of types of players)
        to generate a list of all roles in game
        '''
        def role_swap(lst, search_for, replace_with):
            '''A helper function that replaces the first instance of str
            search_for in list lst with new value str replace_with and returns
            the new modified lst. Returns -1 if search_for was not found in lst.
            '''
            for i, val in enumerate(lst):
                if val == search_for:
                    lst[i] = replace_with
                    return lst
            return -1
        roles = [VANSPY] * self.number.spies + [VANRES] * self.number.res
        if MERLIN in self.special_roles:
            roles = role_swap(roles, VANRES, MERLIN)
            roles = role_swap(roles, VANSPY, ASSASSIN)
        if PERCIVAL in self.special_roles:
            roles = role_swap(roles, VANRES, PERCIVAL)
        if MORGANA in self.special_roles:
            roles = role_swap(roles, VANSPY, MORGANA)
        if MORDRED in self.special_roles:
            if VANSPY in roles:
                roles = role_swap(roles, VANSPY, MORDRED)
            elif ASSASSIN in roles:
                roles = role_swap(roles, ASSASSIN, MORDASS)
            else:
                raise GameError("Invalid roles; wrong number of spies")
        if OBERON in self.special_roles:
            if VANSPY in roles:
                roles = role_swap(roles, VANSPY, OBERON)
            elif ASSASSIN in roles and MORDRED in roles:
                roles = role_swap(roles, MORDRED, MORDASS)
                roles = role_swap(roles, ASSASSIN, OBERON)
            else:
                print("Oberon role being ignored. Insufficient spies.")
        return roles

    def get_nick(self, full_name):
        if full_name not in self.nick_dict:
            return full_name
        else:
            return self.nick_dict[full_name]

    def get_status(self): #### INCOMPLETE
        '''Returns the game state details at any given point as a string.
        '''
        status_dict = {
            0: "Initialized",
            1: "example other status"
        }
        return status_dict[self.current_status]

    def inc_leader(self):       # after leader takes turn, increment index
        self.li += 1
        if self.li >= len(self.players):
            self.li = 0

    def interpret_roles(self, role_list):
        '''Takes a pre-formatted list of characters "mpgdo" (lowercase) and
        uses the games rules of The Resistance to determine the role list.
        For example, "pg" and "g" would return no special roles, becuase [m] for
        Merlin would also be required. That is, "mpg" would properly cause
        Game.special_roles to == ['Merlin', 'Assassin', 'Percival', 'Morgana']

TODO:   Allow pre-built named role lists instead of this clunky method.
        '''
        self.special_roles = []     # reset the game role list
        if 'm' in role_list:        # if you add Merlin you must add Assassin
            self.special_roles.extend([MERLIN, ASSASSIN])
            if 'p' in role_list:    # only use Perc if you have Merlin
                self.special_roles.append(PERCIVAL)
                if 'g' in role_list:    # only use Morgana if you have Perc
                    self.special_roles.append(MORGANA)
            if 'd' in role_list:    # only use Mord if you have Merlin
                self.special_roles.append(MORDRED)
        if 'o' in role_list:        # no restriction on Oberon
            self.special_roles.append(OBERON)

    def is_player(self, p):
        return (p in Caseless(self.players)
            or p in Caseless(self.nick_dict.values()))

    def list_all_roles(self):
        return ", ".join(self.all_roles)

    def list_mission_team(self):
        return [self.get_nick(name) for name in self.missions[-1].approved_team]

    def list_players(self):
        return [self.get_nick(name) for name in self.players]

    def list_players_str(self):
        tmp = self.list_players()
        return "None" if tmp == [] else ", ".join(tmp)

    def list_roles_verbose(self):
        tmp = []
        role_order = (MERLIN, PERCIVAL, MORGANA, MORDRED, MORDASS,
                      ASSASSIN, OBERON, VANRES, VANSPY)
        for r in role_order:
            if r in self.all_roles:
                x = r
                if r == VANRES:
                    n = self.all_roles.count(VANRES)
                    if n == 0:
                        x = "no other " + VANRES_PL
                    elif n == 1:
                        x = VANRES
                    else:
                        x = "{0} ".format(n) + VANRES_PL
                elif r == VANSPY:
                    n = self.all_roles.count(VANSPY)
                    if n == 0:
                        x = "no other " + VANSPY_PL
                    elif n == 1:
                        x = VANSPY
                    else:
                        x = "{0} ".format(n) + VANSPY_PL
                tmp.append(x)
        return ", ".join(tmp[:-1]) + " and " + tmp[-1]

    def list_special_roles(self):
        return ", ".join(self.special_roles) if self.special_roles else "None"

    def need_team(self):
        return len(self.curr_round().team) == 0

    def remove_player(self, sender):
        if self.has_started:
            raise GameError("Cannot remove player from game in progress!")
        del self.players[str(sender)]
        del self.ids[str(sender)]
        del self.nick_dict[str(sender)]

    def show_leader(self):
        return self.get_nick(self.curr_leader())

    def show_order(self, sep=", "):
        return sep.join([self.get_nick(pl) for pl in self.order])

    def show_team(self):
        return ", ".join([self.get_nick(p) for p in self.curr_team()])

    def start(self):
        '''Pretty self-explanatory. Starts the game, sets flags as such,
        initiates many starting values for later reference including turn order
        and assigning roles randomly using the random.shuffle function. Adds
        Mission 1 to the game, which itself creates Round 1.
        '''
        if self.has_started:
            raise GameError("Game has already started!")
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
        self.add_mission(1, self.li)

    def unready_all_players(self):
        self.ready_players = []

    async def private_info(self, user, role):
        '''async coroutine function to send each player their relevant private
        information given their particular role in the game.
        Takes a discord.py User model and a Role object.
        '''
        await user.send("You are " + str(role))
        if role.can_see_spies:
            if role.is_res:         # Merlin
                known_spies = [self.get_nick(pl) for pl in self.players
                                if self.players[pl].role.spy_seen_by_merl]
            else:                   # spy seeing fellow (non-Oberon) spies
                known_spies = [self.get_nick(pl) for pl in self.players
                                if self.players[pl].role.spy_seen_by_spies]
            if len(known_spies) == 0:
                known_spies = ["Unknown"]
            if self.number.spies > len(known_spies):
                known_spies.append("another unknown player")
            await user.send(
                "The following players are SPIES: " + ", ".join(known_spies))
        if role.can_see_merl:       # Percival
            merls = [self.get_nick(pl) for pl in self.players
                        if self.players[pl].role.looks_like_merl]
            if len(merls) == 1:     # no Morgana in game
                await user.send("MERLIN is " + merls[0])
            elif len(merls) == 2:   # Merlin and Morgana
                await user.send("MERLIN is either {0} or {1}".format(*merls))
            else:
                raise GameError('''Invalid number of Merlin(s)/Morgana(s).
                    Dumping: {0}'''.format(self.__dict__))
