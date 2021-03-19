class Caseless:
    def __init__(self, iter):
        self.iter = iter

    def __contains__(self, item):
        return item.casefold() in [i.casefold() for i in self.iter]
