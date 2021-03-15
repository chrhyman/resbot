from random import shuffle

class Player:
    def __init__(self, discord_user):       # arg=discord.py User model object
        self.nameid = str(discord_user)     # str, 'discord_username#id'
        self.id = discord_user.id           # int, discord_unique_id for PMs
        self.nick = discord_user.name       # str, 'discord_username'
        self.role = None                    # Role object for this player
        self.ready = False                  # !ready sets to True
        self.needs_to_vote = False          # flag set by _
        self.has_voted = False              # flag set by _
        self.needs_team = False             # flag set by _

    def __str__(self):
        return self.nick

class PlayerList(list):
    def __contains__(self, player_str):
        if isinstance(self.get_player(player_str), Player):
            return True
        return False

    def __str__(self):
        return self.show(', ')

    def show(self, delimiter):
        return delimiter.join([str(p) for p in self])

    def get_player(self, player_str):
        for player in self:
            matches = [player.nameid, str(player.id), player.nick]
            if player_str.casefold() in [n.casefold() for n in matches]:
                return player
        return None

    def shuffle(self):
        shuffle(self)

class GamePlayerList(PlayerList):
    def __init__(self, lst=[]):
        super().__init__(lst)
        self.leader = 0

    def show(self, delimiter):
        names = []
        for i in range(len(self)):
            name = str(self[i])
            if self.leader == i:
                name = f"*{name}*"
            names.append(name)
        return delimiter.join(names)

# TEMPORARY
class DU:
    ID = 0
    def __init__(self, name):
        self.name = name
        self.id = DU.ID
        DU.ID += 1

    def __str__(self):
        return f"{self.name}#{self.id}"
