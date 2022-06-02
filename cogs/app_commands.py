import asyncio
import datetime
import os
import random
import typing
from typing import List, Optional, Tuple

import discord
import pytz
import requests
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Cog
from discord import ui
from cogs.CONSTANTS import MyBot

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)
timezone = pytz.timezone("Europe/Paris")


class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Commandes classiques", emoji="🔧", description="Les commandes classiques  !"),
            discord.SelectOption(label="Commandes slash", emoji="🔨", description="Les commandes slash (nouveauté) !")
        ]
        super().__init__(placeholder="Veuillez choisir une catégorie de commandes", max_values=1, min_values=1,
                         options=options)

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
                                value="*__i!invite__* : Crée une invitation du serveur.\n *__i!avatar__* : Obtient l'avatar du membre.\n *__i!help__* : Affiche ce message.\n *__i!poll__* : Crée un sondage.\n *__i!ost__* : Génère une OST aléatoire.\n *__i!id__* : Prends l'ID de quelqu'un.\n *__i!warns__* : Vois tes avertissements.\n *__i!info__* : Informations sur i20",
                                inline=False)
            classhelp.add_field(
                name="__*Pour avoir plus de précision sur une commande, veuillez faire 'i!help nomDeLaCommande'.*__",
                value="Merci à Amaury pour l'aide qu'il a donnée pour la commande <3\n Vous pouvez aussi faire **i!help syntax** pour en apprendre plus sur la syntaxe utilisée dans l'explication des utilisations des commandes.\n---",
                inline=False)
            await interaction.response.edit_message(embed=classhelp)
        elif self.values[0] == "Commandes slash":
            slashhelp = discord.Embed(title="Les commandes slash d'i20 :",
                                      description="---\ni20 possède aussi une toute nouvelle fonctionnalité : les commandes slash. Les voici :",
                                      color=0x110b7a)
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
    def __init__(self, *, timeout=360):
        super().__init__(timeout=timeout)
        self.add_item(Select())


class AppCommands(Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
        tree = self.bot.tree
        self.joindate = app_commands.ContextMenu(name="Date d'arrivée sur le serveur", callback=self.show_join_date)
        self.quote = app_commands.ContextMenu(name="Quoter ce message", callback=self.quote_message)
        self.bot.tree.add_command(self.joindate)
        self.bot.tree.add_command(self.quote)


    @app_commands.command(name="sum", description="Additionne des nombres! (cog)")
    @app_commands.describe(premiernombre="Premier nombre.", deuxiemenombre="Deuxième nombre.",
                           show="Tu veux le montrer aux autres ou pas ?")
    async def slash(self, interaction: discord.Interaction, premiernombre: int, deuxiemenombre: int,
                    show: typing.Optional[bool] = False):
        await interaction.response.send_message(
            f'{premiernombre} + {deuxiemenombre} = {premiernombre + deuxiemenombre}', ephemeral=not show)

    @app_commands.command(name="embed", description="Crée un embed.")
    @app_commands.describe(titre="Le titre du embed.", descr="La description du embed.",
                           titrechamp1="Le titre du premier champ.", descrchamp1="La description du premier champ.",
                           titrechamp2="Le titre du deuxième champ.", descrchamp2="La description du deuxième champ.",
                           footer="Le footer à mettre.")
    async def embed(self, interaction: discord.Interaction, titre: str, descr: str, titrechamp1: typing.Optional[str],
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

    @app_commands.command(name="flip", description="Pile ou face ?")
    async def flip(self, interaction: discord.Interaction):
        coin = random.choice(["heads", "tails"])
        await interaction.response.send_message("Suspense...")
        await asyncio.sleep(3)
        if coin == "heads":
            await interaction.channel.send("Le pièce est tombée sur pile.")
            await interaction.channel.send("http://assets.stickpng.com/images/580b585b2edbce24c47b27c1.png")
        else:
            await interaction.channel.send("La pièce est tombée sur face.")
            await interaction.channel.send(
                "https://upload.wikimedia.org/wikipedia/fr/3/34/Piece-2-euros-commemorative-2012-france.png")

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

    @app_commands.command(name="info", description="Informations sur i20")
    async def superhelp(self, interaction: discord.Interaction):
        version = "2.2"
        description = "Bienvenue sur i20, un bot créé par PetitFrapo pour le serveur du monde d'Yvain, sur lequel vous êtes sûrement. Il implémente de nombreuses fonctionnalités de l'API discord.py, ainsi que ses dernières fonctionnalités, telles que les commandes slash. Effectuez la commande i!help afin de savoir quelles en sont les commandes. Vous pouvez aussi aller voir le salon <#858633105342857236> afin de vous renseigner sur certaines fonctionnalités qu'il comporte en réaction à certains messages."
        embed = discord.Embed(title=f"**__i20 v{version}__**",
                              description=description,
                              timestamp=interaction.created_at)
        embed.set_author(name="i20")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="button", description="Crée un petit bouton et fais le faire ce que tu veux !")
    @app_commands.describe(style="Choisis un style entre les différents choix !", label="Le texte marqué sur le bouton.", url="L'URL à laquelle il doit rediriger (optionnel).", emoji="Le NOM de l'emoji. Doit être un emoji de Discord.")
    async def create_button(self, interaction: discord.Interaction, style: str, label: str, url: Optional[str]=None, emoji: Optional[str]="", callback: Optional[str]=""):
        if style == "vert":
            style = "green"
        elif style == "rouge":
            style = "red"
        elif style == "gris":
            style = "grey"
        elif style in {"blurple", "url"}:
            pass
        else:
            await interaction.response.send_message("Le style rentré n'est pas correct !", ephemeral=True)
            return

        if emoji != "":
            try:
                emote = discord.PartialEmoji(name=emoji)
            except:
                await interaction.response.send_message("L'emoji donné est soit propre au serveur, soit inexistant.'", ephemeral=True)
                return

        async def mention(member):
            await member.send(f"{member.mention}")


        if url is not None:
            if emoji != "":
                userbutton = ui.Button(label=label, style=eval(f"discord.ButtonStyle.{style}"), url=url, emoji=emote)
            else:
                userbutton = ui.Button(label=label, style=eval(f"discord.ButtonStyle.{style}"), url=url)
        else:
            class MyButtonCallback(ui.Button):
                def __init__(self, label, style, callbackstr):
                    super().__init__(style=style, label=label)
                    self.callbackstr = callbackstr

                async def callback(self, interaction: discord.Interaction):
                    if self.callbackstr.startswith("mention("):
                        runtime = self.callbackstr.replace("mention(", "").replace(")", "")
                        if runtime == "me":
                            await interaction.channel.send(f"{interaction.user.mention}")
                    elif self.callbackstr.startswith("send("):
                        if "random(10)" in self.callbackstr:
                            a = str(random.randint(1, 10))
                            print(a)
                            self.newcallbackstr = self.callbackstr.replace("random(10)", a)
                        runtime = self.newcallbackstr.replace("send(", "").replace(")", "")
                        await interaction.channel.send(runtime)

            userbutton = MyButtonCallback(label=label, style=eval(f"discord.ButtonStyle.{style}"), callbackstr=callback)

        view = ui.View()
        view.add_item(userbutton)
        await interaction.response.send_message(view=view)

    @create_button.autocomplete("style")
    async def style_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        styles = ["blurple", "vert", "rouge", "url", "gris"]
        return [
            app_commands.Choice(name=style, value=style)
            for style in styles if current.lower() in style.lower()
        ]


    @app_commands.command(name="help", description="Menu d'aide")
    async def helpui(self, interaction: discord.Interaction, command: str = ""):
        com = command.lower()
        if com == "":
            embed = discord.Embed(title="Menu d'aide d'i20 :",
                                  description="Veuillez choisir une catégorie.",
                                  colour=0x110b7a)
            await interaction.response.send_message(embed=embed, view=SelectView())
        elif com == "avatar":
            embed = discord.Embed(title="Avatar :",
                                  description="*__i!avatar__* : Pour prendre l’avatar de quelqu’un ou le sien, mentionnez celui dont vous souhaitez la pp. Prend en charge les jpgs.\n\n L'utilisation est **i!avatar {user}**.",
                                  colour=0x110b7a)
        elif com == "randommsg":
            embed = discord.Embed(title="Random Message :",
                                  description="*__i!randommsg__* : Sentiments de nostalgie ? Pas de problème, cette commande cherche un message aléatoire dans le salon ! \n\n L'utilisation est **i!randommsg** tout simplement.",
                                  colour=0x110b7a)
        elif com == "warn":
            embed = discord.Embed(title="Warn :",
                                  description="*__i!warn__* : Quelqu'un a fait quelque chose de pas gentil et tu veux qu'il s'en souvienne ? Mets-lui un avertissement, tu verras, c'est rigolo ! Cette commande est utilisable seulement par les modérateurs. \n\n L'utilisation est **i!warn [member] {reason}**.",
                                  colour=0x110b7a)
        elif com == "id":
            embed = discord.Embed(title="ID :",
                                  description="*__i!id__* : Tu veux utiliser une commande comme **i!date** mais tu n'as pas envie de mentionner la personne car c'est un modérateur ? Et bien utilise cette commande, et remplace la mention de la personne par son identifiant. Tu verras ça marche ! \n\n L'utilisation est **i!id [memberName]**.",
                                  colour=0x110b7a)
        elif com == "ost":
            embed = discord.Embed(title="OST :",
                                  description="*__i!ost__* : Envie d'écouter une OST de jeux vidéos ? Parfait ! La commande vous en passe une super cool !\n\n L'utilisation est **i!ost** tout simplement.",
                                  colour=0x110b7a)
        elif com == "clear":
            embed = discord.Embed(title="Clear :",
                                  description="*__i!clear__* : Supprimez un certain nombre de messages dans le salon où la commande a été exécutée, insérez une valeur après pour renseigner le nombre de messages a supprimer. Cette commande est utilisable seulement par les modérateurs.\n\n L'utilisation est **i!clear {number}**.",
                                  colour=0x110b7a)
        elif com == "throw":
            embed = discord.Embed(title="Throw :",
                                  description="*__i!throw__* : Vous avez toujours rêvé de lançer des choses sur des gens ? Et bien cette commande est faite pour vous !\n\n L'utilisation est **i!throw [victime]**.",
                                  colour=0x110b7a)
        elif com == "ban":
            embed = discord.Embed(title="Ban :",
                                  description="*__i!ban__* : Quelqu’un de pas sage? B O N K bannissez le. Mentionnez le après la commande. Cette commande est utilisable seulement par les modérateurs.\n\n L'utilisation est **i!ban {member}**.",
                                  colour=0x110b7a)
        elif com == "code":
            embed = discord.Embed(title="Code :",
                                  description="*__i!code__* : i20 est un bot très intéressant, si vous souhaitez accéder à son code vous pouvez via cette commande.\n\n L'utilisation est **i!code** tout simplement.",
                                  colour=0x110b7a)
        elif com == "ship":
            embed = discord.Embed(title="Ship :",
                                  description="*__i!ship__* : On se sent un peu trop Cupidon ces temps-ci ? Pas de problème, i20 prend le relais et trouve les tourtereaux parfaits à votre place !\n\n L'utilisation est **i!ship {member1} {member2}** tout simplement.",
                                  colour=0x110b7a)
        elif com == "date":
            embed = discord.Embed(title="Date :",
                                  description="*__i!date__* : Vous vouliez l’heure ? Eh bien non, pourquoi ne pas passer le temps en faisant faire des rendez-vous entre les gens !\n\n L'utilisation est **i!date {user1} {user2}**.\n PS : Tu as trouvé le secret d'i20, essaie donc la commande **i!bonk** ! ",
                                  colour=0x110b7a)
        elif com == "flip":
            embed = discord.Embed(title="Flip :",
                                  description="*__i!flip__* : Âmes joueuses ? Embarquez dans un pile ou face avec du suspense !\n\n L'utilisation est **i!flip** tout simplement.",
                                  colour=0x110b7a)
        elif com == "embed":
            embed = discord.Embed(title="Embed :",
                                  description="*__i!embed__* : Vous avez envie de faire des textes ultra stylax ? Cette commande est faite pour vous!\n\n L'utilisation est **i!embed [title] [description] [couleur] {champ1} {desc_champ1} {champ2} {desc_champ2}**.\n PS : Les modérateurs peuvent rajouter 'hidename' **__à la fin__** de leur message afin de cacher leur identité.",
                                  colour=0x110b7a)
        elif com == "interesting":
            embed = discord.Embed(title="Interesting :",
                                  description="*__i!interesting__* : Vous trouvez que la discussion ou le dernier message est très intéressant ? Alors essayez cette commande !\n\n L'utilisation est **i!interesting** tout simplement.",
                                  colour=0x110b7a)
        elif com == "unban":
            embed = discord.Embed(title="Unban :",
                                  description="*__i!unban__* : Finalement il a été sage U N B O N K ! Débanissez le. Cette commande est utilisable seulement par les modérateurs.\n\n L'utilisation est **i!unban {user}**.",
                                  colour=0x110b7a)
        elif com == "ping":
            embed = discord.Embed(title="Ping :",
                                  description="*__i!ping__* : Vous pouvez ping quelqu’un en toute discrétion avec cette commande. Abusez pas S.V.P.\n\n L'utilisation est **i!ping {user}**.",
                                  colour=0x110b7a)
        elif com == "meme":
            embed = discord.Embed(title="Meme :",
                                  description="*__i!meme__* : Hahaha un meme au hasard ! Hésitez pas à proposer vos memes.\n\n L'utilisation est **i!meme** tout simplement.",
                                  colour=0x110b7a)
        elif com == "quote":
            embed = discord.Embed(title="Quote :",
                                  description="*__i!quote__* : Yvain et PetitFrapo les grands cultes vous proposent de nombreuses citations aussi inspirantes les unes que les autres. Découvrez les avec cette commande.\n\n L'utilisation est **i!quote** tout simplement.",
                                  colour=0x110b7a)
        elif com == "kick":
            embed = discord.Embed(title="Kick :",
                                  description="*__i!kick__* : GET THE FRICK OUT OF HERE, autrement dit faites le partir aussi vite qu'il est venu ! Cette commande est utilisable uniquement par les modérateurs.\n\n L'utilisation est **i!kick [member]**.",
                                  colour=0x110b7a)
        elif com == "pin":
            embed = discord.Embed(title="Pin :",
                                  description="*__i!pin__* : Vous avez envie d'épingler un message mais vous êtes sur mobile et, pfiou trop la flemme ? Cette commande est donc trop cool ! Cette commande est utilisable uniquement par les modérateurs.\n\n L'utilisation est **i!pin** tout simplement.",
                                  colour=0x110b7a)
        elif com == "warns":
            embed = discord.Embed(title="Warnings :",
                                  description="*__i!warns__* : Tu veux voir combien de fautes tu as commis sur le serveur ? Utilise la commande !\n\n L'utilisation est **i!warns {member}**.",
                                  colour=0x110b7a)
        elif com == "invite":
            embed = discord.Embed(title="Invite :",
                                  description="*__i!invite__* : Générez rapidement un lien d’invitation pour faire augmenter la populace !\n\n L'utilisation est **i!invite** tout simplement.",
                                  colour=0x110b7a)
        elif com == "poll":
            embed = discord.Embed(title="Poll :",
                                  description="*__i!poll__* : Êtes-vous le seul à vous poser cette question bête ? Faites-le savoir en entrant la commande. Le sondage sera envoyé dans le salon adéquat.\n\n L'utilisation est **i!poll [question] [réponse1] [réponse2] {réponse3} {réponse4}**.\n PS : Chaque question et réponse doit être entre guillemets.",
                                  colour=0x110b7a)
        elif com == "help":
            embed = discord.Embed(title="Help :",
                                  description="*__i!help__* : C'est pas bien dur, vous venez de le faire ! Cette commande affiche ce message !\n\n L'utilisation est **i!help {commande}**.\n PS : Vous pouvez aussi utiliser i!?.",
                                  colour=0x110b7a)
        elif com == "syntax":
            embed = discord.Embed(title="Syntaxe :",
                                  description="La syntaxe n'est pas bien dure à comprendre !\n **[argument]** : L'argument est obligatoire.\n **{argument}** : L'argument est optionnel.\n Et rien de plus ! Amusez-vous bien avec le bot !",
                                  colour=0x110b7a)
        elif com == "say":
            embed = discord.Embed(title="Say :",
                                  description="Faites dires des choses loufoques à i20. Il y a néanmoins un filtre de mot.\n PS : On aime pas la choucroute ni le haggis.\n\n L'utilisation est **i!say [textÀDire]**.",
                                  colour=0x110b7a)
        elif com == "removewarn":
            embed = discord.Embed(title="Remove Warn :",
                                  description="moooooh vous êtes trop sympa comme modo, excuse quelqu'un lui retirant son dernier warn !\n\n L'utilisation est **i!removewarn [membreÀExcuser]**.",
                                  colour=0x110b7a)

        # Slash
        elif com == "hexa":
            embed = discord.Embed(title="Hexa :",
                                  description="Transforme un nombre classique en hexadécimal (base 16).",
                                  colour=0x110b7a)
        elif com == "8ball":
            embed = discord.Embed(title="8Ball :",
                                  description="(NE MARCHE PAS TRÈS BIEN) Posez une question à i20. Il vous répondra (dans 50% des cas) une réponse avec une syntaxe correcte !",
                                  colour=0x110b7a)
        elif com == "sum":
            embed = discord.Embed(title="Sum :",
                                  description="Oui, on sait que t'as la flemme de le faire dans ta tête, alors laisse i20 additionner tes deux nombres.",
                                  colour=0x110b7a)
        elif com == "8ball":
            embed = discord.Embed(title="8Ball :",
                                  description="(NE MARCHE PAS TRÈS BIEN) Posez une question à i20. Il vous répondra (dans 50% des cas) une réponse avec une syntaxe correcte !",
                                  colour=0x110b7a)
        elif com == "shorten":
            embed = discord.Embed(title="Shorten :",
                                  description="Raccourcis une URL très facilement.",
                                  colour=0x110b7a)
        elif com == "info":
            embed = discord.Embed(title="Info :",
                                  description="Ça parait plutôt évident nan ?.",
                                  colour=0x110b7a)
        else:
            await interaction.response.send_message(f"La commande {com} n'existe pas !")
            return

        if com != "":
            await interaction.response.send_message(embed=embed)


    async def show_join_date(self, interaction: discord.Interaction, member: discord.Member):
        # The format_dt function formats the date time into a human readable representation in the official client
        await interaction.response.send_message(f'{member} a rejoint le {discord.utils.format_dt(member.joined_at)}')


    async def quote_message(self, interaction: discord.Interaction, message: discord.Message):
        modrole = discord.utils.get(interaction.guild.roles, id=845027528196227133)
        if modrole not in interaction.user.roles:
            await interaction.response.send_message("Seul un modérateur peut quote un message !")
            return
        # We're sending this response message with ephemeral=True, so only the command executor can see it
        await interaction.response.send_message(
            f'Le message a été quote ! Regarde le channel pour le voir !.', ephemeral=True
        )

        # Handle report by sending it into a log channel
        star_channel = interaction.guild.get_channel(980431170858811434)  # replace with your channel id

        embed = discord.Embed(title='Citation :', description=message.content, color=discord.Colour.random())

        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
        embed.timestamp = message.created_at

        url_view = discord.ui.View()
        url_view.add_item(
            discord.ui.Button(label='Aller au message', style=discord.ButtonStyle.url, url=message.jump_url))

        await star_channel.send(embed=embed, view=url_view)




async def setup(bot):
    await bot.add_cog(AppCommands(bot))
