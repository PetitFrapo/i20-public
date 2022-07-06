# Cette partie du code représente les commandes slash et pas hybrides (sauf send),
# Il y en a beaucoup, n'hésitez pas à faire i!help ou /help sur le serveur pour les connaître toutes !

import datetime
import os
import random
import typing
from typing import *

import discord
import pytz
import requests
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Cog, Context
from discord import ui
from cogs.cogutils import MyBot, get_db, get_db_no_ctx, CallbackButton

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)
timezone = pytz.timezone("Europe/Paris")


class Slash(Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
        tree = self.bot.tree

    @app_commands.command(name="math", description="Utilise i20 comme une calculette !")
    @app_commands.describe(terme1="Premier terme.", operateur="L'opérateur à utiliser.", terme2="Deuxième terme.")
    async def math(self, interaction: discord.Interaction, terme1: int, operateur: str, terme2: int):
        if operateur not in {"+", "-", "*", "/", "//", "**", "%"}:
            await interaction.response.send_message("L'opérateur n'est pas correct !", ephemeral=True)
            return
        result = eval(f"{terme1} {operateur} {terme2}")
        await interaction.response.send_message(f"{terme1} {operateur} {terme2} = {result}", ephemeral=True)

    @math.autocomplete("operateur")
    async def mathautocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        operators = ["+", "-", "*", "/", "//", "**", "%"]
        return [
            app_commands.Choice(name=operator, value=operator)
            for operator in operators if current.lower() in operator.lower()
        ]

    @app_commands.command(name="embed", description="Crée un embed.")
    @app_commands.describe(titre="Le titre du embed.", descr="La description du embed.",
                           titrechamp1="Le titre du premier champ.", descrchamp1="La description du premier champ.",
                           titrechamp2="Le titre du deuxième champ.", descrchamp2="La description du deuxième champ.",
                           footer="Le footer à mettre.")
    async def slashembed(self, interaction: discord.Interaction, titre: str, descr: str, titrechamp1: typing.Optional[str],
                    descrchamp1: typing.Optional[str], titrechamp2: typing.Optional[str],
                    descrchamp2: typing.Optional[str], footer: typing.Optional[str]):
        embed = discord.Embed(title=titre, description=descr)
        if titrechamp1 is not None and descrchamp1 is not None:
            embed.add_field(name=titrechamp1, value=descrchamp1)
        if titrechamp2 is not None and descrchamp2 is not None:
            embed.add_field(name=titrechamp2, value=descrchamp2)
        if footer is not None:
            embed.set_footer(text=footer)
        await interaction.response.send_message(embed=embed, ephemeral=False)
        await self.bot.tree.sync(guild=discord.Object(id=962604741278449724))

    @app_commands.command(name="hexa", description="Convertis en hexadécimal !")
    @app_commands.describe(nombre="Le nombre à transformer en hexadécimal.")
    async def tohex(self, interaction: discord.Interaction, nombre: int):
        await interaction.response.send_message(hex(nombre)[2:], ephemeral=True)

    @app_commands.command(name="8ball", description="Demande à la boule de cristal...")
    @app_commands.describe(question="Entre ce que tu veux demander à la boule...")
    async def eightball(self, interaction: discord.Interaction, question: str):
        response = ["Oui, ", "Non, ", "Peut-être que "]
        question = question.replace("?", ".")
        question = question.replace("est-ce que ", "")
        question = question.replace("Est-ce que ", "")

        rand = random.choice(response)
        if rand == "Non, ":
            ques = question.split()
            print(ques)

            for i in range(len(ques)):
                if ques[i].startswith("m'"):
                    ques[i] = ques[i].replace(ques[i], f"ne {ques[i][:-1]} pas")
                if ques[i].startswith("j'"):
                    ques[i] = ques[i].replace("j'", "tu ")
                    question = " ".join(ques)
                    ques = question.split()
                    ques[i + 1] = "n'" + ques[i + 1] + " pas"
                    print(ques)
                if ques[i].startswith("je"):
                    ques[i] = ques[i].replace(ques[i], f"ne {ques[i][:-1]} pas")

            question = " ".join(ques)
            if question.endswith("pas"):
                question = question + "."
        question = question.replace("est-ce que ", "")
        question = question.replace("Est-ce que ", "")

        question = question.replace("-t-il", "")
        question = question.replace("-t'il", "")
        question = question.replace("m'", "t'")
        question = question.replace(" me ", " te ")
        question = question.replace("je", "tu")
        question = question.replace("j'", "tu ")

        if question[0].lower() in {"a", "e", "i", "o", "u", "y"}:
            response[2] = "Peut-être qu'"
        finalquest = rand + question
        await interaction.response.send_message(finalquest, ephemeral=False)
        await self.bot.tree.sync()

    @app_commands.command(name="shorten", description="Raccourcis une URL !")
    @app_commands.describe(lien="Le lien à raccourcir.")
    async def cuttly(self, interaction: discord.Interaction, lien: str):
        if not lien.startswith("https://"):
            lien = "https://" + lien
        api_url = f"https://cutt.ly/api/api.php?key={os.getenv('CUTTLY_API_KEY')}&short={lien}"
        data = requests.get(api_url).json()["url"]

        if data["status"] == 7:
            shortened_url = data["shortLink"]
            embedurl = discord.Embed(title="Raccourcisseur URL",
                                     description=f"Voici votre lien raccourci : {shortened_url}")
            await interaction.response.send_message(embed=embedurl)
        else:
            embederreur = discord.Embed(title="Erreur", description=f"Erreur lors du raccourcissement. Erreur {data}")
            await interaction.response.send_message(embed=embederreur)

    @app_commands.command(name="poll", description="Crée un sondage.")
    @app_commands.describe(question="La question du sondage", option1="La première option.",
                           option2="La seconde option.", option3="La troisième option.", option4="La quatrième option.")
    async def slashpoll(self, interaction: discord.Interaction, question: str, option1: str, option2: str,
                        option3: typing.Optional[str] = "", option4: typing.Optional[str] = ""):
        pollChannel: discord.TextChannel = interaction.client.get_channel(922936202909319168)
        # await interaction.message.delete()
        threeOpt = None
        fourOpt = None

        if option3 == "" and option4 == "":
            twoOpt = True
            embed = discord.Embed(title=question, description=f"1️⃣ : {option1}\n 2️⃣ : {option2}",
                                  timestamp=datetime.datetime.now(tz=timezone))
        elif option3 != "" and option4 == "":
            threeOpt = True
            embed = discord.Embed(title=question, description=f"1️⃣ : {option1}\n 2️⃣ : {option2}\n 3️⃣ : {option3}",
                                  timestamp=datetime.datetime.now(tz=timezone))
        elif option3 != "" and option4 != "":
            fourOpt = True
            embed = discord.Embed(title=question,
                                  description=f"1️⃣ : {option1}\n 2️⃣ : {option2}\n 3️⃣ : {option3}\n 4️⃣ : {option4}",
                                  timestamp=datetime.datetime.now(tz=timezone))
        emoji1 = "1️⃣"
        emoji2 = "2️⃣"
        emoji3 = "3️⃣"
        emoji4 = "4️⃣"

        role = discord.utils.get(interaction.guild.roles, id=922944521384374312)
        if role in interaction.user.roles:
            await interaction.user.send(
                "Désolé, tu es banni de la commande /poll... Tu as sûrement joué avec ou spam les sondages...")
        else:
            message = await pollChannel.send(embed=embed)
            await message.add_reaction(emoji1)
            await message.add_reaction(emoji2)
            if threeOpt is True:
                await message.add_reaction(emoji3)
            elif fourOpt is True:
                await message.add_reaction(emoji3)
                await message.add_reaction(emoji4)

        await interaction.response.send_message("Sondage effectué.")

    @app_commands.command(name="ban", description="B O N K le marteau")
    @app_commands.describe(member="La personne à bannir.", reason="La raison du ban.")
    @app_commands.checks.has_role("Modérateurs")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: typing.Optional[str]):
        if member != bot.user:
            if member != interaction.user:
                await interaction.guild.ban(member, reason=reason)
                await interaction.response.send_message(
                    f"{member} a été banni du serveur pour la raison : " + "'" + reason + "'" + " ! MOUAHAHA ! Mon marteau était fatigué...")
            else:
                await interaction.response.send_message("Tu ne peux pas te bannir toi même !")
        else:
            await interaction.response.send_message("n'essaie même pas")

    @commands.hybrid_command(name="send", description="Envoie un message avec un embed, et jusqu'à trois boutons !")
    @app_commands.describe(message="Le texte à envoyer.", embed="L'embed à envoyer.", button1="Le premier bouton à envoyer.", button2="Le second bouton à envoyer.", button3="Le troisième bouton à envoyer.")
    async def send_rich(self, ctx: Context, message: str, embed: Optional[str] = None, button1: Optional[str] = None, button2: Optional[str] = None, button3: Optional[str] = None):
        has_embed, has_view = False, False
        id = str(ctx.author.id)
        if any([button1 is not None, button2 is not None, button3 is not None]):
            buttondata, dictidbtn = await get_db(ctx, self.bot, 981950835036659742, id)
            buttons = [button1, button2, button3]
            view = ui.View()
            for tag in buttons:
                if tag is None:
                    continue
                if tag not in buttondata[id].keys():
                    await ctx.send(f"Le bouton **{tag}** n'existe pas !", ephemeral=True)
                    return
                data = buttondata[id][tag]
                if data["callback"] != "":
                    buttona = CallbackButton(label=data["label"], style=eval(data['style']), url=data["url"], callback=data['callback'])
                else:
                    buttona = ui.Button(label=data["label"], style=eval(data['style']), url=data["url"])
                view.add_item(buttona)
                has_view = True

        if embed is not None:
            embeddata, dictidembed = await get_db(ctx, self.bot, 981950865348890644, id)
            if embed not in embeddata[id].keys():
                await ctx.send(f"L'embed **{embed}** n'existe pas !", ephemeral=True)
                return
            embd = discord.Embed().from_dict(embeddata[id][embed])
            has_embed = True

        if has_embed and has_view:
            await ctx.send(message, embed=embd, view=view)
        elif has_embed and not has_view:
            await ctx.send(message, embed=embd)
        elif not has_embed and has_view:
            await ctx.send(message, view=view)
        else:
            await ctx.send(message)

    @send_rich.autocomplete("embed")
    async def dbsendembedac(self, interaction: discord.Interaction,
                              current: str) -> List[app_commands.Choice[str]]:
        id = str(interaction.user.id)
        data, dictid = await get_db_no_ctx(bot=self.bot, channel_id=981950865348890644, id=id)
        tags = []
        for key in data[id].keys():
            tags.append(key)
        return [
            app_commands.Choice(name=tag, value=tag)
            for tag in tags if current.lower() in tag.lower()
        ]

    @send_rich.autocomplete("button1")
    async def dbbutton1sendac(self, interaction: discord.Interaction,
                              current: str) -> List[app_commands.Choice[str]]:
        id = str(interaction.user.id)
        data, dictid = await get_db_no_ctx(bot=self.bot, channel_id=981950835036659742, id=id)
        tags = []
        for key in data[id].keys():
            tags.append(key)
        return [
            app_commands.Choice(name=tag, value=tag)
            for tag in tags if current.lower() in tag.lower()
        ]

    @send_rich.autocomplete("button2")
    async def dbbutton2sendac(self, interaction: discord.Interaction,
                              current: str) -> List[app_commands.Choice[str]]:
        id = str(interaction.user.id)
        data, dictid = await get_db_no_ctx(bot=self.bot, channel_id=981950835036659742, id=id)
        tags = []
        for key in data[id].keys():
            tags.append(key)
        return [
            app_commands.Choice(name=tag, value=tag)
            for tag in tags if current.lower() in tag.lower()
        ]

    @send_rich.autocomplete("button3")
    async def dbbutton3sendac(self, interaction: discord.Interaction,
                              current: str) -> List[app_commands.Choice[str]]:
        id = str(interaction.user.id)
        data, dictid = await get_db_no_ctx(bot=self.bot, channel_id=981950835036659742, id=id)
        tags = []
        for key in data[id].keys():
            tags.append(key)
        return [
            app_commands.Choice(name=tag, value=tag)
            for tag in tags if current.lower() in tag.lower()
        ]


# On ajoute le cog au bot.
async def setup(bot):
    await bot.add_cog(Slash(bot))
