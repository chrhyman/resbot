from constants import *

# class to handle number of players and quantities of them in game
class Numbers:
    MINPLAYERS = 5
    MAXPLAYERS = 10
    def __init__(self, players):
        min, max = Numbers.MINPLAYERS, Numbers.MAXPLAYERS
        assert min <= players <= max, 'Error: Must have {0}-{1} players.'.format(min, max)
        self.players = players

    def getSpies(self):     # 1/3 of all players are spies (round up)
        return -(-self.players//3)

    def getRes(self):       # all players that aren't spies are res
        return self.players - self.getSpies()

    def getTeamSize(self, mission):     # static from game rules
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
            assert False, 'Error: Mission number %s does not exist' % mission

    def getFailsNeeded(self, mission):  # mission 4 needs two fails with 7+
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
            self.isRes = True           # flag True for Res only
            self.canShoot = False       # flag True for Assassin
            self.spySeenBySpies = False # flag True for non-Oberon spies
            self.spySeenByMerl = False  # flag True for non-Mordred spies
            self.canSeeSpies = False    # flag True for Merlin and non-Ob spies
            self.looksLikeMerl = False  # flag True for Merlin and Morgana
            self.canSeeMerl = False     # flag True for Percival
            if self.role == MERLIN:
                self.canSeeSpies = True
                self.looksLikeMerl = True
            if self.role == PERCIVAL:
                self.canSeeMerl = True
        # spy roles
        if self.role in SPYROLES:
            self.isRes = False
            self.canShoot = False
            self.spySeenBySpies = True
            self.spySeenByMerl = True
            self.canSeeSpies = True
            self.looksLikeMerl = False
            self.canSeeMerl = False
            if self.role in (ASSASSIN, MORDASS):
                self.canShoot = True
            if self.role == MORGANA:
                self.looksLikeMerl = True
            if self.role in (MORDRED, MORDASS):
                self.spySeenByMerl = False
            if self.role == OBERON:
                self.spySeenBySpies = False
                self.canSeeSpies = False

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

class Team:
    pass

class Vote:
    pass
