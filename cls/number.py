from cls.error import GameError

class Number:
    MIN = 5
    MAX = 10
    TOTAL_MISSIONS = 5
    TEAM_SIZE_MATRIX = [    # TEAM_SIZE_MATRIX[mission_number][n_players]
        [], # no mission 0
        [None, None, None, None, None, 2, 2, 2, 3, 3, 3], # mission 1
        [None, None, None, None, None, 3, 3, 3, 4, 4, 4], # mission 2
        [None, None, None, None, None, 2, 4, 3, 4, 4, 4], # mission 3
        [None, None, None, None, None, 3, 3, 4, 5, 5, 5], # mission 4
        [None, None, None, None, None, 3, 4, 4, 5, 5, 5], # mission 5
    ]

    def __init__(self, n_players):
        if not (Number.MIN <= n_players <= Number.MAX):
            raise GameError(f"Invalid number of players: {n_players}.")
        self.players = n_players
        self.majority = n_players // 2 + 1
        self.spy = -(-n_players // 3)       # 1/3 rounded up
        self.res = n_players - self.spy
        self.mission = 0

    def inc_mission(self):
        if self.mission >= Number.TOTAL_MISSIONS:
            raise GameError(f"Cannot exceed {Number.TOTAL_MISSIONS} missions")
        else:
            self.mission += 1

    def team_size(self):
        return Number.TEAM_SIZE_MATRIX[self.mission][self.players]

    def fails_needed(self):
        if self.mission == 4 and self.players >= 7:
            return 2
        else:
            return 1
