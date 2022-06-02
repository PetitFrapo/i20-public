import asyncio
import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord import ui, app_commands
import requests
from cogs.CONSTANTS import MyBot, CESTify

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter):
        await ctx.guild.kick(member)
        await ctx.send(f"{member} a été kick du serveur ! Il fallait être plus sage !")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=""):
        if member != self.bot.user:
            if member != ctx.author:
                await ctx.guild.ban(member, reason=reason)
                await ctx.send(
                    f"{member} a été banni du serveur pour la raison : \"{reason}\" ! MOUAHAHA ! Mon marteau était fatigué...")
            else:
                await ctx.send("Tu ne peux pas te bannir toi même !")
        else:
            await ctx.send("n'essaie même pas")
        await ctx.send(
            f"{member} a été banni du serveur pour la raison : \"{reason}\" ! MOUAHAHA ! Mon marteau était fatigué...")

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(
                    f'{user.name}#{user.discriminator} a été débanni ! Il était peut-être pas si méchant que ça...')
                return

    @commands.command(name="warn")
    @commands.has_role("Modérateurs")
    async def warn(self, ctx: commands.Context, member: discord.Member, *, reason="aucune raison donnée"):
        modrole = discord.utils.get(ctx.guild.roles, id=845027528196227133)
        if ctx.author.id == member.id:
            await ctx.send("Tu ne peux pas te warn toi-même !")
        elif modrole in member.roles:
            await ctx.send("Tu ne peux pas warn un autre modérateur ! ||Même si parfois avec Amaury c'est tentant...||")
        elif member.id == self.bot.user.id:
            await ctx.send("Pourquoi t'essaies de me warn petit chenapan !!")
        else:
            #await ctx.message.delete()
            warnchannel: discord.TextChannel = self.bot.get_channel(924313724188250163)
            embed = discord.Embed(title=f"Tu as été warn {member.name}!",
                                  description=f"Désolé {member.mention} ! La raison de ton warn est : _**{reason}**_.",
                                  colour=discord.Colour.red(),
                                  timestamp=ctx.message.created_at)
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
            embed.set_footer(text=f"Ce warn t'a été mis par {ctx.author.name}.")
            try:
                await member.send(embed=embed)
            except:
                await ctx.send(embed=embed)
            secondembed = discord.Embed(title=f"{member.name} a été warn !",
                                        description=f"La raison est : **{reason}**.",
                                        colour=discord.Colour.red(),
                                        timestamp=ctx.message.created_at)
            secondembed.set_footer(text=f"Ce warn a été donné par {ctx.author.name}.")
            await warnchannel.send(embed=secondembed)

    @commands.command(name="warns", aliases=["warnings"])
    async def warns(self, ctx, user: discord.Member = None):
        if user == None:
            target = ctx.author
        else:
            target = user
        warniterator = []
        warnings: discord.TextChannel = self.bot.get_channel(924313724188250163)
        async for message in warnings.history(limit=None):
            if target.name in message.embeds[0].title or target.display_name in message.embeds[0].title:
                dict = message.embeds[0].to_dict()
                author = dict['footer']['text'].split("par ")[1][:-1]
                reason = dict['description'].split("raison est : ")[1][:-1]
                warniterator.append([message.created_at.strftime("%d/%m/%Y à %H:%M"), reason, author])

        embed = discord.Embed(title=f"Tu as eu {len(warniterator)} warn(s) :", color=discord.Colour.random())
        for warnfield in warniterator:
            embed.add_field(name=f"Warn du {warnfield[0]} :",
                            value=f"Mis par {warnfield[2]} pour la raison '{warnfield[1]}'.", inline=False)
        if warniterator == []:
            await ctx.send("Tu n'as pas de warn !")
        else:
            await ctx.send(embed=embed)

    @commands.command(name="removewarn")
    async def removewarn(self, ctx, excusedMember: discord.Member):
        found = False
        warnings: discord.TextChannel = self.bot.get_channel(924313724188250163)
        async for warn in warnings.history(limit=None):
            if len(warn.embeds) != 0:
                if excusedMember.name in warn.embeds[0].title:
                    await ctx.send(
                        f"Voulez-vous retirer le dernier warn de {excusedMember.name}, qui a été mis par {warn.embeds[0].footer.text.split('par ')[1][:-1]} le {warn.created_at.strftime('%d/%m/%Y à %H:%M')} ? Répondez 'Oui' si oui.")

                    def check(m: discord.Message):
                        return m.content.lower() == "oui" and m.author == ctx.author

                    try:
                        yes = await self.bot.wait_for('message', check=check, timeout=30)
                        if yes:
                            await warn.delete()
                            await ctx.send("Warn supprimé !")
                    except asyncio.TimeoutError:
                        await ctx.send("Temps écoulé !")
                        break
                else:
                    found = False
        if found == False:
            await ctx.send(f"{excusedMember.name} n'a pas de warn !")

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, number_of_messages: int):
        messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()
        for each_message in messages:
            await each_message.delete()
        await ctx.channel.send("Les messages ont été supprimés !", delete_after=3)

    @commands.command(name="pin")
    @commands.has_role("Modérateurs")
    async def pin(self, ctx):
        try:
            refmessageid = ctx.message.reference.message_id
            pinmessage = await ctx.fetch_message(refmessageid)
            await pinmessage.pin()
        except:
            await ctx.send("Tu ne réponds à aucun message !")

    @commands.hybrid_command(name="updaterole")
    @app_commands.checks.has_role("Modérateurs")
    @commands.has_role("Modérateurs")
    async def updaterole(ctx: commands.Context, roletodel: discord.Role, roletoadd: discord.Role) -> None:
        times = 0
        guild: discord.Guild = ctx.guild
        for member in guild.members:
            if roletodel in member.roles:
                await member.remove_roles(roletodel)
                await member.add_roles(roletoadd)
                times += 1
        await ctx.send(f"**{times}** modifications ont été effectuées !")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
