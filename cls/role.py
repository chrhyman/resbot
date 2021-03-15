import txt.roles as R

class Role:
    def __str__(self):
        return self.role

class Res(Role):
    pass

class VanRes(Res):
    def __init__(self):
        self.role = R.VANRES

class Merlin(Res):
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
