# TODO: turn this mess into a single dict where these are key:value pairs, jfc

newgamestarted = "New game started! Send '!join' to join the game."
log_newgame = "New game of The Resistance has been started."
nogame = "There is no game in progress. Send '!new' in the game channel to start a new game."
gameinprog = "Game already in progress."
wrongchannel = "Please send that command again from the primary game channel, not a private chat."
playermax = "The maximum number of players have already joined. Please wait until next game or until someone leaves to play."
enoughplayers = "There are enough players to begin. When you are ready to start, each player should send '!ready'."
log_notingame = "User {0} used a command without being in the current game. Message: {1}"
notenough = "There aren't enough players to begin a game."
listroles = "Playing with the following special roles: "
readytostart = "All players are ready to begin.\n\nGame currently has the following special roles: {0}. Use '!roles <MPGDO>' to change these roles or '!help roles' for more info.\n\nAny player may send '!start' to begin the game." # where {0} is Game.list_special_roles()
notreadytostart = "The game is not ready to begin. Verify that all players are !ready and that the game has a valid number of players."
sentprivinfo = "Each player has been sent their private information. Please note that at this dev stage all EchoBot roles are public. The following roles are in this game: {0}" # use Game.all_roles for list.
firstleader = "The first leader is **{0}**. They can use '!team' to propose a team to go on the first mission or '!help team' for more info."
proposed = "{0} has proposed the following team: {1}" # {1} is Game.show_team()
