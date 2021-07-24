from abc import ABC

class Role(ABC):
    '''Base class for all Roles'''
    def __str__(self):
        return self.role

    def is_res(self):
        return isinstance(self, Res)

    def is_spy(self):
        return isinstance(self, Spy)

    def is_leader(self):
        return isinstance(self, Leader)

    def is_shooter(self):
        return isinstance(self, Shooter)

    def is_hidden(self):
        return isinstance(self, Hidden)

    def is_blind(self):
        return isinstance(self, Blind)

    def is_percival(self):
        return isinstance(self, Percival)

    def is_merlin(self):
        return isinstance(self, Merlin)

class Leader(Role):
    '''Visible to Percival'''
    pass

class Res(Role):
    pass

class VanRes(Res):
    def __init__(self):
        self.role = 'a member of the RESISTANCE'

class Merlin(Res, Leader):
    '''Can see all (non-Hidden; i.e. Mordred) Spies'''
    def __init__(self):
        self.role = 'Merlin'

class Percival(Res):
    '''Can identify Leader(s), one of whom is Merlin'''
    def __init__(self):
        self.role = 'Percival'

class Spy(Role):
    '''Can see all (non-Blind; i.e. Oberon) Spies'''
    pass

class VanSpy(Spy):
    def __init__(self):
        self.role = 'a SPY'

class Shooter(Spy):
    '''Can attempt to shoot Merlin at the end of the game'''
    pass

class Assassin(Shooter):
    def __init__(self):
        self.role = 'Assassin'

class Morgana(Spy, Leader):
    '''Looks like Merlin (i.e. one of two Leaders) to Percival'''
    def __init__(self):
        self.role = 'Morgana'

class Hidden(Spy):
    '''Cannot be seen by Merlin'''
    pass

class Mordred(Hidden):
    def __init__(self):
        self.role = 'Mordred'

class MordredAssassin(Hidden, Shooter):
    def __init__(self):
        self.role = 'Mordred the Assassin'

class Blind(Spy):
    '''Cannot see or be seen by other Spies (but still visible to Merlin)'''
    pass

class Oberon(Blind):
    def __init__(self):
        self.role = 'Oberon'
