# Cette partie du code représente l'implémentation du système d'anniversaire au bot.

from discord import ui
from discord.ext import tasks
from discord.ext.commands import Cog, Context
from cogs.cogutils import *

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)


class BirthdayDB(discord.ui.Modal):
    def __init__(self, ctx, bot):
        self.ctx = ctx
        self.bot = bot
        super().__init__(title='Anniversaire :')

    date = discord.ui.TextInput(label='Date (format DD/MM)', placeholder="Exemple : 30/04.")
    year = discord.ui.TextInput(label='Année de naissance (NON OBLIGATOIRE)', required=False, placeholder="Exemple : 1998.")
    whattosend = discord.ui.TextInput(label="Un mot à t'envoyer lors de ton anniversaire.", required=False, placeholder="Mets \"{age}\" là où tu veux mettre ton âge.")
    # mention = discord.ui.TextInput(label="Veux-tu être mentionné avec le message ?", required=True, placeholder="\"Oui\" ou \"Non\".")
    mentiontest = ui.Select(placeholder="Veux-tu être mentionné avec le message ?", options=[discord.SelectOption(label="Oui, je veux être mentionné.", emoji="👍"), discord.SelectOption(label="Non, je ne veux pas être mentionné.", emoji="👎")])


    async def on_submit(self, interaction: discord.Interaction):
        if self.whattosend is None:
            whattosend = f"Joyeux anniversaire {interaction.user} !"
        id = str(interaction.user.id)
        data, dictid = await get_db(self.ctx, self.bot, 982186759775473674, id)

        data[id]["date"] = str(self.date)
        data[id]["year"] = str(self.year)
        data[id]["message"] = str(self.whattosend)
        data[id]["mention?"] = str(self.mentiontest.values[0])

        await dictid.edit(content=str(data))
        await interaction.response.send_message(f'D\'accord, je t\'enverrai le message \"{self.whattosend}\" le {self.date} !', ephemeral=True)


class Button(discord.ui.Button):
    def __init__(self, ctx, bot):
        self.ctx = ctx
        self.bot = bot
        super().__init__(style=discord.ButtonStyle.blurple, label="Clique pour rentrer ton anniversaire !")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BirthdayDB(self.ctx, self.bot))



class BirthdayCog(Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.birthday_task.start()

    @commands.hybrid_group(name="birthday")
    async def birthday(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Veuillez utiliser une sous-commande.")

    @birthday.command(name="set", description="Entre ton anniversaire et sois notifié le jour J !")
    async def bdset(self, ctx):
        button = Button(ctx, self.bot)
        await ctx.send(view=ui.View().add_item(button))

    @birthday.command(name="remove", description="Retire ton anniversaire de la liste.")
    async def bdremove(self, ctx: Context):
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 982186759775473674, id)
        await dictid.delete()
        await ctx.send("Tes informations d'anniversaire ont bien éte supprimées !")

    @birthday.command(name="list", description="Montre les anniversaires de tout le monde !")
    async def bdlist(self, ctx: Context):
        bdlist = await get_all_db(ctx, self.bot, 982186759775473674)
        string = ""
        iterations = 0
        for bd in bdlist:
            iterations += 1
            for i in bd.keys():
                id = i
                member = self.bot.get_user(int(id))
                string += f"{member.name} : {bd[id]['date']}.\n"
        embed = discord.Embed(title="Anniversaires du serveur :", description=string, colour=discord.Colour.random())
        await ctx.send(embed=embed)

    @tasks.loop(hours=24)
    async def birthday_task(self):
        data = await get_birthday_task_db(self.bot)
        for dictionary in data:
            for i in dictionary.keys():
                id = i
            date = dictionary[id]["date"]
            if datetime.datetime.today().strftime("%d/%m") == date:
                year = dictionary[id]["year"]
                message = dictionary[id]["message"]
                if dictionary[id]["mention?"].lower() in {"oui, je veux être mentionné.", "oui"}:
                    mention = True
                else:
                    mention = False
                age = int(datetime.datetime.now().strftime("%Y")) - int(year)
                message = message.replace("{age}", str(age))

                # Le monde d'Yvain
                guild = self.bot.get_guild(845026449495818240)
                birthday_channel: discord.TextChannel = guild.get_channel(985088152488251443)

                # i20 Playground
                # guild: discord.Guild = self.bot.get_guild(962604741278449724)
                # birthday_channel: discord.TextChannel = guild.get_channel(985090104139857950)

                user = self.bot.get_user(int(id))
                if mention:
                    await birthday_channel.send("--------------------------")
                    await birthday_channel.send(f"🥳🥳🥳🎉🎉 {user.mention} 🎉🎉🥳🥳🥳")
                    await birthday_channel.send("----------- **JOYEUX ANNIVERSAIRE** -----------")
                await birthday_channel.send(message)

    @birthday_task.before_loop
    async def wait_until_7am(self):
        now = CESTify(datetime.datetime.now())
        next_run = now.replace(hour=8, minute=30, second=0)

        if next_run < now:
            next_run += datetime.timedelta(days=1)

        await discord.utils.sleep_until(next_run)


# On ajoute le cog au bot.
async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))
