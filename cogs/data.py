# Ne pas le mettre dans le code source public.

import json
import discord
from discord.ext import commands
from discord.ext.commands import Cog
from cogs.cogutils import MyBot

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents,
            application_id=853301761572732928)

DATABASE = bot.get_guild(981950727511474266)
registers_channel = DATABASE.get_channel(981950728056754200)

class Data(Cog):
    def __init__(self, bot):
        self.bot = bot

    def whichaddin(self, string: str) -> str:
        if string[0].lower() in {"a", "e", "i", "o", "u", "y"}:
            addin = "'"
        else:
            addin = "e "
        return addin

    @commands.group(pass_context=True)
    async def data(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Veuillez utiliser un des modes :  i!data add, i!data remove, i!data get ou i!data show.")

    @data.command(pass_context=True, name="add")
    async def register(self, ctx, name, value):
        id = str(ctx.author.id)
        f = open("cogs/jsondata/registers.json", "r", encoding="utf8")
        data = json.load(f)
        f.close()
        if not id in data.keys():
            data[id] = {}
        data[id][name] = value
        f = open("cogs/jsondata/registers.json", "w")
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.close()
        await ctx.send(f"La valeur **{value}** a bien été associée à la clé **{name}** dans ta table personnelle !")

    @data.command(name="remove", pass_context=True)
    async def retire(self, ctx, key):
        id = str(ctx.author.id)
        f = open("jsondata/registers.json", "r", encoding="utf8")
        data = json.load(f)
        f.close()
        if not id in data.keys():
            await ctx.send("Tu ne peux pas retirer de valeurs puisque tu n'as pas de table !")
        else:
            if key not in data[id].keys():
                await ctx.send(f"La valeur **{key}** n'existe pas ! Tu ne peux donc pas la retirer !")
            else:
                del data[id][key]
                f = open("jsondata/registers.json", "w")
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.close()
                await ctx.send(f"La clé **{key}** a bien été retirée de ta table !")

    @data.command(pass_context=True, name="get")
    async def acquire(self, ctx, key):
        id = str(ctx.author.id)
        f = open("cogs/jsondata/registers.json", "r", encoding="utf8")
        data = json.load(f)
        f.close()
        if not id in data.keys():
            await ctx.send(
                "Tu n'as aucune valeur dans ta table ! Fais **i!data add [nomDeLaClé] [valeur]** pour en rajouter une.")
        else:
            if key not in data[id].keys():
                await ctx.send(
                    f"La valeur **{key}** n'existe pas ! Fais **i!data add {key} [valeur]** pour la rajouter.")
            else:
                lookedfor = data[id][key]
                await ctx.send(f"La clé **{key}** possède la valeur **{lookedfor}** dans ta table !")

    @data.command(pass_context=True, name="show")
    async def showall(self, ctx):
        id = str(ctx.author.id)
        f = open("cogs/jsondata/registers.json", "r", encoding="utf8")
        data = json.load(f)
        f.close()
        if not id in data.keys():
            await ctx.send(
                "Tu n'as aucune valeur dans ta table ! Fais **!data add [nomDeLaClé] [valeur]** pour en rajouter une.")
        else:
            list = []
            prettylist = f""
            for i in data[id].keys():
                list.append([i, data[id][i]])
                prettylist = prettylist + f"**{i}** : {data[id][i]}\n"

            if prettylist == "":
                await ctx.send(
                    "Tu n'as aucune valeur dans ta table ! Fais **!data add [nomDeLaClé] [valeur]** pour en rajouter une.")
            else:
                embed = discord.Embed(title=f"Table de {ctx.author.name} :", description=prettylist,
                                      colour=discord.Colour.random())
                await ctx.send(embed=embed)

    @data.command(name="addfor", pass_context=True)
    async def addfor(self, ctx, target: discord.Member, name: str, value: str):
        id = str(target.id)
        if ctx.author.id not in {558317667505668098, 693481596300296204}:
            await ctx.send("Tu ne peux pas exécuter cette sous-commande !")
        else:
            f = open("cogs/jsondata/registers.json", "r", encoding="utf8")
            data = json.load(f)
            f.close()
            if id not in data.keys():
                data[id] = {}
            data[id][name] = value
            f = open("jsondata/registers.json", "w")
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.close()
            await ctx.send(
                f"La valeur **{value}** a bien été associée à la clé **{name}** dans la table de {target.name} !")

    @data.command(name="removefor", pass_context=True)
    async def retirefor(self, ctx, target: discord.Member, key: str):
        id = str(target.id)
        if not ctx.author.id in {558317667505668098, 693481596300296204}:
            await ctx.send("Tu ne peux pas exécuter cette sous-commande !")
        else:
            f = open("cogs/jsondata/registers.json", "r", encoding="utf8")
            data = json.load(f)
            f.close()
            if not id in data.keys():
                await ctx.send(f"Tu ne peux pas retirer de valeurs puisque {target.name} n'a pas de table !")
            else:
                if not key in data[id].keys():
                    await ctx.send(f"La valeur **{key}** n'existe pas ! Tu ne peux donc pas la retirer !")
                else:
                    del data[id][key]
                    f = open("cogs/jsondata/registers.json", "w")
                    json.dump(data, f, indent=4, ensure_ascii=False)
                    f.close()
                    name = target.name
                    if name[0].lower() in {"a", "e", "i", "o", "u", "y"}:
                        addin = "'"
                    else:
                        addin = "e "
                    await ctx.send(f"La clé **{key}** a bien été retirée de la table d{addin}{target.name}!")

    @data.command(name="getfor", pass_contetx=True)
    async def getfor(self, ctx, target: discord.Member, key: str):
        id = str(target.id)
        if not ctx.author.id in {558317667505668098, 693481596300296204}:
            await ctx.send("Tu ne peux pas exécuter cette sous-commande !")
        else:
            f = open("cogs/jsondata/registers.json", "r", encoding="utf8")
            data = json.load(f)
            f.close()
            if not id in data.keys():
                await ctx.send(f"Il n'y a aucune valeur dans la table de {target.name} !")
            else:
                if not key in data[id].keys():
                    await ctx.send(f"La valeur **{key}** n'existe pas !")
                else:
                    lookedfor = data[id][key]
                    addin = self.whichaddin(target.name)
                    await ctx.send(
                        f"La clé **{key}** possède la valeur **{lookedfor}** dans la table d{addin}{target.name} !")

    @data.command(pass_context=True, name="showfor")
    async def showfor(self, ctx, member: discord.Member):
        id = str(member.id)
        if not ctx.author.id in {558317667505668098, 693481596300296204}:
            await ctx.send("Tu ne peux pas exécuter cette sous-commande !")
        else:
            f = open("cogs/jsondata/registers.json", "r", encoding="utf8")
            data = json.load(f)
            f.close()
            if not id in data.keys():
                await ctx.send("Cette table ne contient aucune valeur !")
            else:
                list = []
                prettylist = f""
                for i in data[id].keys():
                    list.append([i, data[id][i]])
                    prettylist = prettylist + f"**{i}** : {data[id][i]}\n"
                if prettylist == "":
                    await ctx.send("Cette table ne contient aucune valeur !")
                else:
                    embed = discord.Embed(title=f"Table de {member.name} :", description=prettylist,
                                          colour=discord.Colour.random())
                    await ctx.send(embed=embed)

    @data.command(name="help", pass_context=True)
    async def datahelp(self, ctx, com: str = ""):
        nope = False
        com = com.lower()
        if com == "":
            embed = discord.Embed(title="Help sur la commande **i!data** :",
                                  description="*__i!data **add**__* : Ajoute une valeur à ta table.\n*__i!data **remove**__* : Retire une valeur de ta table.\n*__i!data **get**__* : Obtiens une valeur de ta table.\n*__i!data **show**__* : Monte ta table.\n",
                                  colour=discord.Colour.random())
        elif com == "add":
            embed = discord.Embed(title="i!data add :",
                                  description="Ajoute une valeur dans ta table personnelle, seul toi (ou PetitFrapo) y a accès.\n**Utilisation** : i!data add [nomDeLaClé] [value]",
                                  colour=discord.Colour.random())
        elif com == "remove":
            embed = discord.Embed(title="i!data remove :",
                                  description="Retire une valeur dans ta table personnelle.\n**Utilisation** : i!data remove [nomDeLaClé]",
                                  colour=discord.Colour.random())
        elif com == "get":
            embed = discord.Embed(title="i!data get :",
                                  description="Obtient une valeur dans ta table personnelle.\n**Utilisation** : i!data get [nomDeLaClé]",
                                  colour=discord.Colour.random())
        elif com == "show":
            embed = discord.Embed(title="i!data show :",
                                  description="Montre ta table dans son entièreté.\n**Utilisation** : i!data show",
                                  colour=discord.Colour.random())
        else:
            embed = None
            await ctx.send(f"La commande {com} n'existe pas !")
            nope = True
        if not nope:
            await ctx.send(embed=embed)


async def setup(bot: MyBot):
    await bot.add_cog(Data(bot))
