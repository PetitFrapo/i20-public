import datetime
import discord
import json
from discord.ext import commands
from discord.ext.commands import Cog
from cogs.CONSTANTS import MyBot

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)


class Birthday(discord.ui.Modal, title='Anniversaire :'):
    date = discord.ui.TextInput(label='Date (format DD/MM)', placeholder="Exemple : 30/04.")
    year = discord.ui.TextInput(label='Année de naissance (NON OBLIGATOIRE)', required=False, placeholder="Exemple : 1998.")
    whattosend = discord.ui.TextInput(label="Un mot à t'envoyer lors de ton anniversaire.", required=False, placeholder="Mets \"{age}\" là où tu veux mettre ton âge.")
    mention = discord.ui.TextInput(label="Veux-tu être mentionné avec le message ?", required=True, placeholder="\"Oui\" ou \"Non\".")


    async def on_submit(self, interaction: discord.Interaction):
        if self.whattosend is None:
            whattosend = f"Joyeux anniversaire {interaction.user} !"
        await interaction.response.send_message(f'D\'accord, je t\'enverrai le message \"{self.whattosend}\" le {self.date} !', ephemeral=True)
        id = str(interaction.user.id)
        f = open("cogs/jsondata/birthday.json", "r", encoding="utf8")
        data = json.load(f)
        f.close()
        if not id in data.keys():
            data[id] = {}
        data[id]["date"] = str(self.date)
        data[id]["year"] = str(self.year)
        data[id]["message"] = str(self.whattosend)
        data[id]["mention?"] = str(self.mention)
        f = open("jsondata/birthday.json", "w")
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.close()


class Button(discord.ui.Button):
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Birthday())

class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(style=discord.ButtonStyle.blurple, label="Clique pour rentrer ton anniversaire !"))


class BirthdayCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="birthday")
    async def birthday(self, ctx):
        await ctx.send(view=ButtonView())

    @commands.command(name="forcebdaymsg")
    async def fbdm(self, ctx):
        id = str(ctx.author.id)
        f = open("cogs/jsondata/birthday.json", "r", encoding="utf8")
        data = json.load(f)
        f.close()
        date = data[id]["date"]
        year = data[id]["year"]
        message = data[id]["message"]
        if data[id]["mention?"].lower() in {"oui", "yes", "true", "y"}:
            mention = True
        else:
            mention = False
        age = int(datetime.datetime.now().strftime("%Y")) - int(year)
        print(age)
        message = message.replace("{age}", str(age))
        if mention:
            for i in range(10):
                await ctx.send(f"🥳🥳🥳🎉🎉 {ctx.author.mention} 🎉🎉🥳🥳🥳")
                await ctx.send("**JOYEUX ANNIVERSAIRE**")
        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))
