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
    1: "Each player has been sent their private information. Please note that at this dev stage all EchoBot roles are public.\n\nThe following roles were assigned this game: {0}", # Game.all_roles
    2: "*Player order* —\n**{0}**", # Game.show_order('[delimiter]')
    3: "The first leader is **{0}**. They can use `!team <names separated by spaces>` to propose a team to go on the first mission or `!help team` for more info.", # Game.show_leader
    4: "The game is not ready to begin. Verify that all players are !ready and that the game has a valid number of players.",
    5: GAMEINPROG
}

team = {
    0: "The current leader is {0}", # Game.show_leader()
    1: "Unable to recognize these list items as players: {0}", # ", ".join(list)
    2: "Incorrect team size. {0} team members required but you provided {1}.",
    3: "**Mission {0}, Round {1}:**\nLeader *{2}* has proposed the following team:\n{3}", # {0} = Game.missions[-1].n {1} = len(Game.missions[-1].rounds) {2} = Game.show_leader() # {3} = Game.show_team()
    4: "You've already proposed a team for this round.",
    5: "All players should now vote for whether you `!approve` or `!reject` this team. It is recommended to vote privately so all votes can be made public simultaneously, at the end of the round."
}

team_vote = {
    0: "You've already voted!",
    1: "{0}/{1} votes received.",
    2: "{1}{0}{1} voted *{2}*.", # {1} = "**" if on team to bold name, else empty string
    3: "Leader *{0}'s* team (**{1}**) has been approved for the mission!\n\nThe mission team has been selected! Each mission team member should now *privately* message their vote: `!succeed` or `!fail`. Once all votes have been submitted, the results of the mission will be displayed here. **Votes will not be made public.**",
    4: "Leader *{0}'s* team (**{1}**) was rejected.",
    5: "The next leader is ***{0}***. They can use `!team <names separated by spaces>` to propose a team to go on the mission or `!help team` for more info.",
    6: "All votes have been received and will now be revealed.",
    7: "**Hammer** warning: The fourth team was just rejected for this mission. The next leader will have a chance to create a fifth team (known as the 'hammer'). If this team is also rejected, the SPIES will automatically win the game!",
    8: "The SPIES have infiltrated the democratic workings of the RESISTANCE and dismantled them from within. They have sown discord such that no agreement could be reached among members of the RESISTANCE on how to proceed with their mission.\n\n**THE SPIES WIN!**"
}

mission_vote = {
    0: "The team for this mission hasn't been approved yet.",
    1: "You aren't on the mission team.",
    2: "You've already voted on this mission outcome. You can't change your mind now.",
    3: "You can't vote for this mission to fail because you're a member of the RESISTANCE. Your vote has been changed to a mission success. Also, stop trying to break the rules!",
    4: "The approved team has completed their mission. The outcome is now being determined."
}
