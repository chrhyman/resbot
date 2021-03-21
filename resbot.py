from discord.ext import commands

from game import Game
# from cls.util import GameError

import privdata as pd       # not in repo for security
TOKEN = pd.TOKEN            # type str
ADMIN_IDS = pd.ADMIN_IDS    # iterable of type int

BOT_PREFIX = ("!")          # iterable of type str

client = commands.Bot(command_prefix=BOT_PREFIX)

def is_admin():
    def pred(ctx):
        return ctx.message.author.id in ADMIN_IDS
    return commands.check(pred)

class ResBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.g = None       # type Game when in progress

    @commands.command(name="end", description="Admin only. Ends current game.")
    @is_admin()
    async def end(self, ctx):
        self.g = None

#    @commands.command(**txt.command_descriptions["cmd"])
#    async def cmd(self, ctx, *, arg):
#        if self.g:
#            try:
#                data = self.g.process_command("cmd", ctx, arg)
#            except GameError as e:
#                await ctx.send(str(e))
#                return
#            await self.g.process_output(data)

@client.event
async def on_ready():
    print(f"New Session as {client.user.name}, ID# {client.user.id}.\n")

@client.event
async def on_message(message):
    '''Re-implements the on_message event so as to not ignore other bots.
    '''
    ctx = await client.get_context(message)
    await client.invoke(ctx)

@client.command(name="kill", description="Kills the bot. Admin only.")
@is_admin()
async def kill(ctx):
    print(f"!kill command sent by admin {ctx.message.author.name}.")
    await client.logout()

client.add_cog(ResBot(client))

if __name__ == "__main__":
    client.run(TOKEN)
