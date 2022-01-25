import os
import discord
import random
from dotenv import load_dotenv
default_intents = discord.Intents.default()
default_intents.members = True

load_dotenv(dotenv_path="config")

client = discord.Client(intents=default_intents)

@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_message(message):
    if message.content.lower() == "ping":
        await message.channel.send("pong")
    if message.content.lower() == "bonjour" or message.content.lower() == "salut" or message.content.lower() == "tulas":
        answers = ["Comment ça va?", "Ca roule?", "Yo !", "Je suis heureux d'être un bot ! Ah, salut toi...", "Salut à toi, connais-tu le théorème de PetitFrapo ? Bah, ça existe pas, cet homme est tellement débile après tout...", "! tulaS", "Je suis le double maléfique du grand Yvain !", "J'ai terminé le any% de BOTW en 11 minutes ! Qui dit mieux ? Personne ? Bien ce que je me disais...", "la vi c pa un ki wi", "J'aime le pain. Miam. Oh. Un humain. Je. Dois. L'anéantir.", "Je m'appelle i20 ! Faisons connaissance !", "Pst, toi là, abonne-toi à la chaîne de PetitFrapo et peut-être que je pourrai te rajouter une réponse perso...", "Yo l'humain", "La légende dit qu'un être nommé Brisingr existe. Si tu arrives à écrire son nom sans faute du premier coup, eh bien tu aura ma gratitude !", "Prenez garde ! Le bot i20 peut vous warn ! (quand ce flemmard de petitfrapo l'aura codé)", "Oro ?", "Savez-vous que le temps se dilate lorsque vous discutez avec moi ?", "Salut " + str(message.author.mention) + " !", "Ma magnifique photo de profil a été créée par cc_hunter_boy !", "Burger est un noob il a perdu d'un point !"]
        await message.channel.send(random.choice(answers))
    if message.content.lower() == "delete this" or message.content.lower() == "supprime ça" or message.content.lower() == "make that disappear" or message.content.lower() == "supprime ca" or message.content.lower() == "ce message doit disparaître" or message.content.lower() == "ce message doit disparaitre":
        messages = await message.channel.history(limit=1).flatten()
        for each_message in messages:
            await each_message.delete()
    if message.content.lower() == "react here":
        emoji = "👀"
        await message.add_reaction(emoji)
    if message.content.startswith("après tout") or message.content.startswith("et vois-tu") or message.content.startswith("Après tout") or message.content.startswith("Et vois-tu"):
        chances = random.randrange(1, 7)
        if chances == 4:
            await message.channel.send("Ouais je vois...")
    if message.content.lower() == "i20 ?":
        await message.channel.send("Oui madame ? Oups pardon je me croyais à l'école des bots... Que disais-tu ?")
    if message.content.lower() == "amogus":
        amogusMsg = ["sus", "ඞ", "sussy baka", "!!!!!", "never say kid amogus backwards", "dont look up the scientific name for pig", "ye amogus boi", "sussy impasta amog us!!!!1!"]
        await message.channel.send(random.choice(amogusMsg))
        emojiS = "🇸"
        await message.add_reaction(emojiS)
        emojiU = "🇺"
        await message.add_reaction(emojiU)
        emojiDollar = "💲"
        await message.add_reaction(emojiDollar)
    if message.content.lower() == "moyai":
        await message.channel.send("🗿")
    if message.content.lower() == "ted":
        emojiTED = "<:Ted:905070467143073842>"
        await message.add_reaction(emojiTED)
        await message.channel.send(emojiTED)
    if message.content.lower() == "dm moi le mot tomate":
        await message.author.send(str(message.author.mention) + " tomate")
    if "manger" in message.content.lower() or "mangé" in message.content.lower():
        await message.channel.send(f"Bon appétit {message.author.display_name} ! ")
    if "feur" in message.content.lower() or "stiti" in message.content.lower() or "bril" in message.content.lower():
        if not message.author.bot:
            if not message.content.startswith("i!say"):
                await message.channel.send(f"Ton humour est vraiment pourri {message.author.mention}...")
        else:
            await message.channel.send("Nan mais M. D. R. Ça veut me faire dire que j'ai un humour de merde... Dépitant...")
        
    
    
        
        
@client.event
async def on_member_join(member):
    welcome_channel: discord.TextChannel = client.get_channel(845178082042314763)
    await welcome_channel.send(content=f"Bienvenue sur le serveur {member.mention} !")

@client.event
async def on_member_remove(member):
    goodbye_channel: discord.TextChannel = client.get_channel(845186181255790603)
    await goodbye_channel.send(content=f"{member.display_name} vient de quitter le serveur ! On espère qu'il/elle reviendra vite !")

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 853625500319875095:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'linksmug':
            role = discord.utils.get(guild.roles, name="Hylien")
        elif payload.emoji.name == "zelda_hmm":
            role = discord.utils.get(guild.roles, name="Hylienne")

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print("done")
            else:
                print("Member not found.")
        else:
            print("Role not found.")

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 853625500319875095:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'linksmug':
            role = discord.utils.get(guild.roles, name="Hylien")
        elif payload.emoji.name == "zelda_hmm":
            role = discord.utils.get(guild.roles, name="Hylienne")

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print("done")
            else:
                print("Member not found.")
        else:
            print("Role not found.")


client.run(os.getenv("TOKEN"))

