import datetime
import inspect
import os
import random

import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from discord import ui
import requests
from cogs.CONSTANTS import MyBot, timezone

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)


def statusformat(status: discord.Status) -> str:
    sta = str(status)
    if sta == "online":
        return "En ligne"
    elif sta == "offline":
        return "Hors ligne"
    elif sta == "idle":
        return "Inactif"
    elif sta == "dnd":
        return "Ne pas déranger"


class Useful(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll", help="Crée un sondage.")
    async def poll(self, ctx: Context, question, option1, option2, option3="", option4="", mention_everyone=""):
        poll_channel: discord.TextChannel = bot.get_channel(922936202909319168)
        await ctx.message.delete()
        three_opt = None
        four_opt = None
        if option3 == "" and option4 == "":
            two_opt = True
            embed = discord.Embed(title=question, description=f"1️⃣ : {option1}\n 2️⃣ : {option2}",
                                  timestamp=datetime.datetime.now(tz=timezone))
        elif option3 != "" and option4 == "":
            three_opt = True
            embed = discord.Embed(title=question, description=f"1️⃣ : {option1}\n 2️⃣ : {option2}\n 3️⃣ : {option3}",
                                  timestamp=datetime.datetime.now(tz=timezone))
        elif option3 != "" and option4 != "":
            four_opt = True
            embed = discord.Embed(title=question,
                                  description=f"1️⃣ : {option1}\n 2️⃣ : {option2}\n 3️⃣ : {option3}\n 4️⃣ : {option4}",
                                  timestamp=datetime.datetime.now(tz=timezone))
        else:
            embed = None
        emoji1 = "1️⃣"
        emoji2 = "2️⃣"
        emoji3 = "3️⃣"
        emoji4 = "4️⃣"

        role = discord.utils.get(ctx.guild.roles, id=922944521384374312)
        if role in ctx.author.roles:
            await ctx.author.send(
                "Désolé, tu es banni de la commande i!poll... Tu as sûrement joué avec ou spam les sondages...")
        else:
            message = await poll_channel.send(embed=embed)
            await message.add_reaction(emoji1)
            await message.add_reaction(emoji2)
            if three_opt is True:
                await message.add_reaction(emoji3)
            elif four_opt is True:
                await message.add_reaction(emoji3)
                await message.add_reaction(emoji4)

        if mention_everyone != "":
            modrole = discord.utils.get(ctx.guild.roles, id=845027528196227133)
            if modrole in ctx.author.roles:
                if mention_everyone.lower() == "true":
                    await poll_channel.send("@everyone")
            else:
                await ctx.author.send("T'as trop cru tu pouvais mentionner everyone mdrrr")

    @commands.command(name="avatar", help="Prenez l'avatar de quelqu'un.", aliases=["pp", "pdp", "pfp"])
    async def avatar(self, ctx, *, user: discord.Member = ""):
        if user == "":
            userAvatar = ctx.author.avatar_url
            await ctx.channel.send(f"Voici l'avatar de {ctx.author.display_name}.")
            await ctx.channel.send(userAvatar)
        else:
            userAvatar = user.avatar_url
            await ctx.channel.send(f"Voici l'avatar de {user.display_name}.")
            await ctx.channel.send(userAvatar)

    @commands.command(name="embed")
    async def embed(self, ctx: commands.Context, title, desc, field1="", field1desc="", field2="", field2desc=""):
        hideName = False
        modrole = discord.utils.get(ctx.guild.roles, id=845027528196227133)
        if modrole in ctx.author.roles:
            if ctx.message.content.lower().endswith("hidename"):
                hideName = True
        color = random.randrange(0, 2 ** 24)
        embed = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.datetime.now(tz=timezone))
        member = ctx.author
        if hideName is False:
            embed.set_author(name=member, icon_url=member.avatar_url)
        if field1 != "" and field1desc != "":
            embed.add_field(name=field1, value=field1desc)
        if field2 != "" and field2desc != "":
            embed.add_field(name=field2, value=field2desc)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(name="profile")
    async def profile(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        name = member.name
        if name.lower()[0] in {"a", "e", "i", "o", "u", "y"}:
            print("true")
            modifier = "'"
        else:
            modifier = "e "
        nick = member.display_name
        if not member.avatar:
            avatar = False
        else:
            icon = member.avatar.url
            avatar = True
        status = statusformat(member.status)
        created = member.created_at.astimezone(timezone).strftime("%d/%m/%Y %H:%M")
        joined = member.joined_at.astimezone(timezone).strftime("%d/%m/%Y %H:%M")

        embed = discord.Embed(title=f"Profil d{modifier}{name}",
                              description=f"alias {nick}",
                              colour=discord.Colour.random())
        embed.add_field(name="Statut",
                        value=status,
                        inline=False)
        embed.add_field(name="Compte créé le",
                        value=created,
                        inline=False)
        embed.add_field(name="A rejoint le",
                        value=joined,
                        inline=False)
        if avatar:
            embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="bg")
    async def bg(self, ctx: Context, image=""):
        if not ctx.message.attachments:
            if image == "":
                await ctx.send("Il faut mettre une pièce jointe ou un lien.")
            else:
                which = image
        else:
            which = ctx.message.attachments[0].url
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',

            data={'size': 'auto', 'image_url': which},
            headers={'X-Api-Key': 'tiFWuGxiquKKEYxL1kVPnyhd'},
        )
        if response.status_code == requests.codes.ok:
            with open('no-bg.png', 'wb') as out:
                out.write(response.content)
                file = discord.File("no-bg.png")
                await ctx.send(file=file)
        else:
            print("Error:", response.status_code, response.text)

    @commands.command(name="edit")
    async def edit(self, ctx: Context, *, whatedit):
        await ctx.message.delete()
        refmessageid = ctx.message.reference.message_id
        msg = await ctx.channel.fetch_message(refmessageid)
        if msg.author.id != 853301761572732928:
            await ctx.send("Tu ne peux modifier un message que si je l'ai envoyé !", delete_after=3)
        else:
            await msg.edit(content=whatedit)

    @commands.command(name="info")
    async def info(self, ctx: Context):
        version = "2.2"
        description = "Bienvenue sur i20, un bot créé par PetitFrapo pour le serveur du monde d'Yvain, sur lequel vous êtes sûrement. Il implémente de nombreuses fonctionnalités de l'API discord.py, ainsi que ses dernières fonctionnalités, telles que les commandes slash. Effectuez la commande i!help afin de savoir quelles en sont les commandes. Vous pouvez aussi aller voir le salon <#858633105342857236> afin de vous renseigner sur certaines fonctionnalités qu'il comporte en réaction à certains messages."
        embed = discord.Embed(title=f"**__i20 v{version}__**",
                              description=description,
                              timestamp=ctx.message.created_at,
                              colour=discord.Colour.random())
        await ctx.send(embed=embed)

    @commands.command(name="reply")
    async def reply(self, ctx: Context, *, content):
        try:
            refmessageid = ctx.message.reference.message_id
            repmessage = await ctx.fetch_message(refmessageid)
        except:
            await ctx.send("Tu ne réponds a aucun message !")
        await ctx.message.delete()
        swear_words = ["putain", "merde", "con", "connard", "fuck", "damn", "hell", "bordel", "pute", "shit",
                       "everyone"]
        swear_flag = None
        a = 0
        for i in swear_words:
            if i in str(content).lower():
                swear_flag = True
                break
            else:
                swear_flag = False
        if swear_flag:
            try:
                await ctx.author.send("JAMAIS JE NE DIRAI CE GENRE DE CHOSES MAIS OÙ VA LE MONDE !")
            except:
                await ctx.send("JAMAIS JE NE DIRAI CE GENRE DE CHOSES MAIS OÙ VA LE MONDE !", delete_after=5)
        else:
            if len(ctx.message.attachments) != 0:
                file = await ctx.message.attachments[0].to_file()
                await repmessage.reply(content, file=file)
            else:
                await repmessage.reply(content)


async def setup(bot):
    await bot.add_cog(Useful(bot))

