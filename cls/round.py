from cls.vote import Vote

class Round:
    def __init__(self, leader):
        self.leader = leader
        self.proposed_team = None
        self.team_vote = Vote()
        self.approved = None

class RoundList(list):
    pass
