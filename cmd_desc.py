new = {
    "name":         "new",
    "aliases":      ["new-game", "newgame", "new_game"],
    "brief":        "Starts a new game of The Resistance",
    "description":  "Starts a new game of The Resistance if there isn't already one in progress. Assigns the current channel as the game channel. This command cannot be sent via a private message."
}

end = {
    "name":         "end",
    "brief":        "Ends game in progress. Admin only.",
    "description":  "Immediately ends any game currently in progress. Admin only."
}

dump = {
    "name":         "dump",
    "brief":        "Prints a data-dump of the Game object. Admin only.",
    "description":  "Prints a Game.__dict__ string for debugging."
}

join = {
    "name":         "join",
    "brief":        "Joins an open game of The Resistance",
    "description":  "Sending this message to the bot will join you to a new game or let you know whether one is already in progress. Games must have between 5 and 10 players."
}

unjoin = {
    "name":         "unjoin",
    "brief":        "Unjoins a game you have joined",
    "description":  "Sending this message to the bot will unjoin you from a new game if roles have not yet been assigned. If the game has !start'd, it's too late to !unjoin."
}

kill = {
    "name":         "kill",
    "brief":        "Kills the bot. Painfully. Admin only.",
    "description":  "Kills the bot. Painfully. Admin-only command."
}

ready = {
    "name":         "ready",
    "brief":        "Tells the bot you are ready to start the game",
    "description":  "Command used after all players have !join'd the game to tell the bot that that player is ready to begin the game. Waits until all joined players are ready. If any new players join before the game starts, all players are un-!ready'd. Once all players are ready, starts the game."
}

nick = {
    "name":         "nick",
    "aliases":      ["change-nick", "change_nick"],
    "brief":        "Sets a player's nickname for the game",
    "description":  "Sets a player's own nickname for the duration of the current game. Prevents two users from having the same nickname."
}

roles = {
    "name":         "roles",
    "brief":        "Marks which roles from The Resistance: Avalon to include in the game",
    "description":  '''Use the command `!roles [M|P|G|D|O]` to set flags for:\n
    * [M]erlin: A member of the Resistance who knows all spies (except Mordred). Also adds an Assassin for the spies.\n
    * [P]ercival: A member of the Resistance who knows who Merlin is. Requires Merlin. Recommend adding Morgana for the spies.\n
    * Mor[G]ana: A spy who looks like Merlin to Percival. Requires Percival and Merlin.\n
    * Mor[D]red: A spy who is invisible to Merlin. Requires Merlin.\n
    * [O]beron: A spy who is invisible to other spies.\n\n
    Example: `!roles MPD` will create a game with [M]erlin, Assassin (added due to the rules of Merlin), [P]ercival, and Mor[D]red.'''
}

start = {
    "name":         "start",
    "brief":        "Starts game if all players are ready",
    "description":  "Starts the game if all players are ready. Will determine the roles in the game, decide a random turn order, distribute roles, and give players their private information."
}

team = {
    "name":         "team",
    "brief":        "Leader-only command to propose a team",
    "description":  '''Allows the current leader to propose a team. Team must contain the correct number of players according to the rules. The player sending the command must be the leader of the current mission's active round. Separate each name by a SPACE and no other characters.\n\n
    Example: `!team Bob Mary Sue` will propose a team of Bob, Mary, and Sue.'''
}

shoot = {
    "name":         "shoot",
    "brief":        "Assassin-only command to shoot Merlin",
    "description":  '''Allows the assassin to choose a target to shoot after the Resistance have won the majority of the missions. Their goal is to shoot Merlin, the member of the Resistance who knows the identity of the Spies and might have been too obvious with their leadership. If the assassin is correct, they win the game for the Spies. If they are incorrect, the Resistance wins the game as they have already won 3 missions.\n\n
    Example: `!shoot Tom` will win for the Spies if Tom is Merlin and win for the Resistance otherwise.'''
}

approve = {
    "name":         "approve",
    "brief":        "Votes to approve the proposed team",
    "description":  "Votes to approve the proposed team for the current round of this mission."
}

reject = {
    "name":         "reject",
    "brief":        "Votes to reject the proposed team",
    "description":  "Votes to reject the proposed team for the current round of this mission."
}

succeed = {
    "name":         "succeed",
    "aliases":      ["success", "pass"],
    "brief":        "Votes to succeed the current mission",
    "description":  "Votes to succeed the current mission. Must be on the mission team, and should be sent privately."
}

fail = {
    "name":         "fail",
    "brief":        "Votes to fail the current mission",
    "description":  "Votes to fail the current mission. Must be on the mission team, and should be sent privately."
}
