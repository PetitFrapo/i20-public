import asyncio
import datetime
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


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="throw")
    async def throw(self, ctx: Context, victim: discord.Member):
        throwmaterials = ["de la crasse", "Amaury", "un fichier PNG", "du pain", "un ballon de basket",
                          "un truc non identifié", "un 12/20 en maths", "des crêpes", "une Pokéball", 'la Master Sword',
                          "une pièce SOS", "un être d'Yvain"]
        throwmaterial = random.choice(throwmaterials)
        await ctx.send(
            f"{ctx.author.display_name} a lancé {throwmaterial} sur {victim.display_name} ! Il est tout sali maintenant...")
        if victim.display_name == "i20":
            await ctx.send("Aïe ! Qui m'a lancé ça ?")
        if throwmaterial == throwmaterials[8]:
            await ctx.send("...")
            await asyncio.sleep(3)
            caught = random.choice([0, 1, 2, 3, 4])
            if caught == 3:
                await ctx.send(f'{ctx.author.display_name} a capturé {victim.display_name} !')
            else:
                await ctx.send(f"{victim.display_name} s'est enfuit !")

    @commands.command(name="ship")
    async def ship(self, ctx, member1: discord.Member = "", member2: discord.Member = ""):
        easteregg = random.randrange(0, 49)
        if easteregg == 45:
            await ctx.send(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Lorient-navire-oceanographi.jpg/1200px-Lorient-navire-oceanographi.jpg")
        else:
            if member1 == "" and member2 == "":
                users = ctx.guild.members
                user1, user2 = random.sample(users, 2)
            else:
                user1 = member1
                user2 = member2
            part1 = user1.display_name[:len(user1.display_name) // 2]
            part2 = user2.display_name[len(user2.display_name) // 2:]
            babyname = part1 + part2
            await ctx.send(
                f"{user1.display_name} et {user2.display_name} ont eu un enfant ! Il s'appellera {babyname} !")
            if user1.display_name == "i20" or user2.display_name == "i20":
                await ctx.send(f"uwu viens dans mes bras {babyname}~~~")

    @commands.command(name="id")
    async def id(self, ctx, *, target: commands.MemberConverter):
        try:
            targetid = target.id
            await ctx.send(f"L'ID de {target.display_name} est {targetid}.")
        except:
            await ctx.send("Ce membre n'existe pas !")




async def setup(bot):
    await bot.add_cog(Fun(bot))
