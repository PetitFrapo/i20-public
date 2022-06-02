import datetime
import random

import discord
from discord.ext import commands
from discord import ui
import requests
from cogs.CONSTANTS import MyBot, CESTify

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ost")
    async def ost(self, ctx):
        mp3channel: discord.TextChannel = self.bot.get_channel(852754892946014238)
        failed = False
        timetime = await ctx.send("Cette opération peut prendre quelques temps.")
        mp3s = []
        async with ctx.channel.typing():
            history = mp3channel.history(limit=None)
            async for message in history:
                if message.attachments:
                    if message.attachments[0].content_type == "audio/mpeg":
                        # mp3url = await message.attachments[0].to_file()
                        mp3id = message.id
                        mp3s.append(mp3id)
        try:
            mp3tosend = random.choice(mp3s)
        except:
            await timetime.delete()
            await ctx.send("Désolé, il n'y a pas de MP3 dans ce salon...")
            failed = True
        if not failed:
            mp3tosendbutforreal: discord.Message = await mp3channel.fetch_message(mp3tosend)
            file = await mp3tosendbutforreal.attachments[0].to_file()
            await timetime.delete()
            await ctx.send(content=f"Profite bien de ton OST !", file=file)

    @commands.command(name="randommsg", aliases=["rmdmsg", "random"])
    async def randommsg(self, ctx):
        messages = []
        time = await ctx.send("Cette opération peut prendre quelques temps.")
        async with ctx.channel.typing():
            history = await ctx.channel.history(limit=3000).flatten()
            for message in history:
                messages.append(message.content)
            msgToSend = random.choice(messages)
        await time.delete()
        await ctx.send(f"Voici un message aléatoire du salon {ctx.channel} !\n")
        await ctx.send(msgToSend)


async def setup(bot):
    await bot.add_cog(Random(bot))
