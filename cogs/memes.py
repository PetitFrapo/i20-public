import datetime

import discord
from discord.ext import commands
from discord import ui
import requests
from cogs.CONSTANTS import MyBot, CESTify

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="meme")
    async def meme(self, ctx: commands.Context, subreddit=""):
        nsfwcount = -1
        while True:
            nsfwcount += 1
            if nsfwcount == 3:
                await ctx.send("Le subreddit demandé est sûrement NSFW. Veuillez en demander un SFW.")
                break
            if subreddit != "":
                addin = f"/{subreddit}"
            else:
                addin = ""
            r = requests.get(f"https://meme-api.herokuapp.com/gimme{addin}")

            data = eval(r.text.replace("false", "False").replace("true", "True"))
            postLink = data["postLink"]
            subreddit = data["subreddit"]
            imgurl = data["url"]
            nsfw = data["nsfw"]
            if nsfw:
                continue
            title = data["title"]
            author = data["author"]

            embed = discord.Embed(title=title, timestamp=CESTify(datetime.datetime.now()), colour=discord.Colour.random())
            embed.set_image(url=imgurl)
            embed.set_author(name=author)
            embed.set_footer(text=subreddit)
            button = ui.Button(label="Original Post", style=discord.ButtonStyle.url, url=postLink)
            view = ui.View()
            view.add_item(button)
            await ctx.send(embed=embed, view=view)
            break

async def setup(bot):
    await bot.add_cog(Memes(bot))
