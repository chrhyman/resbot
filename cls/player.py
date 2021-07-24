from random import shuffle
from typing import Optional, Union

from discord.abc import User

from cls.roles import Role
from cls.util import Caseless, GameError

class Player:
    def __init__(self, discord_user: User):
        self.discord_user = discord_user
        self.name = discord_user.name
        self.unique_name = str(discord_user)    # 'name#discriminator'
        self.nick = self.name                   # default to username
        self.role = None
        self.ready = False                      # flag for intializing the game

    def __str__(self):
        return self.nick

    def assign_role(self, role: Role) -> None:
        self.role = role

    def update_nick(self, new_nick: str) -> None:
        self.nick = new_nick

class PlayerList(list):
    def __contains__(self, pl: Union[Player, str]) -> bool:
        if self.get_player(pl) is not None:
            return True
        return False

    def __str__(self):
        return self.show(', ')

    def all_players_ready(self) -> bool:
        return all([player.ready for player in self])

    def change_nick(self, player_str: str, new_nick: str) -> None:
        if new_nick in self:
            raise GameError("That name is already in use")
        elif player_str not in self:
            raise GameError(f"Player not in game: {player_str}")
        else:
            self.get_player(player_str).update_nick(new_nick)

    def get_player(self, pl: Union[Player, str]) -> Optional[Player]:
        for player in self:
            if isinstance(pl, Player) and pl == player:
                return player
            matches = [player.name, player.unique_name , player.nick]
            if isinstance(pl, str) and pl in Caseless(matches):
                return player
        return None

    def show(self, delimiter: str) -> str:
        return delimiter.join([str(player) for player in self])

    def shuffle(self) -> None:
        shuffle(self)

    def unready_all_players(self) -> None:
        for player in self:
            player.ready = False

class GamePlayerList(PlayerList):
    def __init__(self, lst: Optional[list[Player]]=None):
        if lst is None:
            lst = []
        super().__init__(lst)
        self.leader = 0

    def show(self, delimiter: str) -> str:
        names = [str(p) for p in self]
        names[self.leader] = f"*{names[self.leader]}*"
        return delimiter.join(names)

    def shuffle(self):
        # order matters; don't call shuffle on GamePlayerList
        pass
