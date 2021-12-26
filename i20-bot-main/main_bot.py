import os
import discord
import datetime
import time
import pytz
import random
from discord.ext import commands
from dotenv import load_dotenv
bot = commands.Bot(command_prefix=("i!", "I!"), help_command=None)
timezone = pytz.timezone("CET")
load_dotenv(dotenv_path="config")

@bot.event
async def on_ready():
    print("Le bot est prêt !")
    await bot.change_presence(activity=discord.Game(name="Je suis un bot créé par PetitFrapo !"))
    print("Le statut est prêt !")

#@bot.event
#async def on_message(message):
    #if message.content.lower() == "bonjour" or message.content.lower() == "salut":
        #await message.channel.send("Comment ça va?")

@bot.command(name="clear", description="Supprime un certain nombre de messages dans le salon. Cette commande est utilisable uniquement par les modérateurs.", help="Supprime des messages du salon.")
@commands.has_permissions(manage_messages=True)
async def delete(ctx, number_of_messages: int):
    messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()
    for each_message in messages:
        await each_message.delete()
    await ctx.channel.send("Les messages ont été supprimés !", delete_after=3)

@bot.command(name="interesting", description="Quand quelque chose est intéressant", help="Intéressant...")
async def on_message(message):
    await message.channel.send("Hmm, oui je vois, très intéressant...")

@bot.command(name="invite", help="Crée une invitation.", description="Crée une invitation pour le salon actuel.")
async def invite(ctx):
    invite = await ctx.channel.create_invite()
    await ctx.channel.send(f"Voici l'invitation : {invite} !")
    
@bot.command(name="ping", help="NOTIFICATION INTENSIFIES", description="Notifie la personne précisée.")
async def mention(message, user: discord.Member=""):
    if user == "":
        await message.channel.send(content=message.author.mention)
    else:
        await message.channel.send(content=user.mention)

@bot.command(name="kick", description="Pour kick les gens pas trétré genti", help="Kick les gens.")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: commands.MemberConverter):
    await ctx.guild.kick(member)
    await ctx.send(f"{member} a été kick du serveur ! Il fallait être plus sage !")

@bot.command(name="ban", description="B O N K le marteau", help="B O N K le marteau")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: commands.MemberConverter, *, reason=""):
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"{member} a été banni du serveur pour la raison : " + "'" + reason + "'" + " ! MOUAHAHA ! Mon marteau était fatigué...")

@bot.command(name="unban", description="uaetram el K N O B", help="Débannir les gens janti")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.name}#{user.discriminator} a été débanni ! Il était peut-être pas si méchant que ça...')
            return
       
@bot.command(name="quote", description="Les phrases drôles d'Yvain", help="Citation aléatoire.")
async def quote(message):
    quotes = ["Je cite : J'ai pas la mouna, par Shizuku, dans la vidéo Let's Play Minish Cap Randomizer #2.", "Je cite : TU ES MON CHEVAL, par PetitFrapo, en MP avec Shizuku.", "Je cite : Il faut que j'aille au mont Gounegueule, par Shizuku, dans la vidéo du Let's Play #1, #1.2 et #2.", "Je cite : MAIS C'EST SUPER TA VIE, par Shizuku à un pauvre petit commercant de la cité d'Hyrule, dans la vidéo du Let's Play Minish Cap Randomizer #2.", "Je cite : Ils ont l'Ultra-Instinct ! ILS ONT L'ULTRA INSTINCT !!, par Shizuku, dans le Jeudi de la souffrance sur Deathtroid.", "Je cite : spoiler : c'est pour que ce soit pas un spoiler., par PetitFrapo, sur le salon bac-à-sable.", "Je cite : En vrai c'est pas évident de faire un truc moche et de le rendre stylé ^^, par Shizuku/Yvain, sur le salon chat-modos (auquel vous n'avez pas accès niark niark)."] 
    await message.channel.send(random.choice(quotes))

@bot.command(name="say", description="Faites dire quelque chose à i20", aliases=["s"])
async def say(ctx, *, textToSay):
    commandMessage = await ctx.channel.history(limit=1).flatten()
    for eachMessage in commandMessage:
        await eachMessage.delete()
    swearWords = ["putain", "merde", "con", "connard", "fuck", "damn", "hell", "bordel", "pute", "shit"]
    swearFlag = None
    a = 0
    for i in swearWords:
        if i in str(textToSay).lower():
            swearFlag = True
            break
        else:
            swearFlag = False
    if swearFlag == True:
        await ctx.author.send("JAMAIS JE NE DIRAI CE GENRE DE CHOSES MAIS OÙ VA LE MONDE !")
    else:
        await ctx.channel.send(textToSay)

@bot.command(name="date", help="romance.", aliases=["love", "rdv"])
async def date(ctx, user: commands.MemberConverter="", user2: commands.MemberConverter=""):
    if user == "":
        await ctx.channel.send(f"{ctx.author.name} est en rendez-vous avec i20 !")
    elif user != "" and user2 == "":
        await ctx.channel.send(f"{user.display_name} est en date avec i20!")
    else:
        await ctx.channel.send(f"{user.display_name} est en date avec {user2.display_name} !")

@bot.command(name="poll", help="Crée un sondage.")
async def poll(ctx, question, option1, option2, option3="", option4=""):
    pollChannel: discord.TextChannel = bot.get_channel(922936202909319168)
    commandMessage = await ctx.channel.history(limit=1).flatten()
    threeOpt = None
    fourOpt = None
    for eachMessage in commandMessage:
        await eachMessage.delete()
    if option3 == "" and option4 == "":
        twoOpt = True
        embed = discord.Embed(title=question, description=f"1️⃣ : {option1}\n 2️⃣ : {option2}", timestamp=datetime.datetime.now(tz=timezone))
    elif option3 != "" and option4 == "":
        threeOpt = True
        embed = discord.Embed(title=question, description=f"1️⃣ : {option1}\n 2️⃣ : {option2}\n 3️⃣ : {option3}", timestamp=datetime.datetime.now(tz=timezone))
    elif option3 != "" and option4 != "":
        fourOpt = True
        embed = discord.Embed(title=question, description=f"1️⃣ : {option1}\n 2️⃣ : {option2}\n 3️⃣ : {option3}\n 4️⃣ : {option4}", timestamp=datetime.datetime.now(tz=timezone))
    emoji1 = "1️⃣"
    emoji2 = "2️⃣"
    emoji3 = "3️⃣"
    emoji4 = "4️⃣"
   
    message = await pollChannel.send(embed=embed)
    await message.add_reaction(emoji1)
    await message.add_reaction(emoji2)
    if threeOpt is True:
        await message.add_reaction(emoji3)
    elif fourOpt is True:
        await message.add_reaction(emoji3)
        await message.add_reaction(emoji4)
        
@bot.command(name="avatar", help="Prenez l'avatar de quelqu'un.", aliases=["pp", "pdp", "pfp"])
async def avatar(ctx, *, user: discord.Member=""):
    if user == "":
        userAvatar = ctx.author.avatar_url
        await ctx.channel.send(f"Voici l'avatar de {ctx.author.display_name}.")
        await ctx.channel.send(userAvatar)
    else:
        userAvatar = user.avatar_url
        await ctx.channel.send(f"Voici l'avatar de {user.display_name}.")
        await ctx.channel.send(userAvatar)
        
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
        await ctx.channel.send("https://upload.wikimedia.org/wikipedia/fr/3/34/Piece-2-euros-commemorative-2012-france.png")

@bot.command(name="bonk")
async def bonk(ctx):
    await ctx.send("B O N K")
    await ctx.send("https://media.discordapp.net/attachments/858632881139875840/924339843771809802/IMG_3748.jpg")
    
        
@bot.command(name="help", aliases=["?"])
async def helptest(ctx, command=""):
    com = command.lower()
    if com == "":
        embed = discord.Embed(title="Les commandes d'i20 :",
                              color=0x110b7a,
                              description="---\ni20 est un bot possédant plein de commandes, les voici :")
        embed.add_field(name="Fun :",
                        value="*__i!interesting__* : Intéressant...\n *__i!flip__* : Pile ou face ?\n *__i!meme__* : Génère un meme aléatoire.\n *__i!date__* : romance.\n *__i!ping__* : NOTIFICATION INTENSIFIES\n *__i!say__* : Faites dire quelque chose à i20 ! Ne dites pas de gros mots ou gare à vous !\n *__i!quote__* : Les citations cultes d'Yvain et PetitFrapo !",
                        inline=False)

        embed.add_field(name="Modération :",
                        value="*__i!ban__* : B O N K le marteau\n *__i!unban__* : uaetram el K N O B\n *__i!kick__* : Pour kick les gens pas trétré genti\n *__i!clear__* : Supprime des messages du salon.",
                        inline=False)
        embed.add_field(name="Utile :",
                        value="*__i!invite__* : Crée une invitation du serveur.\n *__i!avatar__* : Obtient l'avatar du membre.\n *__i!help__* : Affiche ce message.\n *__i!poll__* : Crée un sondage.",
                        inline=False)
        embed.add_field(name="__*Pour avoir plus de précision sur une commande, veuillez faire 'i!help nomDeLaCommande.*__", value="---", inline=False)
    elif com == "avatar":
        embed = discord.Embed(name="Avatar :", description="*__i!avatar__* : Pour prendre l’avatar de quelqu’un ou le sien, mentionnez celui dont vous souhaitez la pp. Prend en charge les jpgs.\n\n L'utilisation est **i!avatar {user}**.", colour=0x110b7a)
    elif com == "clear":
        embed = discord.Embed(name="Clear :", description="*__i!clear__* : Supprimez un certain nombre de messages dans le salon où la commande a été exécutée, insérez une valeur après pour renseigner le nombre de messages a supprimer. Cette commande est utilisable seulement par les modérateurs.\n\n L'utilisation est **i!clear {number}**.", colour=0x110b7a)
    elif com == "ban":
        embed = discord.Embed(name="Ban :", description="*__i!ban__* : Quelqu’un de pas sage? B O N K bannissez le. Mentionnez le après la commande. Cette commande est utilisable seulement par les modérateurs.\n\n L'utilisation est **i!ban {member}**.", colour=0x110b7a)
    elif com == "code":
        embed = discord.Embed(name="Code :", description="*__i!code__* : i20 est un bot très intéressant, si vous souhaitez accéder à son code vous pouvez via cette commande.\n\n L'utilisation est **i!code** tout simplement.", colour=0x110b7a)
    elif com == "date":
        embed = discord.Embed(name="Date :", description="*__i!date__* : Vous vouliez l’heure ? Eh bien non, pourquoi ne pas passer le temps en faisant faire des rendez-vous entre les gens !\n\n L'utilisation est **i!date {user1} {user2}**.\n PS : Tu as trouvé le secret d'i20, essaie donc la commande **i!bonk** ! ", colour=0x110b7a)
    elif com == "flip":
        embed = discord.Embed(name="Flip :", description="*__i!flip__* : Âmes joueuses ? Embarquez dans un pile ou face avec du suspense !\n\n L'utilisation est **i!flip** tout simplement.", colour=0x110b7a)
    elif com == "interesting":
        embed = discord.Embed(name="Interesting :", description="*__i!interesting__* : Vous trouvez que la discussion ou le dernier message est très intéressant ? Alors essayez cette commande !\n\n L'utilisation est **i!interesting** tout simplement.", colour=0x110b7a)

    await ctx.send(embed=embed)
        
bot.run(os.getenv("TOKEN"))
