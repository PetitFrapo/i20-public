# Cette partie du code n'est pas un cog, mais rassemble des commandes qui me sont utiles dans multiples fichiers,
# donc je peux les importer peu importe ou je suis.
# C'est pour ça que dans presque tous les fichiers, il est possible de voir "from cogs.cogutils import *".

import datetime
import typing
from typing import *
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
        # i20 Playground
        self.tree.copy_global_to(guild=discord.Object(id=962604741278449724))
        # Yvain
        self.tree.copy_global_to(guild=discord.Object(id=845026449495818240))

        await self.tree.sync(guild=discord.Object(id=962604741278449724))
        await self.tree.sync(guild=discord.Object(id=845026449495818240))


def CESTify(date: datetime.datetime) -> datetime.datetime:
    return date.astimezone(timezone)


def prettytime(date: datetime.datetime) -> str:
    return date.strftime("%d/%m/%Y %H:%M")


async def get_db(ctx: commands.Context,
                 bot: Union[commands.Bot, MyBot, MyBotTree],
                 channel_id: int,
                 id: Union[str, int]) -> typing.Tuple[dict, discord.Message]:
    """Gets the dict and Message objects necessary for Discord server database hosting."""
    database = bot.get_guild(981950727511474266)
    registers_channel = database.get_channel(channel_id)
    history = registers_channel.history(limit=None)
    iterations = 0
    notin = 0
    async for message in history:
        iterations += 1
        if id not in message.content:
            notin += 1
    if notin == iterations:
        string = "{\"" + id + "\": {}}"
        msg = await registers_channel.send(string)
        dictid: discord.Message = msg
        data = eval(msg.content)
    else:
        async for message in registers_channel.history(limit=None):
            dictiona: dict = eval(message.content)
            if id in dictiona.keys():
                dictid: discord.Message = message
                data = dictiona

    return (data, dictid)


async def get_birthday_task_db(bot: MyBot):
    """Gets the dict and Message objects necessary for Discord server database hosting."""
    database = bot.get_guild(981950727511474266)
    registers_channel = database.get_channel(982186759775473674)
    history = registers_channel.history(limit=None)
    data = []
    async for message in history:
        dict = eval(message.content)
        data.append(dict)

    return data


async def get_all_db(ctx: commands.Context,
                     bot: Union[commands.Bot, MyBot, MyBotTree],
                     channel_id: int):
    """Gets the dict and Message objects necessary for Discord server database hosting."""
    database = bot.get_guild(981950727511474266)
    registers_channel = database.get_channel(channel_id)
    history = registers_channel.history(limit=None)
    data = []
    async for message in history:
        dictmsg = eval(message.content)
        data.append(dictmsg)

    return data


class SimpleEmbed(discord.Embed):
    def __init__(self, title: str, description: str, footer: Optional[str], color: Optional[str], author: Optional[str], fields: Optional[List[Tuple[str, str]]]):
        super().__init__(title=title, description=description, colour=color)
        self.set_footer(text=footer)
        self.set_author(name=author)
        for i in fields:
            self.add_field(name=i[0], value=i[1])


class RCEmbed(SimpleEmbed):
    def __init__(self, title, description, footer, author, fields):
        super().__init__(title=title, description=description, author=author, fields=fields, footer=footer,
                         color=discord.Colour.random())


