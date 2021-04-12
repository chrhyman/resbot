class Caseless:
    '''Uses .casefold() to implement `in` without regards to case
    '''
    def __init__(self, iter):
        self.iter = iter

    def __contains__(self, item):
        return item.casefold() in [i.casefold() for i in self.iter]

class GameError(Exception):
    '''An exception specific to this package. To be caught with try-except.
    '''
    pass
