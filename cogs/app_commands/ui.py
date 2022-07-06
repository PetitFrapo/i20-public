# Cette partie du code rassemble le sous-module ui de discord.py,
# Cela passe par les boutons, les menus de sélection, les questionnaires, etc...

import datetime
import typing
import discord
import pytz
from discord.ext import commands
from discord import Interaction
from discord.ext.commands import Cog, Context
from discord import ui
from cogs.cogutils import MyBot, CESTify

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)
timezone = pytz.timezone("Europe/Paris")


# Un modal représente le questionnaire.
class Submit(ui.Modal, title='Soumettre une idée :'):
    def __init__(self, guild):
        self.guild = guild
        self.isanonymous = True
        super().__init__()

    command = discord.ui.TextInput(label='Commande concernée (peut être une nouvelle) :', placeholder="Exemple : quote.", style=discord.TextStyle.short, required=True)
    fdescr = discord.ui.TextInput(label='Modification proposée (rapide) :', required=True, placeholder="Exemple : Nouvelle citation.", style=discord.TextStyle.short)
    ldescr = discord.ui.TextInput(label="Description longue :", required=True, placeholder="Exemple : Je veux rajouter blabla car...", style=discord.TextStyle.paragraph)
    anonytest = ui.Select(placeholder="Veux-tu que ton nom s'affiche ?", options=[discord.SelectOption(label="Oui, je veux que mon nom s'affiche.", emoji="👍"), discord.SelectOption(label="Non, je veux rester anonyme.", emoji="👎")])

    async def on_submit(self, interaction: discord.Interaction):
        if str(self.anonytest.values[0]).lower() == "oui, je veux que mon nom s'affiche.":
            self.isanonymous = False
        elif str(self.anonytest.values[0]).lower() == "non, je veux rester anonyme.":
            self.isanonymous = True

        channel = self.guild.get_channel(982644476436693032)
        embed = discord.Embed(title=f'''{interaction.user.name if not self.isanonymous else "Quelqu'un"} a soumis quelque chose !\n''', description=f"Commande : {self.command}", timestamp=CESTify(datetime.datetime.now()), colour=discord.Colour.random())
        embed.add_field(name="Description courte :", value=self.fdescr, inline=False)
        embed.add_field(name="Longue descritpion", value=self.ldescr, inline=False)
        await channel.send(f"{self.guild.get_member(558317667505668098).mention}", embed=embed)
        await interaction.response.send_message("Ta soumission a bien été envoyée !", ephemeral=True)


class UI(Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
        tree = self.bot.tree

    @commands.hybrid_command(name="submit", description="Proposez vos idées pour i20 !")
    async def submit_ideas(self, ctx: Context):
        send_to_guild = self.bot.get_guild(981950727511474266)

        class SubmitIdeasButton(ui.Button):
            def __init__(self, label, style):
                super().__init__(label=label, style=style)

            async def callback(self, interaction: Interaction) -> typing.Any:
                await interaction.response.send_modal(Submit(send_to_guild))

        button = SubmitIdeasButton(label="Propose tes idées !", style=discord.ButtonStyle.primary)
        view = ui.View()
        view.add_item(button)
        await ctx.send(view=view)


# On ajoute le cog au bot.
async def setup(bot):
    await bot.add_cog(UI(bot))
