# Bienvenue sur le code source d'i20, ici vous trouverez toutes sortes de choses intéressantes,
# que ce soit pour obtenir des idées pour un programme, ou pour comprendre comment le bot marche.

# Crédits : PetitFrapo et c'est tout.

# Version: 2.3b

import inspect
import os
import discord
import pytz
import random
from discord.ext.commands import Context
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

extensions = (
    "cogs.help",
    "cogs.listeners",
    "cogs.memes",
    "cogs.app_commands.slash",
    "cogs.app_commands.contextmenu",
    "cogs.app_commands.ui",
    # "cogs.data",
    "cogs.database",
    "cogs.birthday",
    "cogs.random",
    "cogs.moderation",
    "cogs.fun",
    "cogs.useful"
)


class MyBot(commands.Bot):
    def __init__(self, *, command_prefix, case_insensitive, help_command, intents, application_id):
        super().__init__(command_prefix=command_prefix, case_insensitive=case_insensitive, help_command=help_command,
                         intents=intents, application_id=application_id)

    async def setup_hook(self):
        for ext in extensions:
            await self.load_extension(ext)
        self.loop.create_task(presence())
        self.tree.copy_global_to(guild=discord.Object(id=962604741278449724))
        self.tree.copy_global_to(guild=discord.Object(id=845026449495818240))
        await self.tree.sync(guild=discord.Object(id=845026449495818240))
        await self.tree.sync(guild=discord.Object(id=962604741278449724))


client = discord.Client(intents=default_intents)
bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None,
            intents=default_intents, application_id=853301761572732928)

timezone = pytz.timezone("Europe/Paris")
load_dotenv(dotenv_path="config")

bottree = bot.tree
tree = app_commands.CommandTree(client)
yvainguild = discord.Object(id=845026449495818240)


def whichaddin(string: str) -> str:
    if string[0].lower() in {"a", "e", "i", "o", "u", "y"}:
        addin = "'"
    else:
        addin = "e "
    return addin


@bot.event
async def on_ready():
    print(f"i20 {os.getenv('version')} est prêt !")


async def presence():
    await bot.wait_until_ready()
    while not bot.is_closed():
        presences = ["Respectez moi sinon grr", "Je suis un bot créé par PetitFrapo !", "la vi c pa un kiwi",
                     "mon magnifique code.", "Essaie d'avoir un statut custom ++"]
        game = random.choice(presences)
        if game != presences[3]:
            await bot.change_presence(activity=discord.Game(name=game))
        else:
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.watching))
        await asyncio.sleep(5)


@bot.command(name="run")
async def run(ctx, *, whattorun):
    if ctx.author.id != 558317667505668098:
        await ctx.send("Cette commande peut être dangereuse. Seul PetitFrapo peut l'exécuter.")
    else:
        async def _run(what):
            if what.startswith("await"):
                await eval(what.replace("await ", ""))
            else:
                whattoprint = []
                _locals = locals()
                new = what.replace("await ctx.send(", "whattoprint.append(")

                exec(new, globals(), _locals)
                whattoprint = _locals['whattoprint']
                for i in whattoprint:
                    await ctx.send(i)

        await _run(whattorun)


@bot.command(name="source")
async def source(ctx: Context, com: str) -> None:
    comlist = bot.commands
    comnlist = [co.name for co in comlist]
    if com.lower() not in comnlist:
        await ctx.send(f"La commande {com} n'existe pas !")
        return
    for command in comlist:
        if command.name == com.lower():
            if command.cog_name is not None:
                addin = "app_commands." if command.cog_name in {"Slash", "ContextMenu", "UI"} else ""
                line = f"from cogs.{addin}{command.cog_name.lower()} import {command.cog_name}"
                exec(line)
                command = eval(f"{command.cog_name}.{command.name}")

            code = inspect.getsource(command.callback)

    if len(code) > 2000:
        f = open(f"{com}.txt", "w")
        f.write(code)
        f.close()
        file = discord.File(f"{com}.txt")
        await ctx.send(file=file)
        os.system(f"rm {com}.txt")
    else:
        await ctx.send(f"```py\n{code}```")


# On lance le bot. La variable TOKEN est une variable cachée dont vous n'avez pas accès.
bot.run(os.getenv("TOKEN"))
