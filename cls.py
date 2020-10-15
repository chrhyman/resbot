from constants import *     # replace * with explicit list once finalized

class GameError(Exception):
    '''Exception raised for any data state that represents a contradiction
    of the game rules for The Resistance. Player interface should error
    check for these possibilities.
    '''
    pass

class Caseless:
    '''Allows easy re-implementation of an iterable for checking if an item is
    in a list without respect to its Case i.e. .casefold()
    Designed for basically just this structure:
        string in Caseless([list, of, String, with, CASE]) => bool
    '''
    def __init__(self, iter):
        self.iter = iter

    def __contains__(self, item):
        return item.casefold() in [i.casefold() for i in self.iter]

class Number:
    '''Handles number of players, spies, resistance members, and team sizes, as
    well as number of fails needed for specific missions in those games.
    '''
    MINPLAYERS = 5
    MAXPLAYERS = 10
    def __init__(self, players):
        min, max = Number.MINPLAYERS, Number.MAXPLAYERS
        assert min <= players <= max, 'Error: Invalid player count'
        self.players = players
        self.maj = players // 2 + 1     # required to pass a team vote
        self.spies = -(-players // 3)
        self.res = players - self.spies

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

class Role:
    '''Takes a string from the constant ROLELIST and assigns appropriate flags.
    '''
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
        self.approved_team = []
        self.votes = {}
        self.winner = None      # "R" or "S"

    def __str__(self):
        out = "Mission {0}:".format(self.n)
        if len(self.rounds) != 0:
            for n, r in enumerate(self.rounds):
                out += "\n- Round {0}: {1}".format(n+1, r)
        if self.approved_team != []:
            out += "\n- Mission team: " + ", ".join(self.approved_team)
        if self.winner is not None:
            out += "\n- Winner: {0}".format(self.winner)
        return out

    def add_round(self, leader_index):
        if len(self.rounds) == 5:
            raise GameError("Last round was hammer! Can't add Round to Mission")
        self.rounds.append(Round(leader_index))

    def assign_team(self):
        cr = self.rounds[-1]
        if cr.approved:
            self.approved_team = cr.team

    def vote(self, player, verdict):
        if player in self.votes:
            raise GameError("%s has already voted" % player)
        self.votes[player] = verdict

class Round:
    def __init__(self, leader_index):
        self.li = leader_index
        self.team = []
        self.votes = {}         # dict of {<player>: boolean}
        self.approved = None    # True if approved, else False; None b4 tally

    def __str__(self):
        out = "Leader Index: " + str(self.li)
        if len(self.team) != 0:
            out += "; Team: "
            out += ", ".join(self.team)
        out += "; Votes: " + str(self.votes)
        out += "; Approved: {0}".format(self.approved)
        return out

    def make_team(self, team):
        if self.team:
            raise GameError("Team already defined for this Round.")
        self.team = team

    def vote(self, player, verdict):
        if player in self.votes:
            raise GameError("%s has already voted" % player)
        self.votes[player] = verdict
