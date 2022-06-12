# Cette partie du code rassemble les commandes de modération.

import asyncio
import datetime
from typing import Optional
import random
import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from discord import ui, app_commands
import requests
from cogs.cogutils import MyBot, CESTify, prettytime

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)


class RecordModal(ui.Modal):
    def __init__(self, mode: str, member: discord.Member, ctx: Context, bot: MyBot | commands.Bot, warnchannel: discord.TextChannel, modrole: discord.Role):
        title = f"{mode.capitalize()} ce membre :"
        self.warnchannel = warnchannel
        self.modrole = modrole
        self.mode = mode
        self.bot = bot
        self.ctx = ctx
        self.member = member
        super().__init__(title=title)

        if mode == "ban":
            self.reason = discord.ui.TextInput(label='Raison du ban :', placeholder="Exemple : pa trè genti.", style=discord.TextStyle.short, required=False)
        elif mode == "kick":
            self.reason = discord.ui.TextInput(label='Raison du kick :', placeholder="Exemple : pa trè genti.", style=discord.TextStyle.short, required=False)
        elif mode == "mute":
            self.duration = discord.ui.TextInput(label='Durée du mute (heures) :', placeholder="Exemple : 3 (mettre 0 équivaut à unmute)", style=discord.TextStyle.short, required=True)
            self.reason = discord.ui.TextInput(label='Raison du mute :', placeholder="Exemple : pa trè genti.", style=discord.TextStyle.short, required=False)
            self.add_item(self.duration)
        else:
            self.reason = discord.ui.TextInput(label='Raison du warn :', placeholder="Exemple : pa trè genti.", style=discord.TextStyle.short, required=False)

        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if self.mode == "ban":
            if self.ctx.author.id == self.member.id:
                await interaction.response.send_message("Tu ne peux pas te ban toi-même !", ephemeral=True)
            elif self.modrole in self.member.roles:
                await interaction.response.send_message(
                    "Tu ne peux pas ban un autre modérateur ! Même si parfois avec Amaury c'est tentant...", ephemeral=True)
            elif self.member.id == self.bot.user.id:
                await interaction.response.send_message("Pourquoi t'essaies de me ban petit chenapan !!", ephemeral=True)
            else:
                await self.member.ban(reason=str(self.reason))
                await interaction.response.send_message(f"{self.member.name} a été ban !")
        elif self.mode == "kick":
            if self.ctx.author.id == self.member.id:
                await interaction.response.send_message("Tu ne peux pas te kick toi-même !", ephemeral=True)
            elif self.modrole in self.member.roles:
                await interaction.response.send_message(
                    "Tu ne peux pas kick un autre modérateur ! Même si parfois avec Amaury c'est tentant...", ephemeral=True)
            elif self.member.id == self.bot.user.id:
                await interaction.response.send_message("Pourquoi t'essaies de me kick petit chenapan !!", ephemeral=True)
            else:
                await self.member.kick(reason=str(self.reason))
                await interaction.response.send_message(f"{self.member.name} a été kick !")
        elif self.mode == "mute":
            if self.ctx.author.id == self.member.id:
                await interaction.response.send_message("Tu ne peux pas te mute toi-même !", ephemeral=True)
            elif self.modrole in self.member.roles:
                await interaction.response.send_message(
                    "Tu ne peux pas mute un autre modérateur ! Même si parfois avec Amaury c'est tentant...", ephemeral=True)
            elif self.member.id == self.bot.user.id:
                await interaction.response.send_message("Pourquoi t'essaies de me mute petit chenapan !!", ephemeral=True)
            else:
                dura = datetime.timedelta(hours=int(str(self.duration)))
                await self.member.timeout(dura, reason=str(self.reason))
                await interaction.response.send_message(f"{self.member.name} a été mute pendant {self.duration} heures !")

        else:
            if self.ctx.author.id == self.member.id:
                await interaction.response.send_message("Tu ne peux pas te warn toi-même !", ephemeral=True)
            elif self.modrole in self.member.roles:
                await interaction.response.send_message(
                    "Tu ne peux pas warn un autre modérateur ! ||Même si parfois avec Amaury c'est tentant...", ephemeral=True)
            elif self.member.id == self.bot.user.id:
                await interaction.response.send_message("Pourquoi t'essaies de me warn petit chenapan !!", ephemeral=True)
            else:
                embed = discord.Embed(title=f"Tu as été warn {self.member.name}!",
                                      description=f"Désolé {self.member.mention} ! La raison de ton warn est : _**{self.reason}**_.",
                                      colour=discord.Colour.red(),
                                      timestamp=self.ctx.message.created_at)
                embed.set_author(name=self.ctx.guild.name, icon_url=self.ctx.guild.icon.url)
                embed.set_footer(text=f"Ce warn t'a été mis par {self.ctx.author.name}.")
                try:
                    await self.member.send(embed=embed)
                except:
                    await self.ctx.send(embed=embed)
                secondembed = discord.Embed(title=f"{self.member.name} a été warn !",
                                            description=f"La raison est : **{self.reason}**.",
                                            colour=discord.Colour.red(),
                                            timestamp=self.ctx.message.created_at)
                secondembed.set_footer(text=f"Ce warn a été donné par {self.ctx.author.name}.")
                await self.warnchannel.send(embed=secondembed)
                await interaction.response.send_message(f"{self.member.name} a été warn avec raison : **{self.reason}** !")




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
        messages = ctx.channel.history(limit=number_of_messages + 1)
        async for each_message in messages:
            await each_message.delete()
        await ctx.channel.send("Les messages ont été supprimés !", delete_after=3)

    @commands.command(name="pin")
    @commands.has_role("Modérateurs")
    async def pin(self, ctx: Context):
        try:
            refmessageid = ctx.message.reference.message_id
            pinmessage = await ctx.fetch_message(refmessageid)
            await pinmessage.pin()
        except:
            await ctx.send("Tu ne réponds à aucun message !")

    @commands.command(name="mute", aliases=["timeout"])
    @commands.has_role("Modérateurs")
    async def mute(self, ctx: Context, member: discord.Member, hours: int, reason: Optional[str] = "pas de raison"):
        duration = datetime.timedelta(hours=hours)
        await member.timeout(duration, reason=reason)
        if hours == 0:
            await ctx.send(f"Le membre {member.name} a bien été unmute pour la raison : **{reason}**.")
            return
        if duration.days == 0:
            await ctx.send(f"Le membre {member.name} a été timeout pendant {hours} {'heures' if hours > 1 else 'heure'} pour la raison **{reason}**.")
        else:
            changingtime = hours
            days = 0
            while changingtime >= 24:
                days += 1
                changingtime -= 24
            await ctx.send(f"Le membre {member.name} a été timeout pendant {days} {'jour' if days == 1 else 'jours'} et {changingtime} {'heure' if changingtime == 1 else 'heures'}.")

    @commands.command(name="unmute")
    @commands.has_role("Modérateurs")
    async def untimeout(self, ctx: Context, member: discord.Member, reason: Optional[str] = "pas de raison"):
        duration = datetime.timedelta(hours=0)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"Le membre {member.name} a bien été unmute pour la raison : **{reason}**.")

    @commands.command(name="record")
    async def criminal_record(self, ctx: Context, member: discord.Member):
        joined = prettytime(CESTify(member.joined_at))
        warniterator = []
        warnings: discord.TextChannel = self.bot.get_channel(924313724188250163)
        async for message in warnings.history(limit=None):
            if member.name in message.embeds[0].title or member.display_name in message.embeds[0].title:
                dict = message.embeds[0].to_dict()
                author = dict['footer']['text'].split("par ")[1][:-1]
                reason = dict['description'].split("raison est : ")[1][:-1]
                warniterator.append([message.created_at.strftime("%d/%m/%Y à %H:%M"), reason, author])

        warnchannel: discord.TextChannel = self.bot.get_channel(924313724188250163)
        modrole = discord.utils.get(ctx.guild.roles, id=845027528196227133)


        class BabaBooey(ui.Button):
            def __init__(self, label: str, style: discord.ButtonStyle, mode: str, emoji: discord.PartialEmoji):
                self.mode = mode
                super().__init__(style=style, label=label, emoji=emoji)

            async def callback(self, interaction: discord.Interaction):
                nonlocal warnchannel, modrole
                await interaction.response.send_modal(RecordModal(mode=self.mode, member=member, ctx=ctx, bot=bot, warnchannel=warnchannel, modrole=modrole))

        # kick: ⏏️,  ban: 🔨, warn: 🔫, mute: 🤫
        kickbtn = BabaBooey(label="Kick le membre", emoji=discord.PartialEmoji(name="⏏"), style=discord.ButtonStyle.red, mode="kick")
        banbtn = BabaBooey(label="Ban le membre", emoji=discord.PartialEmoji(name="🔨"), style=discord.ButtonStyle.red, mode="ban")
        warnbtn = BabaBooey(label="Warn le membre", emoji=discord.PartialEmoji(name="🔫"), style=discord.ButtonStyle.red, mode="warn")
        mutebtn = BabaBooey(label="Mute le membre", emoji=discord.PartialEmoji(name="🤫"), style=discord.ButtonStyle.red, mode="mute")

        view = ui.View().add_item(kickbtn).add_item(banbtn).add_item(warnbtn).add_item(mutebtn)

        embed = discord.Embed(title=f"Casier de {member.name} :", description=f"A rejoint le {joined}.\nVoici les warns de {member.name} :", colour=discord.Colour.red())
        warnslist = []
        if len(warniterator) == 0:
            embed.add_field(name="Ce membre n'a pas de warn !", value="et oui il est sage")
        else:
            for i in warniterator:
                warnslist.append([f"Warn n°{warniterator.index(i)+1} le {i[0]}", f"par {i[2]}, raison :\n{i[1]}"])

        for i in warnslist:
            embed.add_field(name=i[0], value=i[1])

        await ctx.send(embed=embed, view=view)


# On ajoute le cog au bot.
async def setup(bot):
    await bot.add_cog(Moderation(bot))
