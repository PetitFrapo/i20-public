# Cette partie du code représente toutes les commandes de la catégorie Fun.

import asyncio
import typing
import random
import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from discord import ui
from cogs.cogutils import MyBot

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None,
            intents=default_intents, application_id=853301761572732928)


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="throw")
    async def throw(self, ctx: Context, victim: discord.Member):
        throwmaterials = ["de la crasse", "Amaury", "un fichier PNG", "du pain", "un ballon de basket",
                          "un truc non identifié", "un 12/20 en maths", "des crêpes", "une Pokéball", 'la Master Sword',
                          "une pièce SOS", "un être d'Yvain", "mon code source", "une crêpe", "un train",
                          "José", "une baguette de pain", "une lance", "son bras", "un ordinateur",
                          "Yoshikage Kira", "un chat (le pauvre)", "Yare", "une jambe trouvée par terre (wait)",
                          "Olivier de chez Carglass", "... mais qu'est-ce que c'est que ça..."]
        throwmaterial = random.choice(throwmaterials)
        await ctx.send(
            f"{ctx.author.display_name} a lancé {throwmaterial} sur {victim.display_name} ! Il est tout sali "
            f"maintenant...")
        if victim.display_name == "i20":
            await ctx.send("Aïe ! Qui m'a lancé ça ?")
        if throwmaterial == throwmaterials[8]:
            await ctx.send("...")
            await asyncio.sleep(3)
            caught = random.choice([0, 1, 2, 3, 4])
            if caught == 3:
                await ctx.send(f'{ctx.author.display_name} a capturé {victim.display_name} !')
            else:
                await ctx.send(f"{victim.display_name} s'est enfui !")

    @commands.command(name="ship")
    async def ship(self, ctx, member1: discord.Member = "", member2: discord.Member = ""):
        easteregg = random.randrange(0, 49)
        if easteregg == 45:
            await ctx.send(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Lorient-navire-oceanographi.jpg/1200px"
                "-Lorient-navire-oceanographi.jpg")
        else:
            if member1 == "" and member2 == "":
                users = ctx.guild.members
                user1, user2 = random.sample(users, 2)
            else:
                user1 = member1
                user2 = member2
            fpart1 = user1.display_name[:len(user1.display_name) // 2]
            fpart2 = user2.display_name[len(user2.display_name) // 2:]
            spart1 = user1.display_name[len(user1.display_name) // 2:]
            spart2 = user2.display_name[:len(user2.display_name) // 2]

            fbabyname = fpart1 + fpart2
            sbabyname = spart2 + spart1

            class Button(ui.Button):
                def __init__(self, label, style):
                    super().__init__(style=style, label=label)

                async def callback(self, interaction: discord.Interaction):

                    content = f"Mouais bof bof, une autre idée : {sbabyname}"\
                        if interaction.message.content in {f"{user1.display_name} et {user2.display_name} ont eu un "
                                                           f"enfant ! Il s'appellera {fbabyname} !",
                                                           f"Ouais nan {fbabyname} sonnait mieux..."}\
                        else f"Ouais nan {fbabyname} sonnait mieux... "

                    await interaction.response.edit_message(content=content)

            button = Button(label="Peut-être que...", style=discord.ButtonStyle.primary)
            view = ui.View().add_item(button)
            await ctx.send(
                f"{user1.display_name} et {user2.display_name} ont eu un enfant ! Il s'appellera {fbabyname} !",
                view=view
            )
            if user1.display_name == "i20" or user2.display_name == "i20":
                await ctx.send(f"uwu viens dans mes bras {fbabyname}~~~")

    @commands.command(name="id")
    async def id(self, ctx, *, target: commands.MemberConverter):
        targetid = target.id
        await ctx.send(f"L'ID de {target.display_name} est {targetid}.")

    @id.error
    async def id_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Le membre n'existe pas !")

    @commands.command(name="bonk")
    async def bonk(self, ctx: Context):
        await ctx.send("B O N K")
        await ctx.send("https://media.discordapp.net/attachments/858632881139875840/924339843771809802/IMG_3748.jpg")

    @commands.hybrid_command(name="flip", description="Pile ou face ?")
    async def flip(self, ctx: Context):
        coin = random.choice(["heads", "tails"])
        await ctx.channel.send("Suspense...")
        await asyncio.sleep(3)
        if coin == "heads":
            await ctx.channel.send("Le pièce est tombée sur pile.")
            await ctx.channel.send("http://assets.stickpng.com/images/580b585b2edbce24c47b27c1.png")
        else:
            await ctx.channel.send("La pièce est tombée sur face.")
            await ctx.channel.send(
                "https://upload.wikimedia.org/wikipedia/fr/3/34/Piece-2-euros-commemorative-2012-france.png")

    @commands.command(name="date")
    async def date(self, ctx: Context, user: commands.MemberConverter = "", user2: commands.MemberConverter = ""):
        if user == "":
            await ctx.send(f"{ctx.author.name} est en rendez-vous avec i20 !")
        elif user != "" and user2 == "":
            await ctx.send(f"{user.display_name} est en date avec i20!")
        else:
            await ctx.send(f"{user.display_name} est en date avec {user2.display_name} !")

    @commands.command(name="quote")
    async def quote(self, ctx: Context):
        class MyButt(ui.Button):
            def __init__(self, label, style):
                self.quotes = [
                    "Je cite : J'ai pas la mouna, par Yvain, dans la vidéo Let's Play Minish Cap Randomizer #2.",
                    "Je cite : TU ES MON CHEVAL, par PetitFrapo, en MP avec Yvain.",
                    "Je cite : Il faut que j'aille au mont Gounegueule, par Yvain, dans la vidéo du Let's Play #1, "
                    "#1.2 et #2.",
                    "Je cite : MAIS C'EST SUPER TA VIE, par Yvain à un pauvre petit commercant de la cité d'Hyrule, "
                    "dans la vidéo du Let's Play Minish Cap Randomizer #2.",
                    "Je cite : Ils ont l'Ultra-Instinct ! ILS ONT L'ULTRA INSTINCT !!, par Yvain, dans le Jeudi de la "
                    "souffrance sur Deathtroid.",
                    "Je cite : spoiler : c'est pour que ce soit pas un spoiler., par PetitFrapo, sur le salon "
                    "bac-à-sable.",
                    "Je cite : En vrai c'est pas évident de faire un truc moche et de le rendre stylé ^^, par Yvain, "
                    "sur le salon chat-modos (auquel vous n'avez pas accès niark niark)."]
                super().__init__(label=label, style=style)

            async def callback(self, interaction: discord.Interaction) -> typing.Any:
                await interaction.response.edit_message(content=random.choice(self.quotes))

        button = MyButt(label="Une autre !", style=discord.ButtonStyle.blurple)
        view = ui.View()
        view.add_item(button)
        await ctx.send(random.choice(button.quotes), view=view)


# On ajoute le cog au bot.
async def setup(bot):
    await bot.add_cog(Fun(bot))
