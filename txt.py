GAMEINPROG = "Game already in progress."
A_IS_B = "{0} is {1}"
A_ISNOW_B = "{0} is now {1}"

log = {
    "err": "User {0} is not in current game and used a command. Message: {1}",
    "nogame": "No game in progress",
    "new": "New game of The Resistance has been started.",
    "end": "Game ended by admin.",
    "join": "{0} added. Players: {1}", # {1} = Game.list_players_str
    "unjoin": "{0} left. Players: {1}",
    "nick": A_ISNOW_B,
    "nicks": "All nicks:\n{0}", # Game.nick_dict
    "start": "Game started. Order: {0}", # Game.show_order
    "team": "M{0}R{1}: Leader {2} proposes team {3}",
    "line": "----------\n",
    "user": "Logged in as: {0}",
    "id": "ID#: {0}",
    "kill": "Kill command sent by admin {0}"
}

new = {
    0: GAMEINPROG,
    1: "Please send that command again from the primary game channel, not a private chat.",
    2: "New game started! Send '!join' to join the game."
}

join = {
    0: "There is no game in progress. Send '!new' in the game channel to start a new game.",
    1: GAMEINPROG,
    2: "You've already joined this game!",
    3: "The maximum number of players have already joined. Please wait until next game or until someone leaves to play.",
    4: "{0} joined! Current players are: {1}", # {1} = Game.list_players_str
    5: "There are enough players to begin. When you are ready to start, each player should send '!ready'."
}

unjoin = {
    0: "Cannot unjoin from game in progress.",
    1: "{0} left. Current players are: {1}" # {1} = Game.list_players_str
}

nick = {
    0: "Invalid character in nickname: '{0}'. Please try again.",
    1: "Nickname '{0}' already in use.",
    2: A_ISNOW_B
}

ready = {
    0: "You're already ready!",
    1: "There aren't enough players to begin a game.",
    2: "All players are ready to begin.\n\nGame currently has the following special roles: {0}.\n\nUse `!roles <MPGDO>` to change these roles or `!help roles` for more info.\n\nAny player may send `!start` to begin the game.", # Game.list_special_roles()
    3: "{0}/{1} players are ready."
}

roles = {
    0: "Playing with the following special roles: {0}" # Game.list_special_roles
}

start = {
    0: A_IS_B,
    1: "Each player has been sent their private information. Please note that at this dev stage all EchoBot roles are public. The following roles were assigned this game: {0}", # Game.all_roles
    2: "*Player order* —\n**{0}**", # Game.show_order
    3: "The first leader is **{0}**. They can use `!team` to propose a team to go on the first mission or `!help team` for more info.", # Game.show_leader
    4: "The game is not ready to begin. Verify that all players are !ready and that the game has a valid number of players."
}

team = {
    0: "The current leader is {0}", # Game.get_nick(Game.curr_leader())
    1: "Unable to recognize these list items as players: {0}", # ", ".join(list)
    2: "Incorrect team size. {0} team members required.",
    3: "**Mission {0}, Round {1}:**\nLeader *{2}* has proposed the following team:\n\n{3}" # {0} = Game.missions[-1].n {1} = len(Game.missions[-1].rounds) {2} = Game.show_leader() # {3} = Game.show_team()
}
