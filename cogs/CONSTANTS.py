import discord
from discord.ext import commands
import pytz

timezone = pytz.timezone("Europe/Paris")


class MyBot(commands.Bot):
    def __init__(self, *, command_prefix, case_insensitive, help_command, intents, application_id):
        super().__init__(command_prefix=command_prefix, case_insensitive=case_insensitive, help_command=help_command, intents=intents, application_id=application_id)


class MyBotTree(commands.Bot):
    def __init__(self, *, command_prefix, case_insensitive, help_command, intents, application_id):
        super().__init__(command_prefix=command_prefix, case_insensitive=case_insensitive, help_command=help_command, intents=intents, application_id=application_id)

class MyBotTreeCopyToYvain(commands.Bot):
    def __init__(self, *, command_prefix, case_insensitive, help_command, intents, application_id):
        super().__init__(command_prefix=command_prefix, case_insensitive=case_insensitive, help_command=help_command, intents=intents, application_id=application_id)


    async def setup_hook(self):
        # SCT
        self.tree.copy_global_to(guild=discord.Object(id=962604741278449724))
        # Yvain
        self.tree.copy_global_to(guild=discord.Object(id=845026449495818240))

        await self.tree.sync(guild=discord.Object(id=962604741278449724))
        await self.tree.sync(guild=discord.Object(id=845026449495818240))

def CESTify(date):
    return date.astimezone(timezone)

def prettytime(date):
    return date.strftime("%d/%m/%Y %H:%M")
