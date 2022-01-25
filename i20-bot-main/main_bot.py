import os
import discord
import datetime
import time
import pytz
import random
import asyncio
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv

default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix=("i!", "I!"), help_command=None, intents=default_intents)
timezone = pytz.timezone("CET")
load_dotenv(dotenv_path="config")



@bot.event
async def on_ready():
    print("Le bot est prêt !")
    #await bot.change_presence(activity=discord.Game(name="Je suis un bot créé par PetitFrapo !"))
    print("Le statut est prêt !")


async def presence():
    await bot.wait_until_ready()
    while not bot.is_closed():
        presences = ["Respectez moi sinon grr", "Je suis un bot créé par PetitFrapo !", "la vi c pa un kiwi", "mon magnifique code.", "BOTW 2."]
        game = random.choice(presences)
        if game != presences[3]:
            await bot.change_presence(activity=discord.Game(name=game))
        else:
            await bot.change_presence(activity=discord.Activity(name=game, type=discord.ActivityType.watching) )
        await asyncio.sleep(5)





# @bot.event
# async def on_message(message):
# if message.content.lower() == "bonjour" or message.content.lower() == "salut":
# await message.channel.send("Comment ça va?")

@bot.command(name="clear",
             description="Supprime un certain nombre de messages dans le salon. Cette commande est utilisable uniquement par les modérateurs.",
             help="Supprime des messages du salon.")
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
async def mention(message, user: discord.Member = ""):
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
    await ctx.send(
        f"{member} a été banni du serveur pour la raison : " + "'" + reason + "'" + " ! MOUAHAHA ! Mon marteau était fatigué...")


@bot.command(name="unban", description="uaetram el K N O B", help="Débannir les gens janti")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(
                f'{user.name}#{user.discriminator} a été débanni ! Il était peut-être pas si méchant que ça...')
            return

@bot.command(name="code")
async def code(ctx):
    await ctx.send("Voici le code d'i20 : https://www.github.com/PetitFrapo/i20-public/ !")       
        
        
        
@bot.command(name="quote", description="Les phrases drôles d'Yvain", help="Citation aléatoire.")
async def quote(message):
    quotes = ["Je cite : J'ai pas la mouna, par Yvain, dans la vidéo Let's Play Minish Cap Randomizer #2.",
              "Je cite : TU ES MON CHEVAL, par PetitFrapo, en MP avec Yvain.",
              "Je cite : Il faut que j'aille au mont Gounegueule, par Yvain, dans la vidéo du Let's Play #1, #1.2 et #2.",
              "Je cite : MAIS C'EST SUPER TA VIE, par Yvain à un pauvre petit commercant de la cité d'Hyrule, dans la vidéo du Let's Play Minish Cap Randomizer #2.",
              "Je cite : Ils ont l'Ultra-Instinct ! ILS ONT L'ULTRA INSTINCT !!, par Yvain, dans le Jeudi de la souffrance sur Deathtroid.",
              "Je cite : spoiler : c'est pour que ce soit pas un spoiler., par PetitFrapo, sur le salon bac-à-sable.",
              "Je cite : En vrai c'est pas évident de faire un truc moche et de le rendre stylé ^^, par Yvain, sur le salon chat-modos (auquel vous n'avez pas accès niark niark)."]
    await message.channel.send(random.choice(quotes))


@bot.command(name="say", description="Faites dire quelque chose à i20", aliases=["s"])
async def say(ctx, *, textToSay):
    await ctx.message.delete()
    swearWords = ["putain", "merde", "con", "connard", "fuck", "damn", "hell", "bordel", "pute", "shit", "everyone"]
    swearFlag = None
    a = 0
    for i in swearWords:
        if i in str(textToSay).lower():
            swearFlag = True
            break
        else:
            swearFlag = False
    if swearFlag == True:
        try:
            await ctx.author.send("JAMAIS JE NE DIRAI CE GENRE DE CHOSES MAIS OÙ VA LE MONDE !")
        except:
            await ctx.channel.send("JAMAIS JE NE DIRAI CE GENRE DE CHOSES MAIS OÙ VA LE MONDE !", delete_after=5)
    else:
        sayResult = await ctx.channel.send(textToSay)
        log = f"Log de i!say : {ctx.author.display_name} a utilisé i20 pour envoyer {textToSay}. MESSAGE_ID = {sayResult.id}"
        with open("saylogs.txt", "a") as l:
            l.write(log)
            l.write("\n")




@bot.command(name="date", help="romance.", aliases=["love", "rdv"])
async def date(ctx, user: commands.MemberConverter = "", user2: commands.MemberConverter = ""):
    if user == "":
        await ctx.channel.send(f"{ctx.author.name} est en rendez-vous avec i20 !")
    elif user != "" and user2 == "":
        await ctx.channel.send(f"{user.display_name} est en date avec i20!")
    else:
        await ctx.channel.send(f"{user.display_name} est en date avec {user2.display_name} !")


@bot.command(name="poll", help="Crée un sondage.")
async def poll(ctx, question, option1, option2, option3="", option4="", mention_everyone=""):
    pollChannel: discord.TextChannel = bot.get_channel(922936202909319168)
    commandMessage = await ctx.channel.history(limit=1).flatten()
    threeOpt = None
    fourOpt = None
    for eachMessage in commandMessage:
        await eachMessage.delete()
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

    role = discord.utils.get(ctx.guild.roles, id=922944521384374312)
    if role in ctx.author.roles:
        await ctx.author.send(
            "Désolé, tu es banni de la commande i!poll... Tu as sûrement joué avec ou spam les sondages...")
    else:
        message = await pollChannel.send(embed=embed)
        await message.add_reaction(emoji1)
        await message.add_reaction(emoji2)
        if threeOpt is True:
            await message.add_reaction(emoji3)
        elif fourOpt is True:
            await message.add_reaction(emoji3)
            await message.add_reaction(emoji4)

    if mention_everyone != "":
        modrole = discord.utils.get(ctx.guild.roles, id=845027528196227133)
        if modrole in ctx.author.roles:
            if mention_everyone.lower() == "true":
                await pollChannel.send("@everyone")
        else:
            await ctx.author.send("T'as trop cru tu pouvais mentionner everyone mdrrr")


@bot.command(name="avatar", help="Prenez l'avatar de quelqu'un.", aliases=["pp", "pdp", "pfp"])
async def avatar(ctx, *, user: discord.Member = ""):
    if user == "":
        userAvatar = ctx.author.avatar_url
        await ctx.channel.send(f"Voici l'avatar de {ctx.author.display_name}.")
        await ctx.channel.send(userAvatar)
    else:
        userAvatar = user.avatar_url
        await ctx.channel.send(f"Voici l'avatar de {user.display_name}.")
        await ctx.channel.send(userAvatar)


@bot.command(name="meme")
async def meme(ctx):
    f = open("memes.txt", "r")
    meme = random.choice(f.readlines())
    await ctx.channel.send(meme)


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


@bot.command(name="help", aliases=["?"])
async def helptest(ctx, command=""):
    com = command.lower()
    if com == "":
        embed = discord.Embed(title="Les commandes d'i20 :",
                              color=0x110b7a,
                              description="---\ni20 est un bot possédant plein de commandes, les voici :")
        embed.add_field(name="Fun :",
                        value="*__i!interesting__* : Intéressant...\n *__i!flip__* : Pile ou face ?\n *__i!meme__* : Génère un meme aléatoire.\n *__i!date__* : romance.\n *__i!ping__* : NOTIFICATION INTENSIFIES\n *__i!say__* : Faites dire quelque chose à i20 ! Ne dites pas de gros mots ou gare à vous !\n *__i!quote__* : Les citations cultes d'Yvain et PetitFrapo !\n *__i!embed__* : Crée un embed (càd un texte stylé et encadré et tout!).\n *__i!throw__* : Lance quelque chose sur quelqu'un.\n *__i!ship__* : uwu~",
                        inline=False)

        embed.add_field(name="Modération :",
                        value="*__i!ban__* : B O N K le marteau\n *__i!unban__* : uaetram el K N O B\n *__i!kick__* : Pour kick les gens pas trétré genti\n *__i!clear__* : Supprime des messages du salon.",
                        inline=False)
        embed.add_field(name="Utile :",
                        value="*__i!invite__* : Crée une invitation du serveur.\n *__i!avatar__* : Obtient l'avatar du membre.\n *__i!help__* : Affiche ce message.\n *__i!poll__* : Crée un sondage.",
                        inline=False)
        embed.add_field(
            name="__*Pour avoir plus de précision sur une commande, veuillez faire 'i!help nomDeLaCommande'.*__",
            value="Merci à Amaury pour l'aide qu'il a donnée pour la commande <3\n Vous pouvez aussi faire **i!help syntax** pour en apprendre plus sur la syntaxe utilisée dans l'explication des utilisations des commandes.\n---",
            inline=False)
    elif com == "avatar":
        embed = discord.Embed(name="Avatar :",
                              description="*__i!avatar__* : Pour prendre l’avatar de quelqu’un ou le sien, mentionnez celui dont vous souhaitez la pp. Prend en charge les jpgs.\n\n L'utilisation est **i!avatar {user}**.",
                              colour=0x110b7a)
    elif com == "clear":
        embed = discord.Embed(name="Clear :",
                              description="*__i!clear__* : Supprimez un certain nombre de messages dans le salon où la commande a été exécutée, insérez une valeur après pour renseigner le nombre de messages a supprimer. Cette commande est utilisable seulement par les modérateurs.\n\n L'utilisation est **i!clear {number}**.",
                              colour=0x110b7a)
    elif com == "throw":
        embed = discord.Embed(name="Throw :",
                              description="*__i!throw__* : Vous avez toujours rêvé de lançer des choses sur des gens ? Et bien cette commande est faite pour vous !\n\n L'utilisation est **i!throw [victime]**.",
                              colour=0x110b7a)
    elif com == "ban":
        embed = discord.Embed(name="Ban :",
                              description="*__i!ban__* : Quelqu’un de pas sage? B O N K bannissez le. Mentionnez le après la commande. Cette commande est utilisable seulement par les modérateurs.\n\n L'utilisation est **i!ban {member}**.",
                              colour=0x110b7a)
    elif com == "code":
        embed = discord.Embed(name="Code :",
                              description="*__i!code__* : i20 est un bot très intéressant, si vous souhaitez accéder à son code vous pouvez via cette commande.\n\n L'utilisation est **i!code** tout simplement.",
                              colour=0x110b7a)
    elif com == "ship":
        embed = discord.Embed(name="Ship :",
                              description="*__i!ship__* : On se sent un peu trop Cupidon ces temps-ci ? Pas de problème, i20 prend le relais et trouve les tourtereaux parfaits à votre place !\n\n L'utilisation est **i!ship** tout simplement.",
                              colour=0x110b7a)
    elif com == "date":
        embed = discord.Embed(name="Date :",
                              description="*__i!date__* : Vous vouliez l’heure ? Eh bien non, pourquoi ne pas passer le temps en faisant faire des rendez-vous entre les gens !\n\n L'utilisation est **i!date {user1} {user2}**.\n PS : Tu as trouvé le secret d'i20, essaie donc la commande **i!bonk** ! ",
                              colour=0x110b7a)
    elif com == "flip":
        embed = discord.Embed(name="Flip :",
                              description="*__i!flip__* : Âmes joueuses ? Embarquez dans un pile ou face avec du suspense !\n\n L'utilisation est **i!flip** tout simplement.",
                              colour=0x110b7a)
    elif com == "embed":
        embed = discord.Embed(name="Embed :",
                              description="*__i!embed__* : Vous avez envie de faire des textes ultra stylax ? Cette commande est faite pour vous!\n\n L'utilisation est **i!embed [title] [description] [couleur] {champ1} {desc_champ1} {champ2} {desc_champ2}**.\n PS : Les modérateurs peuvent rajouter 'hidename' **__à la fin__** de leur message afin de cacher leur identité.",
                              colour=0x110b7a)
    elif com == "interesting":
        embed = discord.Embed(name="Interesting :",
                              description="*__i!interesting__* : Vous trouvez que la discussion ou le dernier message est très intéressant ? Alors essayez cette commande !\n\n L'utilisation est **i!interesting** tout simplement.",
                              colour=0x110b7a)
    elif com == "unban":
        embed = discord.Embed(name="Unban :",
                              description="*__i!unban__* : Finalement il a été sage U N B O N K ! Débanissez le. Cette commande est utilisable seulement par les modérateurs.\n\n L'utilisation est **i!unban {user}**.",
                              colour=0x110b7a)
    elif com == "ping":
        embed = discord.Embed(name="Ping :",
                              description="*__i!ping__* : Vous pouvez ping quelqu’un en toute discrétion avec cette commande. Abusez pas S.V.P.\n\n L'utilisation est **i!ping {user}**.",
                              colour=0x110b7a)
    elif com == "meme":
        embed = discord.Embed(name="Meme :",
                              description="*__i!meme__* : Hahaha un meme au hasard ! Hésitez pas à proposer vos memes.\n\n L'utilisation est **i!meme** tout simplement.",
                              colour=0x110b7a)
    elif com == "quote":
        embed = discord.Embed(name="Quote :",
                              description="*__i!quote__* : Yvain et PetitFrapo les grands cultes vous proposent de nombreuses citations aussi inspirantes les unes que les autres. Découvrez les avec cette commande.\n\n L'utilisation est **i!quote** tout simplement.",
                              colour=0x110b7a)
    elif com == "kick":
        embed = discord.Embed(name="Kick :",
                              description="*__i!kick__* : GET THE FRICK OUT OF HERE, autrement dit faites le partir aussi vite qu'il est venu ! Cette commande est utilisable uniquement par les modérateurs.\n\n L'utilisation est **i!kick [member]**.",
                              colour=0x110b7a)
    elif com == "invite":
        embed = discord.Embed(name="Invite :",
                              description="*__i!invite__* : Générez rapidement un lien d’invitation pour faire augmenter la populace !\n\n L'utilisation est **i!invite** tout simplement.",
                              colour=0x110b7a)
    elif com == "poll":
        embed = discord.Embed(name="Poll :",
                              description="*__i!poll__* : Êtes-vous le seul à vous poser cette question bête ? Faites-le savoir en entrant la commande. Le sondage sera envoyé dans le salon adéquat.\n\n L'utilisation est **i!poll [question] [réponse1] [réponse2] {réponse3} {réponse4}**.\n PS : Chaque question et réponse doit être entre guillemets.",
                              colour=0x110b7a)
    elif com == "help":
        embed = discord.Embed(name="Help :",
                              description="*__i!help__* : C'est pas bien dur, vous venez de le faire ! Cette commande affiche ce message !\n\n L'utilisation est **i!help {commande}**.\n PS : Vous pouvez aussi utiliser i!?.",
                              colour=0x110b7a)
    elif com == "syntax":
        embed = discord.Embed(name="Syntaxe :",
                              description="La syntaxe n'est pas bien dure à comprendre !\n **[argument]** : L'argument est obligatoire.\n **{argument}** : L'argument est optionnel.\n Et rien de plus ! Amusez-vous bien avec le bot !",
                              colour=0x110b7a)
    elif com == "say":
        embed = discord.Embed(name="Say :",
                              description="Faites dires des choses loufoques à i20. Il y a néanmoins un filtre de mot.\n PS : On aime pas la choucroute ni le haggis.\n\n L'utilisation est **i!say [textÀDire]**.",
                              colour=0x110b7a)

    await ctx.send(embed=embed)


@bot.command(name="bestcommandever")
@commands.has_role("Modérateurs")
async def bestcommandever(ctx, user: discord.User="Amaury#3218"):
    print(user)
    await user.send("Réveille toi maumau")
    if user != "Amaury#3218":
        await ctx.send("non cette commande a été créée pour maumau")
    await user.send(user.mention)
    await ctx.send("niark niark")

@bot.command(name="randmp3")
async def rdmmsg(ctx):
    failed = False
    await ctx.send("Cette opération peut prendre quelques temps.")
    mp3s = []
    history = await ctx.channel.history(limit=None).flatten()
    for message in history:
        if message.attachments:
            if message.attachments[0].content_type == "audio/mpeg":
                # mp3url = await message.attachments[0].to_file()
                mp3id = message.id
                mp3s.append(mp3id)
    try:
        mp3tosend = random.choice(mp3s)
    except:
        await ctx.send("Désolé, il n'y a pas de MP3 dans ce salon...")
        failed = True
    if failed == False:
        mp3tosendbutforreal: discord.Message = ctx.fetch_message(mp3tosend)
        print(mp3tosendbutforreal)
        file = await mp3tosendbutforreal.attachments[0].to_file()
        await ctx.send(content=f"Profite bien de ton OST !", file=file)

@bot.command(name="randommsg")
async def randommsg(ctx):
    messages = []
    await ctx.send("Cette opération peut prendre quelques temps.")
    history = await ctx.channel.history(limit=None).flatten()
    for message in history:
        messages.append(message.content)
    msgToSend = random.choice(messages)
    await ctx.send(f"Voici un message aléatoire du salon {ctx.channel} !\n")
    await ctx.send(msgToSend)


@bot.command(name="saylog")
@commands.has_role("Modérateurs")
async def saylog(ctx):
    check = False
    try:
        id = ctx.message.reference.message_id
        with open("saylogs.txt", "r") as s:
            for i in s.readlines():
                print(i)
                if id in i:
                    check = True
                    coolestline = i
            s.close()
        if check is True:
            await ctx.send(coolestline)
    except:
        await ctx.send("Erreur. Vérifiez que vous répondez au bon message.")

@bot.command(name="clearlogs")
@commands.has_role("Modérateurs")
async def cl(ctx):
    with open("saylogs.txt", "w+") as s:
        s.write(f"Dernier clear : {datetime.date.today()}")

@bot.command(name="embed")
async def embed(ctx, title, desc, field1="", field1desc="", field2="", field2desc=""):
    hideName = False
    modrole = discord.utils.get(ctx.guild.roles, id=845027528196227133)
    if modrole in ctx.author.roles:
        if ctx.message.content.lower().endswith("hidename"):
            hideName = True
    color = random.randrange(0, 2 ** 24)
    embed = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.datetime.now(tz=timezone))
    member = ctx.author
    if hideName is False:
        embed.set_author(name=member, icon_url=member.avatar_url)
    if field1 != "" and field1desc != "":
        embed.add_field(name=field1, value=field1desc)
    if field2 != "" and field2desc != "":
        embed.add_field(name=field2, value=field2desc)
    await ctx.message.delete()
    await ctx.send(embed=embed)

@bot.command(name="throw")
async def throw(ctx, victim: discord.Member):
  throwmaterials = ["de la crasse", "Amaury", "un fichier PNG", "du pain", "un ballon de basket", "un truc non identifié", "un 12/20 en maths", "des crêpes", "une Pokéball", 'la Master Sword', "une pièce SOS", "un être d'Yvain"]
  throwmaterial = random.choice(throwmaterials)
  await ctx.send(f"{ctx.author.display_name} a lancé {throwmaterial} sur {victim.display_name} ! Il est tout sali maintenant...")
  if victim.display_name == "i20":
    await ctx.send("Aïe ! Qui m'a lancé ça ?")
  if throwmaterial == throwmaterials[8]:
    await ctx.send("...")
    asyncio.sleep(3)
    caught = random.choice([0, 1, 2, 3, 4])
    if caught == 3:
      await ctx.send(f'{ctx.author.display_name} a capturé {victim.display_name} !')
    else:
      await ctx.send(f"{victim.display_name} s'est enfuit !")

@bot.command(name="ship")
async def ship(ctx):
    users = ctx.guild.members
    user1, user2 = random.sample(users, 2)
    part1 = user1.display_name[:len(user1.display_name) // 2]
    part2 = user2.display_name[len(user2.display_name) // 2:]
    babyname = part1 + part2
    await ctx.send(f"{user1.display_name} et {user2.display_name} ont eu un enfant ! Il s'appellera {babyname} !")


bot.loop.create_task(presence())
bot.run(os.getenv("TOKEN"))
