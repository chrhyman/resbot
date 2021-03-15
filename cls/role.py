import txt.roles as R

class Role:
    def __str__(self):
        return self.role

class Leader:
    pass

class Res(Role):
    pass

class VanRes(Res):
    def __init__(self):
        self.role = R.VANRES

class Merlin(Res, Leader):
    def __init__(self):
        self.role = R.MERLIN

class Percival(Res):
    def __init__(self):
        self.role = R.PERCIVAL

class Spy(Role):
    pass

class VanSpy(Spy):
    def __init__(self):
        self.role = R.VANSPY

class Shooter(Spy):
    pass

class Assassin(Shooter):
    def __init__(self):
        self.role = R.ASSASSIN

class Morgana(Spy, Leader):
    def __init__(self):
        self.role = R.MORGANA

class Hidden(Spy):
    pass

class Mordred(Hidden):
    def __init__(self):
        self.role = R.MORDRED

class MordAss(Hidden, Shooter):
    def __init__(self):
        self.role = R.MORDASS

class Oberon(Spy):
    def __init__(self):
        self.role = R.OBERON
