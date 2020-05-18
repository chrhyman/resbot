from discord.ext import commands

import game
from classes import Caseless

import privdata                 # not in repo for security
TOKEN = privdata.TOKEN          # type str
ADMIN_IDS = privdata.ADMIN_IDS  # iterable of int admin IDs for @is_admin()

import command_desc
import txt

BOT_PREFIX = ("!")              # iterable

client = commands.Bot(command_prefix=BOT_PREFIX)

def is_admin():         # decorator check function verifies sender is ADMIN
    def pred(ctx):
        return ctx.message.author.id in ADMIN_IDS
    return commands.check(pred)

async def err_notingame(ctx):
    sender = ctx.message.author
    msg = ctx.message.content
    await sender.send("Error: You are not in this game.")
    print(txt.log["err"].format(str(sender), msg))

class ResBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.g = None       # holds Game object when in progress

    @commands.command(**command_desc.new)
    async def new(self, ctx):
        sender = ctx.message.author
        if self.g:
            await sender.send(txt.new[0])
        elif ctx.message.guild is None:
            await sender.send(txt.new[1])
        else:
            self.g = game.Game(ctx.channel) # sets current ctx as game channel
            await self.g.chan.send(txt.new[2])
            print(txt.log["new"])

    @commands.command(**command_desc.end)
    @is_admin()
    async def end(self, ctx):
        await ctx.send("Game over, fools.")
        if self.g and self.g.chan != ctx.channel:
            await self.g.chan.send("Game over, fools.")
        self.g = None
        print(txt.log["end"])

    @commands.command(**command_desc.dump)
    @is_admin()
    async def dump(self, ctx):
        if self.g is None:
            await ctx.send("No game exists.")
            return
        out = ["Dumping:", "Chan-{0}".format(repr(self.g.chan)), "Players-"]
        for pl in self.g.players:
            if self.g.players[pl].role is not None:
                out.append(
                    pl + " role: " + str(self.g.players[pl].role.role))
            out.append(
                pl + " id: " + str(self.g.ids[pl]))
        out.append("Order: " + ", ".join(self.g.order))
        out.append("Nicknames: " + str(self.g.nick_dict))
        out.append("All roles: " + ", ".join(self.g.all_roles))
        out.extend([str(m) for m in self.g.missions])
        print("\n".join(out))
        for l in out:
            await ctx.send(l + "\n")
        print(txt.log["line"])

    @commands.command(**command_desc.join)
    async def join(self, ctx):
        sender = ctx.message.author
        if not self.g:
            await sender.send(txt.join[0])
        elif self.g.has_started:
            await sender.send(txt.join[1])
        elif str(sender) in self.g.players:
            await sender.send(txt.join[2])
        elif len(self.g.players) >= self.g.MAXPLAYERS:
            await sender.send(txt.join[3])
        else:
            self.g.add_player(sender)   # add to game, link id, assign nick
            self.g.unready_all_players()
            await self.g.chan.send(
                txt.join[4].format(sender.name, self.g.list_players_str()))
            if len(self.g.players) >= self.g.MINPLAYERS:
                await self.g.chan.send(txt.join[5])
            print(txt.log["join"].format(
                sender.name, self.g.list_players_str()))

    @commands.command(**command_desc.unjoin)
    async def unjoin(self, ctx):
        sender = ctx.message.author
        if not self.g or str(sender) not in self.g.players:
            pass
        elif self.g.has_started:
            await sender.send(txt.unjoin[0])
        else:
            self.g.remove_player(sender)
            self.g.unready_all_players()
            await self.g.chan.send(txt.unjoin[1].format(
                sender.name, self.g.list_players_str()))
            print(txt.log["unjoin"].format(
                sender.name, self.g.list_players_str()))

    @commands.command(**command_desc.nick)
    async def nick(self, ctx, *, new_nick):
        sender = ctx.message.author
        if not self.g:
            pass
        elif str(sender) not in self.g.players:
            await err_notingame(ctx)
        elif '#' in new_nick:
            await sender.send(txt.nick[0].format('#'))
        elif new_nick in Caseless(self.g.nick_dict.values()):
            await sender.send(txt.nick[1].format(new_nick))
        else:
            self.g.assign_nick(str(sender), new_nick)
            await self.g.chan.send(txt.nick[2].format(str(sender), new_nick))
            print(txt.log["nick"].format(str(sender), new_nick))
            print(txt.log["nicks"].format(self.g.nick_dict))

    @commands.command(**command_desc.ready)
    async def ready(self, ctx):
        sender = ctx.message.author
        if not self.g:
            pass
        elif str(sender) not in self.g.players:
            await err_notingame(ctx)
        elif str(sender) in self.g.ready_players:
            await sender.send(txt.ready[0])
        else:
            self.g.ready_players.append(str(sender))
            if len(self.g.players) < self.g.MINPLAYERS:
                await self.g.chan.send(txt.ready[1])
            elif self.g.check_all_ready():
                await self.g.chan.send(
                    txt.ready[2].format(self.g.list_special_roles()))
            else:
                n, t = len(self.g.ready_players), len(self.g.players)
                await self.g.chan.send(txt.ready[3].format(n, t))

    @commands.command(**command_desc.roles)
    async def roles(self, ctx, *, role_list):
        if (self.g
        and not self.g.has_started
        and str(ctx.message.author) in self.g.players):
            proposed = [c.lower() for c in role_list if c.lower() in "mpgdo"]
            self.g.interpret_roles(proposed)
            await self.g.chan.send(
                txt.roles[0].format(self.g.list_special_roles()))

    @commands.command(**command_desc.start)
    async def start(self, ctx):
        if not self.g:
            pass
        elif self.g.has_started:
            await ctx.message.author.send(txt.start[5])
        elif str(ctx.message.author) not in self.g.players:
            await err_notingame(ctx)
        elif self.g.check_all_ready() and self.g.check_num_players():
            self.g.start()
            for pl in self.g.players:
                user = self.bot.get_user(self.g.ids[pl])
                pl_role = self.g.players[pl].role
                # unable to use bot to PM bot
                # workaround: if an echobot, then send role to game channel
                if pl[:7].lower() == "echobot":
                    await self.g.chan.send(txt.start[0].format(
                        self.g.get_nick(pl), str(pl_role)))
                else:
                    await user.send("New game!")
                    await self.g.private_info(user, pl_role)
            await self.g.chan.send(txt.start[1].format(
                self.g.list_roles_verbose()))
            await self.g.chan.send(txt.start[2].format(
                self.g.show_order(' > ')))
            await self.g.chan.send(txt.start[3].format(self.g.show_leader()))
            print(txt.log["start"].format(self.g.show_order()))
        else:
            await self.g.chan.send(txt.start[4])

    @commands.command(**command_desc.team)
    async def team(self, ctx, *, team_list):
        sender = ctx.message.author
        try:
            leader = self.g.curr_leader()
        except (IndexError, AttributeError):  # game not started, no Game obj
            print(txt.log["nogame"])
            return
        if str(sender) != leader:
            await sender.send(txt.team[0].format(self.g.show_leader()))
        elif not self.g.need_team():
            await sender.send(txt.team[4])
        else:
            pl_lst = team_list.split()
            not_pls = [p for p in pl_lst if not self.g.is_player(p)]
            size = self.g.curr_team_size()
            if not_pls:
                await sender.send(txt.team[1].format(", ".join(not_pls)))
            elif len(pl_lst) != size:
                await sender.send(txt.team[2].format(size, len(pl_lst)))
            else:
                # pl_lst now only contains player names or nicknames
                self.g.assign_team(pl_lst)
                # format the info to display to players
                mission = self.g.missions[-1].n
                round = len(self.g.missions[-1].rounds)
                leader = self.g.show_leader()
                team = self.g.show_team()
                args = [mission, round, leader, team]
                await self.g.chan.send(txt.team[3].format(*args))
                print(txt.log["team"].format(*args))
                await self.g.chan.send(txt.team[5])

    @commands.command(**command_desc.approve)
    async def approve(self, ctx):
        await self.team_vote(True, ctx)

    @commands.command(**command_desc.reject)
    async def reject(self, ctx):
        await self.team_vote(False, ctx)

    # not a command; handles the logic for !approve and !reject at once
    async def team_vote(self, verdict, ctx):
        sender = ctx.message.author
        name = str(sender)
        if not self.g:
            pass
        elif name not in self.g.players:
            pass
        elif not self.g.need_team_vote:
            pass
        else:
            cr = self.g.curr_round()
            if name in cr.votes:
                await sender.send(txt.team_vote[0])
            else:
                ch = self.g.chan
                cr.vote(name, verdict)
                vs, ps = len(cr.votes), self.g.number.players
                if vs == ps:
                    self.g.need_team_vote = False
                    needed = self.g.number.maj
                    tally = 0
                    for player in cr.votes:
                        if cr.votes[player]:
                            tally += 1
                            bold = ""
                            if player in cr.team:
                                bold = "**"
                            await ch.send(txt.team_vote[2].format(
                                self.g.get_nick(player), bold, "approve"))
                        else:
                            bold = ""
                            if player in cr.team:
                                bold = "**"
                            await ch.send(txt.team_vote[2].format(
                                self.g.get_nick(player), bold, "reject"))
                    if tally >= needed:
                        cr.approved = True
                        cm = self.g.curr_mission()
                        cm.assign_team()
                        await ch.send(txt.team_vote[3].format(
                            self.g.show_leader(),
                            ", ".join(self.g.list_mission_team())))
# TODO: tell them what to do next (do the mission in PMs)
# when mission team is approved, inc_leader() after mission success/failure
                    else:
# inc_leader() and display new leader, .add_round to curr_mission
                        cr.approved = False
                        await ch.send(txt.team_vote[4].format(
                            self.g.show_leader(),
                            ", ".join([self.g.get_nick(p) for p in cr.team])))
                else:           # num of votes < number of players
                    await ch.send(txt.team_vote[1].format(vs, ps))

    @commands.command(**command_desc.status)
    async def status(self, ctx):
        if not self.g:
            await ctx.send(txt.log["nogame"]) # incomplete
        else:
            await ctx.send(self.g.get_status())

@client.event
async def on_ready():
    print(txt.log["line"] + "New Session")
    print(txt.log["user"].format(client.user.name))
    print(txt.log["id"].format(client.user.id))
    print(txt.log["line"])

@client.event
async def on_message(message):
    '''Re-implements the on_message event so as to not ignore other bots.
    '''
    ctx = await client.get_context(message)
    await client.invoke(ctx)

@client.command(**command_desc.kill)
@is_admin()
async def kill(ctx):
    await ctx.send("brutal.")
    print(txt.log["kill"].format(ctx.message.author.name))
    await client.logout()

client.add_cog(ResBot(client))

if __name__ == "__main__":
    client.run(TOKEN)
