from discord.ext import commands

from game import Game
# from cls.util import GameError

from private_data import TOKEN, ADMIN_IDS   # bot token, Discord user ID

CTX = commands.Context      # type alias

BOT_PREFIX = ("!")          # iterable of str

client = commands.Bot(command_prefix=BOT_PREFIX)

def is_admin():
    def pred(ctx: CTX) -> bool:
        return ctx.message.author.id in ADMIN_IDS
    return commands.check(pred)

class ResBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.g = None       # Type[Game] when in progress, else None

    @commands.command(
        name="end",
        description="Admin only. Ends current game."
        )
    @is_admin()
    async def end(self, ctx: CTX) -> None:
        self.g = None
        await ctx.send("The game has ended.")

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

@client.command(
    name="kill",
    description="Kills the bot. Admin only."
    )
@is_admin()
async def kill(ctx: CTX) -> None:
    print(f"!kill command sent by admin {ctx.message.author.name}.")
    await client.logout()

client.add_cog(ResBot(client))

if __name__ == "__main__":
    client.run(TOKEN)
