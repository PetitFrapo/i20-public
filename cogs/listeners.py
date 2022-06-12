# Cette partie du code représente ce qu'était avant main.py,
# donc les réactions aux messages ou les reaction roles.

import discord
import random
from discord.ext.commands import Cog
from cogs.cogutils import MyBot
from dotenv import load_dotenv

default_intents = discord.Intents.default()
default_intents.members = True
default_intents.message_content = True

load_dotenv(dotenv_path="config")

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents,
            application_id=853301761572732928)


class Listeners(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener("on_message")
    async def on_msg(self, message):
        if message.content.lower() == "ping":
            await message.channel.send("pong")
        if message.content.lower() == "bonjour" or message.content.lower() == "salut":
            answers = ["Comment ça va?", "Ca roule?", "Yo !", "Je suis heureux d'être un bot ! Ah, salut toi...",
                       "Salut à toi, connais-tu le théorème de PetitFrapo ? Bah, ça existe pas, cet homme est tellement débile après tout...",
                       "! tulaS", "Je suis le double maléfique du grand Yvain !",
                       "J'ai terminé le any% de BOTW en 11 minutes ! Qui dit mieux ? Personne ? Bien ce que je me disais...",
                       "la vi c pa un ki wi", "J'aime le pain. Miam. Oh. Un humain. Je. Dois. L'anéantir.",
                       "Je m'appelle i20 ! Faisons connaissance !",
                       "Pst, toi là, abonne-toi à la chaîne de PetitFrapo et peut-être que je pourrai te rajouter une réponse perso...",
                       "Yo l'humain", "Prenez garde ! Le bot i20 peut vous warn !", "Oro ?",
                       "Savez-vous que le temps se dilate lorsque vous discutez avec moi ?",
                       f"Salut {message.author.mention} !",
                       "Ma magnifique photo de profil a été créée par cc_hunter_boy !",
                       "Burger est un noob il a perdu d'un point !",
                       "Je suis actuellement en version 2.1 ! Bip ! Boup !",
                       "La vie de bot est parfaite ! En plus, je suis tout le temps amélioré !",
                       "Venez dire coucou à mon ami <@951112807187894322>, il a été créé par Amaury (par PetitFrapo à 80% mais les idées proviennent d'Amaury).",
                       "Être un bot est la meilleure chose.", "Tu veux discuter avec moi ?",
                       "Je suis très sensible à l'hypnose, fais i!say pour me faire dire certaines choses !"]
            await message.channel.send(random.choice(answers))
        if message.content.lower() == "react here":
            emoji = "👀"
            await message.add_reaction(emoji)
        elif message.content.lower() == "ratio":
            emoji = "⬆️"
            await message.add_reaction(emoji)
        if message.content.startswith("après tout") or message.content.startswith("et vois-tu"):
            chances = random.randrange(1, 8)
            print(chances)
            if chances == 7:
                await message.channel.send("Ouais je vois...")
        if message.content.lower() == "i20 ?":
            await message.channel.send("Oui madame ? Oups pardon je me croyais à l'école des bots... Que disais-tu ?")
        if message.content.lower().startswith("yilmfg"):
            await message.channel.send("t'as un problème toi")
        if message.content.lower() == "👃":
            await message.channel.send(random.choice(
                ["<:Ted:905070467143073842>", "<:PPted:921830504033054760>", "<:Ted:905070467143073842>",
                 "<:Ted:905070467143073842>"]))
        elif message.content.startswith("feur") or message.content.startswith("stiti") or message.content.startswith("bril"):
            await message.channel.send("Ton humour et bah il pue")

    @Cog.listener("on_member_join")
    async def memberjoin(self, member):
        if member.guild.id == 845026449495818240:
            welcome_channel: discord.TextChannel = self.bot.get_channel(845178082042314763)
            await welcome_channel.send(content=f"Bienvenue sur le serveur {member.mention} !")
            memberrole = discord.utils.get(member.guild.roles, id=845177866374742076)
            await member.add_roles(memberrole)

    @Cog.listener("on_member_remove")
    async def memberremove(self, member):
        goodbye_channel: discord.TextChannel = self.bot.get_channel(845186181255790603)
        await goodbye_channel.send(
            content=f"{member.display_name} vient de quitter le serveur ! On espère qu'il reviendra vite !")

    # Reaction Roles (add)
    @Cog.listener("on_raw_reaction_add")
    async def reaction_role_add(self, payload):
        message_id = payload.message_id

        # SPEEDRUNNER
        if message_id == 853687348302053426:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

            if payload.emoji.name == 'speedrocket':
                role = discord.utils.get(guild.roles, name="Speedrunner")

            if role is not None:
                member = payload.member
                if member is not None:
                    await member.add_roles(role)
                    await member.send("Le rôle **Speedrunner** t'a été ajouté !")

        # PING YOUTUBE / EVENT
        elif message_id == 935837917123842138:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

            if payload.emoji.name == 'SAnic':
                role = discord.utils.get(guild.roles, name="Ping YouTube")
            elif payload.emoji.name == "metasanic":
                role = discord.utils.get(guild.roles, name="Ping Event")

            if role is not None:
                member = payload.member
                if member is not None:
                    await member.add_roles(role)
                    await member.send(f"Le rôle **{role.name}** t\'a été ajouté !")

        # YVAINIEN / YVAINIENNE / D'YVAIN
        elif message_id == 977471941134925905:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

            if payload.emoji.name == 'Ted':
                role = discord.utils.get(guild.roles, name="Yvainien")
            elif payload.emoji.name == "tedette":
                role = discord.utils.get(guild.roles, name="Yvainienne")
            elif payload.emoji.name == "PPted":
                role = discord.utils.get(guild.roles, name="D'Yvain")

            if role is not None:
                member = payload.member
                if member is not None:
                    await member.add_roles(role)
                    await member.send(f"Le rôle **{role.name}** t\'a été ajouté !")

    # Speedrunner Reaction Roles (remove)
    @Cog.listener("on_raw_reaction_remove")
    async def reaction_roles_remove(self, payload):
        message_id = payload.message_id

        # SPEEDRUNNER
        if message_id == 853687348302053426:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

            if payload.emoji.name == 'speedrocket':
                role = discord.utils.get(guild.roles, name="Speedrunner")

            if role is not None:
                member = guild.get_member(payload.user_id)

                if member is not None:
                    await member.remove_roles(role)
                    await member.send("Le rôle **Speedrunner** t'a été retiré !")

        # PING YOUTUBE / EVENT
        elif message_id == 935837917123842138:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

            if payload.emoji.name == 'SAnic':
                role = discord.utils.get(guild.roles, name="Ping YouTube")
            elif payload.emoji.name == "metasanic":
                role = discord.utils.get(guild.roles, name="Ping Event")

            if role is not None:
                member = guild.get_member(payload.user_id)
                if member is not None:
                    await member.remove_roles(role)
                    await member.send(f"Le rôle **{role.name}** t\'a été retiré !")

        # YVAINIEN / YVAINIEN / D'YVAIN (NB)
        elif message_id == 977471941134925905:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

            if payload.emoji.name == 'Ted':
                role = discord.utils.get(guild.roles, name="Yvainien")
            elif payload.emoji.name == "tedette":
                role = discord.utils.get(guild.roles, name="Yvainienne")
            elif payload.emoji.name == "PPted":
                role = discord.utils.get(guild.roles, name="D'Yvain")

            if role is not None:
                member = guild.get_member(payload.user_id)
                if member is not None:
                    await member.remove_roles(role)
                    await member.send(f"Le rôle **{role.name}** t\'a été retiré !")


# On ajoute le cog au bot.
async def setup(bot):
    await bot.add_cog(Listeners(bot))
