from constants import *

class GameError(Exception):
    '''Exception raised for any data state that represents a contradiction
    of the game rules for The Resistance. Player interface should error
    check for these possibilities.
    '''
    pass

class Caseless:
    def __init__(self, iter):
        self.iter = iter

    def __contains__(self, item):
        return item.casefold() in [i.casefold() for i in self.iter]

# handles number of players, spies, resistance, and team sizes/fails needed
class Number:
    MINPLAYERS = 5
    MAXPLAYERS = 10
    def __init__(self, players):
        min, max = Number.MINPLAYERS, Number.MAXPLAYERS
        assert min <= players <= max, 'Error: Invalid player count'
        self.players = players
        self.spies = self.get_spies()
        self.res = self.get_res()

    def get_spies(self):            # 1/3 of all players are spies (round up)
        return -(-self.players//3)

    def get_res(self):              # all players that aren't spies are res
        return self.players - self.spies

    def team_size(self, mission):   # static from game rules; mission is int
        if mission == 1:
            if self.players <= 7:   return 2
            else:                   return 3
        elif mission == 2:
            if self.players <= 7:   return 3
            else:                   return 4
        elif mission == 3:
            if self.players == 5:   return 2
            elif self.players == 7: return 3
            else:                   return 4
        elif mission == 4:
            if self.players <= 6:   return 3
            elif self.players == 7: return 4
            else:                   return 5
        elif mission == 5:
            if self.players == 5:   return 3
            elif self.players <= 7: return 4
            else:                   return 5
        else:
            assert False, 'Error: Mission %s does not exist' % str(mission)

    def fails_needed(self, mission):
        if mission == 4 and self.players >= 7:
            return 2
        else:
            return 1

# Role object sets appropriate flags when initialized with role type
class Role:
    def __init__(self, role):
        assert role in ROLELIST, 'Error: Role "%s" does not exist.' % role
        self.role = role
        # resistance roles
        if self.role in RESROLES:
            self.is_res = True              # True for Res only
            self.can_shoot = False          # True for Assassin
            self.spy_seen_by_spies = False  # True for non-Oberon spies
            self.spy_seen_by_merl = False   # True for non-Mordred spies
            self.can_see_spies = False      # True for Merlin & non-Ob spies
            self.looks_like_merl = False    # True for Merlin and Morgana
            self.can_see_merl = False       # True for Percival
            if self.role == MERLIN:
                self.can_see_spies = True
                self.looks_like_merl = True
            if self.role == PERCIVAL:
                self.can_see_merl = True
        # spy roles
        if self.role in SPYROLES:
            self.is_res = False
            self.can_shoot = False
            self.spy_seen_by_spies = True
            self.spy_seen_by_merl = True
            self.can_see_spies = True
            self.looks_like_merl = False
            self.can_see_merl = False
            if self.role in (ASSASSIN, MORDASS):
                self.can_shoot = True
            if self.role == MORGANA:
                self.looks_like_merl = True
            if self.role in (MORDRED, MORDASS):
                self.spy_seen_by_merl = False
            if self.role == OBERON:
                self.spy_seen_by_spies = False
                self.can_see_spies = False

    def __str__(self):
        return self.role

class Player:
    def __init__(self, name=None):
        self.name = name
        self.role = None

    def __str__(self):
        return self.name

    def assign_role(self, role):
        assert not self.role, "Role already defined as %s." % self.role
        self.role = Role(role)

class Mission:
    def __init__(self, n):
        assert 1 <= n <= 5, "Mission %s does not exist" % n
        self.n = n
        self.rounds = []  # if len(rounds) == 5, it's hammer
        self.winner = None      # "R" or "S"

    def add_round(self, leader_index):
        if len(self.rounds) == 5:
            # hammer
            return
        self.rounds.append(Round(leader_index))

class Round:
    def __init__(self, leader_index):
        self.li = leader_index
        self.team = []
        self.votes = {}         # dict of {<player>: boolean}
        self.approved = False   # True if team has been approved

    def make_team(self, team):
        if self.team:
            raise GameError("Team already defined for this Round.")
        self.team = team

    def vote(self, player, verdict):
        if player in self.votes:
            raise GameError("%s has already voted" % player)
        self.votes[player] = verdict
