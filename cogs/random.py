# Cette partie du code rassemble les commandes i!ost et i!random.

import datetime
import random
import discord
from discord.ext import commands
from discord import ui
import requests
from cogs.cogutils import MyBot, CESTify

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

    @commands.command(name="random", aliases=["rmdmsg", "randommsg", "baba"])
    async def randommsg(self, ctx, number: int = 1, channel: discord.TextChannel = None):
        if number < 1:
            await ctx.send("Tu ne peux pas demander moins d'1 message !")
            return
        if channel is None:
            channel = ctx.channel
        messages = []
        time = await ctx.send("Cette opération peut prendre quelques temps.")
        async with ctx.channel.typing():
            history = channel.history(limit=1000)
            async for message in history:
                messages.append(message.content)
            messages_to_send = random.sample(messages, number)
        await time.delete()
        msg = messages_to_send[0]

        index = messages_to_send.index(msg)

        class AButton(ui.Button):
            def __init__(self, style, emoji, direct):
                self.direct = direct
                self.msg = msg
                super().__init__(style=style, emoji=emoji)

            async def callback(self, interaction: discord.Interaction):
                nonlocal index

                if self.direct == "l":
                    if index == 0:
                        embed = discord.Embed(title=f"Voici un message aléatoire du salon {channel.name} !",
                                              description=messages_to_send[len(messages_to_send)-1]).set_footer(text=f"{len(messages_to_send)}/{len(messages_to_send)}")
                        self.msg = messages_to_send[len(messages_to_send)-1]
                        index = messages_to_send.index(self.msg)
                        await interaction.response.edit_message(embed=embed)
                    else:
                        embed = discord.Embed(title=f"Voici un message aléatoire du salon {channel.name} !",
                                              description=messages_to_send[index-1]).set_footer(text=f"{index}/{len(messages_to_send)}")
                        self.msg = messages_to_send[index-1]
                        index = messages_to_send.index(self.msg)
                        await interaction.response.edit_message(embed=embed)
                else:
                    if index == len(messages_to_send) - 1:
                        embed = discord.Embed(title=f"Voici un message aléatoire du salon {channel.name} !",
                                              description=messages_to_send[0]).set_footer(text=f"1/{len(messages_to_send)}")
                        self.msg = messages_to_send[0]
                        index = messages_to_send.index(self.msg)
                        await interaction.response.edit_message(embed=embed)
                    else:
                        embed = discord.Embed(title=f"Voici un message aléatoire du salon {channel.name} !",
                                              description=messages_to_send[index+1]).set_footer(text=f"{index+2}/{len(messages_to_send)}")
                        self.msg = messages_to_send[index+1]
                        index = messages_to_send.index(self.msg)
                        await interaction.response.edit_message(embed=embed)

        leftbutton = AButton(emoji="⬅️", style=discord.ButtonStyle.primary, direct="l")
        rightbutton = AButton(emoji="➡️", style=discord.ButtonStyle.primary, direct="r")
        view = ui.View().add_item(leftbutton).add_item(rightbutton)

        embed = discord.Embed(title=f"Voici un message aléatoire du salon {channel.name} !", description=msg)
        if number != 1:
            embed.set_footer(text=f"1/{len(messages_to_send)}")
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.send(embed=embed)


# On ajoute le cog au bot.
async def setup(bot):
    await bot.add_cog(Random(bot))
