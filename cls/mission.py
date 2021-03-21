from cls.round import Round, RoundList
from cls.vote import Vote
from cls.util import GameError

class Mission:
    def __init__(self, num):
        if not (1 <= num <= 5):
            raise GameError("Mission must be in range 1-5 inclusive.")
        self.num = num
        self.rounds = RoundList()
        self.approved_team = None
        self.mission_vote = Vote()
        self.outcome = None

    # TODO: determine what the __str__(self) method should do, if anything

class MissionList(list):
    pass

# methods to handle checking for needing teams, votes, etc.
