new_desc = {
    "name":         "new",
    "aliases":      ["new-game", "newgame"],
    "brief":        "Starts a new game of The Resistance",
    "description":  "Starts a new game of The Resistance if there isn't already one in progress."
}

end_desc = {
    "name":         "end",
    "brief":        "Immediately ends any game currently in progress. Admin only.",
    "description":  "Immediately ends any game currently in progress. Admin only."
}

join_desc = {
    "name":         "join",
    "brief":        "Joins a game of The Resistance",
    "description":  "Sending this message to the bot will join you to a new game or let you know whether one is already in progress. Games must have between 5 and 10 players."
}

unjoin_desc = {
    "name":         "unjoin",
    "brief":        "Unjoins a game you have joined.",
    "description":  "Sending this message to the bot will unjoin you from a new game if roles have not yet been assigned. If the game has !start'd, it's too late to !unjoin."
}

kill_desc = {
    "name":         "kill",
    "brief":        "Kills the bot. Painfully. Admin-only command.",
    "description":  "Kills the bot. Painfully. Admin-only command."
}

ready_desc = {
    "name":         "ready",
    "brief":        "Tells the bot you are ready to start the game.",
    "description":  "Command used after all players have !join'd the game to tell the bot that that player is ready to begin the game. Waits until all joined players are ready. If any new players join before the game starts, all players are un-!ready'd. Once all players are ready, starts the game."
}

status_desc = {
    "name":         "status",
    "brief":        "Gives the current game status.",
    "description":  "Returns the current game status. Depending on the game state, this may return various different types of messages."
}

nick_desc = {
    "name":         "nick",
    "aliases":      ["change-nick", "change_nick"],
    "brief":        "Sets a player's own nickname for the duration of the current game.",
    "description":  "Sets a player's own nickname for the duration of the current game. Prevents two users from having the same nickname."
}

setroles_desc = {
    "name":         "roles",
    "aliases":      ["set_roles", "set-roles", "setroles"],
    "brief":        "Marks which roles from The Resistance: Avalon to include in the game",
    "description":  '''Use the command '!roles [M|P|G|D|O]' to set flags for:\n
    * [M]erlin: A member of the Resistance who knows all spies (except Mordred). Also adds an Assassin for the spies.\n
    * [P]ercival: A member of the Resistance who knows who Merlin is. Requires Merlin. Recommend adding Morgana for the spies.\n
    * Mor[G]ana: A spy who looks like Merlin to Percival. Requires Percival and Merlin.\n
    * Mor[D]red: A spy who is invisible to Merlin. Requires Merlin.\n
    * [O]beron: A spy who is invisible to other spies.\n\n
    Example: "!roles MPD" will set flags for a game with Merlin, Assassin, Percival, and Mordred.'''
}

start_desc = {
    "name":         "start",
    "brief":        "Starts the game if all players are ready.",
    "description":  "Starts the game if all players are ready. Will determine the roles in the game, determine a random turn order, distribute roles, and inform players."
}
