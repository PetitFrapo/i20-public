# Cette partie du code contient deux menus contextuels,
# Le premier est : Date d'arrivée sur le serveur (show_join_date).
# Le second est : Quoter ce message (quote_message).

import discord
import pytz

from discord import app_commands
from discord.ext.commands import Cog
from discord import ui
from cogs.cogutils import MyBot

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)
timezone = pytz.timezone("Europe/Paris")


class ContextMenu(Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
        tree = self.bot.tree
        self.joindate = app_commands.ContextMenu(name="Date d'arrivée sur le serveur", callback=self.show_join_date)
        self.quote = app_commands.ContextMenu(name="Quoter ce message", callback=self.quote_message)
        self.bot.tree.add_command(self.joindate)
        self.bot.tree.add_command(self.quote)

    async def show_join_date(self, interaction: discord.Interaction, member: discord.Member):

        # La fonction format_dt change la date en une représentation lisible par l'humain dans le client officiel.
        await interaction.response.send_message(f'{member} a rejoint le {discord.utils.format_dt(member.joined_at)}')

    async def quote_message(self, interaction: discord.Interaction, message: discord.Message):
        modrole = discord.utils.get(interaction.guild.roles, id=845027528196227133)
        if modrole not in interaction.user.roles:
            await interaction.response.send_message("Seul un modérateur peut quote un message !")
            return

        # On envoie ce message avec ephemeral=True, comme ça seul l'exécuteur de la commande peut le voir.
        await interaction.response.send_message(
            f'Le message a été quote ! Regarde le channel pour le voir !.', ephemeral=True
        )

        # On envoie le message de le salon de quotes.
        star_channel = interaction.guild.get_channel(980431170858811434)

        embed = discord.Embed(title='Citation :', description=message.content, color=discord.Colour.random())

        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
        embed.timestamp = message.created_at

        url_view = ui.View()
        url_view.add_item(
            ui.Button(label='Aller au message', style=discord.ButtonStyle.url, url=message.jump_url))

        await star_channel.send(embed=embed, view=url_view)


# On ajoute le cog au bot.
async def setup(bot):
    await bot.add_cog(ContextMenu(bot))
