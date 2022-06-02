import inspect
import os
import discord
import datetime
import time
import pytz
import random
import emoji
from discord.ext.commands import Context

from cogs.CONSTANTS import CESTify, prettytime
import requests
import json
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import urllib.request

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

extensions = (
    "cogs.help",
    "cogs.listeners",
    "cogs.memes",
    "cogs.app_commands",
    #"cogs.data",
    #"cogs.birthday",
    "cogs.random",
    "cogs.moderation",
    "cogs.fun",
    "cogs.useful"
)


class MyBot(commands.Bot):
    def __init__(self, *, command_prefix, case_insensitive, help_command, intents, application_id):
        super().__init__(command_prefix=command_prefix, case_insensitive=case_insensitive, help_command=help_command, intents=intents, application_id=application_id)

    async def on_ready(self) -> None:
        print("Le bot est prêt !")
        #await bot.change_presence(activity=discord.Game(name="Je suis un bot créé par PetitFrapo !"))
        print("Le statut est prêt !")

    async def setup_hook(self):
        for ext in extensions:
            await self.load_extension(ext)
        self.loop.create_task(presence())
        self.tree.copy_global_to(guild=discord.Object(id=962604741278449724))
        await self.tree.sync(guild=discord.Object(id=962604741278449724))



client = discord.Client(intents=default_intents)
bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)

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
    print("Le bot est prêt !")
    print("Le statut est prêt !")



async def presence():
    await bot.wait_until_ready()
    while not bot.is_closed():
        presences = ["Respectez moi sinon grr", "Je suis un bot créé par PetitFrapo !", "la vi c pa un kiwi", "mon magnifique code.", "Essaie d'avoir un statut custom ++"]
        game = random.choice(presences)
        if game != presences[3]:
            await bot.change_presence(activity=discord.Game(name=game))
        else:
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.watching) )
        await asyncio.sleep(5)



@bot.command(name="interesting", description="Quand quelque chose est intéressant", help="Intéressant...")
async def interesting(ctx):
    await ctx.send("Hmm, oui je vois, très intéressant...")


@bot.command(name="invite", help="Crée une invitation.", description="Crée une invitation pour le salon actuel.")
async def invite(ctx):
    invite = await ctx.channel.create_invite()
    await ctx.channel.send(f"Voici l'invitation : {invite} !")


@bot.command(name="ping", help="NOTIFICATION INTENSIFIES", description="Notifie la personne précisée.")
async def ping(message, user: discord.Member = ""):
    if user == "":
        await message.channel.send(content=message.author.mention)
    else:
        await message.channel.send(content=user.mention)


@bot.command(name="quote")
async def quote(message):
    quotes = ["Je cite : J'ai pas la mouna, par Yvain, dans la vidéo Let's Play Minish Cap Randomizer #2.",
              "Je cite : TU ES MON CHEVAL, par PetitFrapo, en MP avec Yvain.",
              "Je cite : Il faut que j'aille au mont Gounegueule, \
               par Yvain, dans la vidéo du Let's Play #1, #1.2 et #2.",
              "Je cite : MAIS C'EST SUPER TA VIE, \
               par Yvain à un pauvre petit commercant de la cité d'Hyrule, \
               dans la vidéo du Let's Play Minish Cap Randomizer #2.",
              "Je cite : Ils ont l'Ultra-Instinct ! ILS ONT L'ULTRA INSTINCT !! \
              , par Yvain, dans le Jeudi de la souffrance sur Deathtroid.",
              "Je cite : spoiler : c'est pour que ce soit pas un spoiler., par PetitFrapo, sur le salon bac-à-sable.",
              "Je cite : En vrai c'est pas évident de faire un truc moche et de le rendre stylé ^^, par Yvain, sur le salon chat-modos (auquel vous n'avez pas accès niark niark)."]
    await message.channel.send(random.choice(quotes))


@bot.command(name="say", description="Faites dire quelque chose à i20", aliases=["s"])
async def say(ctx, *, textToSay):
    await ctx.message.delete()
    swear_words = ["putain", "merde", "con", "connard", "fuck", "damn", "hell", "bordel", "pute", "shit", "everyone"]
    swear_flag = None
    a = 0
    for i in swear_words:
        if i in str(textToSay).lower():
            swear_flag = True
            break
        else:
            swear_flag = False
    if swear_flag == True:
        try:
            await ctx.author.send("JAMAIS JE NE DIRAI CE GENRE DE CHOSES MAIS OÙ VA LE MONDE !")
        except:
            await ctx.channel.send("JAMAIS JE NE DIRAI CE GENRE DE CHOSES MAIS OÙ VA LE MONDE !", delete_after=5)
    else:
        if len(ctx.message.attachments) != 0:
            file = await ctx.message.attachments[0].to_file()
            await ctx.channel.send(textToSay, file=file)
        else:
            await ctx.send(textToSay)


@bot.command(name="date", help="romance.", aliases=["love", "rdv"])
async def date(ctx, user: commands.MemberConverter = "", user2: commands.MemberConverter = ""):
    if user == "":
        await ctx.channel.send(f"{ctx.author.name} est en rendez-vous avec i20 !")
    elif user != "" and user2 == "":
        await ctx.channel.send(f"{user.display_name} est en date avec i20!")
    else:
        await ctx.channel.send(f"{user.display_name} est en date avec {user2.display_name} !")



@bot.command(name="flip", help="Pile ou face ?", aliases=["pf"])
async def flip(ctx):
    coin = random.choice(["heads", "tails"])
    await ctx.channel.send("Suspense...")
    time.sleep(3)
    if coin == "heads":
        await ctx.channel.send("Le pièce est tombée sur pile.")
        await ctx.channel.send("http://assets.stickpng.com/images/580b585b2edbce24c47b27c1.png")
    else:
        await ctx.channel.send("La pièce est tombée sur face.")
        await ctx.channel.send(
            "https://upload.wikimedia.org/wikipedia/fr/3/34/Piece-2-euros-commemorative-2012-france.png")


@bot.command(name="bonk")
async def bonk(ctx):
    await ctx.send("B O N K")
    await ctx.send("https://media.discordapp.net/attachments/858632881139875840/924339843771809802/IMG_3748.jpg")


@bot.command(name="bestcommandever")
@commands.has_role("Modérateurs")
async def bestcommandever(ctx, user: discord.User="Amaury#3218"):
    print(user)
    await user.send("Réveille toi maumau")
    if user != "Amaury#3218":
        await ctx.send("non cette commande a été créée pour maumau")
    await user.send(user.mention)
    await ctx.send("niark niark")



@bot.command(name="maumauvictime")
async def maumauvictime(ctx):
    id = '<@693481596300296204>'
    if ctx.author.name != "PetitFrapo":
        print("worked")
        modrole = discord.utils.get(ctx.guild.roles, id=845027528196227133)
        if modrole in ctx.author.roles:
            await ctx.message.delete()
            await ctx.send("https://cdn.discordapp.com/attachments/855517672211742720/934439168732438628/Capture_decran_2022-01-22_a_14.26.53.png")
            for i in range(1, 11):
                await ctx.send(id)
            await ctx.send("j'suis désolé")
    else:
        await ctx.message.delete()
        await ctx.send(
            "https://cdn.discordapp.com/attachments/855517672211742720/934439168732438628/Capture_decran_2022-01-22_a_14.26.53.png")
        for i in range(1, 11):
            await ctx.send(id)
            await ctx.send("j'suis désolé")




class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Commandes classiques", emoji="🔧", description="Les commandes classiques  !"),
            discord.SelectOption(label="Commandes slash", emoji="🔨", description="Les commandes slash (nouveauté) !")
        ]
        super().__init__(placeholder="Veuillez choisir une catégorie de commandes",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Commandes classiques":
            classhelp = discord.Embed(title="Les commandes d'i20 :",
                                      color=0x110b7a,
                                      description="---\ni20 est un bot possédant plein de commandes, les voici :")
            classhelp.add_field(name="Fun :",
                                value="*__i!interesting__* : Intéressant...\n *__i!flip__* : Pile ou face ?\n *__i!meme__* : Génère un meme aléatoire.\n *__i!date__* : romance.\n *__i!ping__* : NOTIFICATION INTENSIFIES\n *__i!say__* : Faites dire quelque chose à i20 ! Ne dites pas de gros mots ou gare à vous !\n *__i!quote__* : Les citations cultes d'Yvain et PetitFrapo !\n *__i!embed__* : Crée un embed (càd un texte stylé et encadré et tout!).\n *__i!throw__* : Lance quelque chose sur quelqu'un.\n *__i!ship__* : uwu~\n *__i!randommsg__* : Génère un message aléatoire du salon.",
                                inline=False)

            classhelp.add_field(name="Modération :",
                                value="*__i!ban__* : B O N K le marteau\n *__i!unban__* : uaetram el K N O B\n *__i!kick__* : Pour kick les gens pas trétré genti\n *__i!clear__* : Supprime des messages du salon.\n *__i!pin__* : Épingle le message qui est répondu.\n *__i!warn__* : Permet de warn un utilisateur.\n *__i!removewarn__* : Retire un warn à quelqu'un.",
                                inline=False)
            classhelp.add_field(name="Utile :",
                                value="*__i!invite__* : Crée une invitation du serveur.\n *__i!avatar__* : Obtient l'avatar du membre.\n *__i!help__* : Affiche ce message.\n *__i!poll__* : Crée un sondage.\n *__i!ost__* : Génère une OST aléatoire.\n *__i!id__* : Prends l'ID de quelqu'un.\n *__i!warns__* : Vois tes avertissements.",
                                inline=False)
            classhelp.add_field(
                name="__*Pour avoir plus de précision sur une commande, veuillez faire 'i!help nomDeLaCommande'.*__",
                value="Merci à Amaury pour l'aide qu'il a donnée pour la commande <3\n Vous pouvez aussi faire **i!help syntax** pour en apprendre plus sur la syntaxe utilisée dans l'explication des utilisations des commandes.\n---",
                inline=False)
            await interaction.response.edit_message(embed=classhelp)
        elif self.values[0] == "Commandes slash":
            slashhelp = discord.Embed(title="Les commandes slash d'i20 :", description="---\ni20 possède aussi une toute nouvelle fonctionnalité : les commandes slash. Les voici :", color=0x110b7a)
            slashhelp.add_field(name="Fun :",
                                value="*__/8ball__* : Demandez une question à i20, il vous répondra !\n *__/flip__* : Pile ou face ?",
                                inline=False)
            slashhelp.add_field(name="Modération :",
                                value="*__/ban__* : B O N K le slashteau",
                                inline=False)
            slashhelp.add_field(name="Utile :",
                                value="*__/sum__* : Additionne deux nombres.\n *__/poll__* : Crée un sondage.\n *__/embed__* : Crée un embed.\n *__/hexa__* : Traduis un nombre en héxadécimal.\n *__/info__* : Informations sur i20.\n *__/shorten__* : Raccourcis une URL.")
            await interaction.response.edit_message(embed=slashhelp)


class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 360):
        super().__init__(timeout=timeout)
        self.add_item(Select())


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







'''@bot.command(name="submit")
async def submit(ctx: commands.Context):
    class SubmitButton(discord.ui.Button)
        def __init__(self):
            label = "Soumets une idée !"
            style = discord.ButtonStyle.green 
            url = "https://youtu.be/dQw4w9WgXcQ")
            super().__init__(label=label, style=style, url=url)
            
        async def callback(self, interaction: discord.Interaction) -> typing.Any:
            f = open("cogs/jsondata/submits.json")
            data = json.load(f)
            f.close()
            id = interaction.author.id
            if data[id] is None:
                data[id] = []
            data["id"].append({"timestamp": prettytime(CESTify(datetime.datetime.now())), "title": })
            
    view = discord.ui.View()
    view.add_item(button)
    await ctx.send(view=view)'''


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
                line = f"from cogs.{command.cog_name.lower()} import {command.cog_name}"
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

bot.run(os.getenv("TOKEN"))
