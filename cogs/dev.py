from typing import *
import discord
from discord.ext import commands
from discord import Interaction
from discord.ext.commands import Cog, Context
from dotenv import load_dotenv
from discord import app_commands
from discord.app_commands import Choice
import os

from cogs.cogutils import MyBot

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)
load_dotenv(dotenv_path="config")

unloaded_cogs = []


async def debugevent(ctx: Context, error):
    if isinstance(error, commands.CommandNotFound):
        return
    await ctx.send(f"Erreur dans la commande {ctx.invoked_with}, par {ctx.author.name}, le {ctx.message.created_at.strftime('%d/%m/%Y à %H:%M:%S')}. ```{str(error)}```")


class Dev(Cog):
    global coglist
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_group(name="dev")
    @app_commands.checks.has_role(924369265950326785)
    @commands.has_role(924369265950326785)
    async def dev(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Rentre une sous-commande !")

    @commands.has_role(992852476552298646)
    @app_commands.checks.has_role(924369265950326785)
    @dev.command(name="alertunload", description="Désactive un cog EN URGENCE au choix.")
    @app_commands.describe(password="Le mot de passe pour arrêter un cog en urgence.", cog="Le cog à désactiver.")
    async def emergencyunload(self, ctx: Context, password: str, cog: str):
        if password != os.getenv("alertpass"):
            await ctx.send("Mot de passe incorrect.")
            return
        coglist = list(self.bot.cogs)
        if cog not in coglist:
            await ctx.send(f"Le cog {cog} n'existe pas !")
            return
        await self.bot.remove_cog(cog)
        unloaded_cogs.append(cog)
        await ctx.send(f"Le cog {cog} a été unload !")

    @emergencyunload.autocomplete("cog")
    async def emerauto(self, interaction: Interaction,
                       current: str) -> List[app_commands.Choice[str]]:
        return [Choice(name=cog, value=cog) for cog in self.bot.cogs if current.lower() in cog.lower()]

    @commands.has_role(924369265950326785)
    @app_commands.checks.has_role(924369265950326785)
    @dev.command(name="unload", description="Désactive un cog au choix.")
    @app_commands.describe(cog="Le cog à désactiver.")
    async def unload(self, ctx: Context, cog: str):
        coglist = list(self.bot.cogs)
        if cog.lower() in {"moderation", "dev"}:
            await ctx.send("Tu ne peux pas unload Moderation ou Dev !")
            return

        if cog not in coglist:
            await ctx.send(f"Le cog {cog} n'existe pas !")
            return

        await self.bot.remove_cog(cog)
        unloaded_cogs.append(cog)
        await ctx.send(f"Le cog {cog} a été unload !")

    @unload.autocomplete("cog")
    async def unloadauto(self, interaction: Interaction,
                         current: str) -> List[app_commands.Choice[str]]:
        return [Choice(name=cog, value=cog) for cog in self.bot.cogs if current.lower() in cog.lower()]

    @commands.has_role(924369265950326785)
    @app_commands.checks.has_role(924369265950326785)
    @dev.command(name="run", description="Exécute du code en Python.")
    @app_commands.describe(code="Le code à exécuter.")
    async def run(self, ctx: Context, *, code):
        if ctx.author.id != 558317667505668098:
            await ctx.send("Cette commande peut être dangereuse. Seul PetitFrapo peut l'exécuter.")
            return
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

        await _run(code)
        await ctx.send("✅", delete_after=3)
        
    @commands.has_role(924369265950326785)
    @app_commands.checks.has_role(924369265950326785)
    @dev.command(name="reload", description="Réactive un cog désactivé.")
    async def reload(self, ctx: Context, cog: str):
        if cog not in unloaded_cogs:
            await ctx.send("Le cog est déjà chargé !")
            return
        await self.bot.reload_extension(f"cogs.{'app_commands.' if cog.lower() in {'slash', 'ui', 'contextmenu'} else ''}{cog.lower()}")
        await ctx.send(f"L'extension {cog} a bien été réactivée !")


    @commands.has_role(924369265950326785)
    @app_commands.checks.has_role(924369265950326785)
    @dev.group(name="debug")
    async def debugc(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Veuillez entrer une sous-commande.")

    @commands.has_role(924369265950326785)
    @app_commands.checks.has_role(924369265950326785)
    @debugc.command(name="enable", description="Active le mode debug.")
    async def debugenable(self, ctx: Context):
        self.bot.add_listener(debugevent, "on_command_error")
        await ctx.send("Mode debug activé !")

    @commands.has_role(924369265950326785)
    @app_commands.checks.has_role(924369265950326785)
    @debugc.command(name="disable", description="Désactive le mode debug.")
    async def debugdisable(self, ctx: Context):
        self.bot.remove_listener(debugevent, "on_command_error")
        await ctx.send("Mode debug désactivé !")



# On ajoute le cog au bot.
async def setup(bot):  # sourcery skip: instance-method-first-arg-name
    await bot.add_cog(Dev(bot))
