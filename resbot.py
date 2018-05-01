from discord.ext import commands

import game
import privdata # not in repo for security
import command_descriptions as cd
from classes import *

BOT_PREFIX = ("!", "?")
TOKEN = privdata.TOKEN
ADMIN_ID = privdata.ADMIN_ID # wugs#8508

client = commands.Bot(command_prefix=BOT_PREFIX)

def is_me(): # decorator check function to verify that sender is ADMIN
    def pred(ctx):
        return ctx.message.author.id == ADMIN_ID
    return commands.check(pred)

class ResBotCommands:
    def __init__(self, bot):
        self.bot = bot
        self.g = None # holds Game object when in progress
        self.game_in_progress = False

    @commands.command(**cd.new_desc)
    async def new_game(self, ctx):
        if self.game_in_progress:
            await ctx.send("Game already in progress.")
        else:
            self.g = game.Game()
            self.game_in_progress = True
            await ctx.send("New game started! Send '!join' to join the game.")
            print("New game of The Resistance has been started.")

    @commands.command(**cd.join_desc)
    async def join_game(self, ctx):
        sender = ctx.message.author.name
        if not self.game_in_progress:
            await ctx.send("There is no game to join. Send '!new' to start a new game.")
        elif self.g.has_started:
            await ctx.send("Game has already started. Please wait for a new game to join.")
        elif sender in self.g.players:
            await ctx.send("You have already joined this game, %s!" % sender)
        elif len(self.g.players) >= self.g.MAXPLAYERS:
            await ctx.send("The maximum number of players have already joined. Please wait until next game to play.")
        else:
            self.g.add_player(Player(name=sender))
            await ctx.send("Joined! Current players are: " + self.g.list_players_str())
            if len(self.g.players) >= self.g.MINPLAYERS:
                await ctx.send("There are enough players to begin! When you are ready to start, each player should send '!begin'. Roles will be assigned once everyone is ready.")
            print("Player joined game. Player list: " + self.g.list_players_str())

@client.event
async def on_ready():
    print('Logged in as: %s' % client.user.name)
    print('ID#: %d' % client.user.id)
    print('----------')

@client.command(**cd.kill_desc)
@is_me()
async def kill(ctx):
    await ctx.send("brutal.")
    print("Kill command sent by admin.")
    await client.logout()

client.add_cog(ResBotCommands(client))
client.run(TOKEN)
