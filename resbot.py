from discord.ext import commands

import game
import privdata # not in repo for security
import command_descriptions as cd
import long_messages as lm
from classes import *

BOT_PREFIX = ("!")
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

    @commands.command(**cd.new_desc)
    async def new_game(self, ctx):
        if self.g:
            await ctx.send(lm.gameinprog)
        else:
            self.g = game.Game()
            await ctx.send(lm.newgamestarted)
            print(lm.log_newgame)

    @commands.command(**cd.end_desc)
    @is_me()
    async def end_game(self, ctx):
        self.g = None
        await ctx.send("Game over, fools.")
        print("Game ended by admin.")

    @commands.command(**cd.join_desc)
    async def join_game(self, ctx):
        sender = ctx.message.author
        if not self.g:
            await ctx.send(lm.nogame)
        elif self.g.has_started:
            await ctx.send(lm.gameinprog)
        elif str(sender) in self.g.players:
            await sender.send("You already joined this game, %s!" % sender.name)
        elif len(self.g.players) >= self.g.MAXPLAYERS:
            await ctx.send(lm.playermax)
        else:
            self.g.add_player(Player(name=str(sender)))
            self.g.assign_nick(str(sender), sender.name) # strip ID#
            self.g.unready_all_players()
            await ctx.send("Joined! Current players are: " + self.g.list_players_str())
            if len(self.g.players) >= self.g.MINPLAYERS:
                await ctx.send(lm.enoughplayers)
            print("Player joined game. Player list: " + self.g.list_players_str())

    @commands.command(**cd.nick_desc)
    async def change_nick(self, ctx, *, new_nick):
        sender = ctx.message.author
        if not self.g:
            pass
        elif str(sender) not in self.g.players:
            await sender.send("Error: You are not in this game.")
            print(lm.log_notingame.format(str(sender), ctx.message.content))
        elif new_nick in list(self.g.nick_dict.values()):
            await sender.send("That nickname is already in use.")
        else:
            print(self.g.nick_dict)
            self.g.assign_nick(str(sender), new_nick)
            await ctx.send("{0} is now '{1}'".format(str(sender), new_nick))

    @commands.command(**cd.ready_desc)
    async def ready(self, ctx):
        sender = ctx.message.author
        if not self.g:
            pass
        elif str(sender) not in self.g.players:
            await sender.send("Error: You are not in this game.")
            print(lm.log_notingame.format(str(sender), ctx.message.content))
        elif str(sender) in self.g.ready_players:
            await sender.send("You're already ready!")
            print("User {0} is already ready.".format(str(sender)))
        else:
            self.g.ready_players.append(str(sender))
            if len(self.g.players) < self.g.MINPLAYERS:
                await ctx.send(lm.notenough)
            elif self.g.check_all_ready():
                await ctx.send(lm.readytostart.format(self.g.list_special_roles()))
            else:
                n, t = len(self.g.ready_players), len(self.g.players)
                await ctx.send("{0}/{1} players are ready.".format(n, t))

    @commands.command(**cd.setroles_desc) # change "!begin" > "!ready" in !join
    async def set_roles(self, ctx, *, role_list):
        if self.g:
            self.g.interpret_roles([char.lower() for char in role_list
                                    if char.lower() in "mpgdo"])
            await ctx.send(lm.listroles + self.g.list_special_roles())

    @commands.command(**cd.status_desc)
    async def status(self, ctx):
        if not self.g:
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
