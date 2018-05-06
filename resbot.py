from discord.ext import commands

import game
import privdata # not in repo for security
import command_descriptions as cd
import long_messages as lm
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
            await ctx.send(lm.gameinprog)
        else:
            self.g = game.Game()
            self.game_in_progress = True
            await ctx.send(lm.newgamestarted)
            print(lm.log_newgame)

    @commands.command(**cd.end_desc)
    @is_me()
    async def end(self, ctx):
        self.g = None
        self.game_in_progress = False
        await ctx.send("Game over, fools.")
        print("Game ended by admin.")

    @commands.command(**cd.join_desc)
    async def join_game(self, ctx):
        sender = ctx.message.author.name
        if not self.game_in_progress:
            await ctx.send(lm.nogame)
        elif self.g.has_started:
            await ctx.send(lm.gameinprog)
        elif sender in self.g.players:
            await ctx.send("You have already joined this game, %s!" % sender)
        elif len(self.g.players) >= self.g.MAXPLAYERS:
            await ctx.send(lm.playermax)
        else:
            self.g.add_player(Player(name=sender))
            self.g.ready_players = [] # unready all players
            await ctx.send("Joined! Current players are: " + self.g.list_players_str())
            if len(self.g.players) >= self.g.MINPLAYERS:
                await ctx.send(lm.enoughplayers)
            print("Player joined game. Player list: " + self.g.list_players_str())

    @commands.command(**cd.ready_desc)
    async def ready(self, ctx):
        user = ctx.message.author
        if user.name not in self.g.list_players():
            await user.send("Error: You are not in this game.")
            print(lm.log_notingame.format(user.name, ctx.message.content))
        elif user.name in self.g.ready_players:
            await user.send("You're already ready!")
            print("User {0} is already ready.".format(user.name))
        else:
            self.g.ready_players.append(user.name)
            if len(self.g.players) < self.g.MINPLAYERS:
                await ctx.send(lm.notenough)
            elif self.g.check_all_ready():
                print("All are ready") # start the game / options
            else:
                n, t = len(self.g.ready_players), len(self.g.players)
                await ctx.send("{0}/{1} players are ready.".format(n, t))

    @commands.command(**cd.status_desc)
    async def status(self, ctx):
        if not self.game_in_progress:
            await ctx.send(lm.nogame)
        else:
            await ctx.send(self.g.get_status())

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
