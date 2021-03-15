import txt.roles as R

class Role:
    '''Base class for all Roles'''
    def __str__(self):
        return self.role

class Leader(Role):
    '''Visible to Percival'''
    pass

class Res(Role):
    pass

class VanRes(Res):
    def __init__(self):
        self.role = R.VANRES

class Merlin(Res, Leader):
    '''Can see all non-Hidden Spies'''
    def __init__(self):
        self.role = R.MERLIN

class Percival(Res):
    '''Can identify Leaders, one of whom is Merlin'''
    def __init__(self):
        self.role = R.PERCIVAL

class Spy(Role):
    '''Can see all non-Oberon Spies'''
    pass

class VanSpy(Spy):
    def __init__(self):
        self.role = R.VANSPY

class Shooter(Spy):
    '''Can attempt to shoot Merlin at the end of the game'''
    pass

class Assassin(Shooter):
    def __init__(self):
        self.role = R.ASSASSIN

class Morgana(Spy, Leader):
    '''Looks like Merlin to Percival'''
    def __init__(self):
        self.role = R.MORGANA

class Hidden(Spy):
    '''Cannot be seen by Merlin'''
    pass

class Mordred(Hidden):
    def __init__(self):
        self.role = R.MORDRED

class MordAss(Hidden, Shooter):
    def __init__(self):
        self.role = R.MORDASS

class Oberon(Spy):
    '''Cannot be seen by other Spies, but can be seen by Merlin'''
    def __init__(self):
        self.role = R.OBERON
