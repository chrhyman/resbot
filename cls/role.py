from dataclasses import dataclass

@dataclass
class Role:
    '''Base class for all Roles. Defaults all flags to False.'''
    role: str

    # flags for each team
    is_res: bool = False
    is_spy: bool = False

    # flags for special roles
    is_leader: bool = False
    is_shooter: bool = False
    is_hidden: bool = False
    is_blind: bool = False
    is_perceptive: bool = False

    def __str__(self):
        return self.role

class VanillaRes(Role):
    def __init__(self):
        super().__init__(
            role='a member of the RESISTANCE',
            is_res=True)
        self.plural = "members of the RESISTANCE"
        self.team = "the RESISTANCE"

class Merlin(Role):
    def __init__(self):
        super().__init__(
            role='Merlin',
            is_res=True,
            is_leader=True)

class Percival(Role):
    def __init__(self):
        super().__init__(
            role='Percival',
            is_res=True,
            is_perceptive=True)

class VanillaSpy(Role):
    def __init__(self):
        super().__init__(
            role='a SPY',
            is_spy=True)
        self.plural = "SPIES"
        self.team = "the SPIES"

class Assassin(Role):
    def __init__(self):
        super().__init__(
            role='Assassin',
            is_spy=True,
            is_shooter=True)

class Morgana(Role):
    def __init__(self):
        super().__init__(
            role='Morgana',
            is_spy=True,
            is_leader=True)

class Mordred(Role):
    def __init__(self):
        super().__init__(
            role='Mordred',
            is_spy=True,
            is_hidden=True)

class MordredAssassin(Role):
    '''Used when there are too few spies to separate Mordred and Assassin'''
    def __init__(self):
        super().__init__(
            role='Mordred the Assassin',
            is_spy=True,
            is_hidden=True,
            is_shooter=True)

class Oberon(Role):
    def __init__(self):
        super().__init__(
            role='Oberon',
            is_spy=True,
            is_blind=True)
