import discord
from discord.ext import commands
from cogs.CONSTANTS import MyBotTreeCopyToYvain

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBotTreeCopyToYvain(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)


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
                                value="*__i!invite__* : Crée une invitation du serveur.\n *__i!avatar__* : Obtient l'avatar du membre.\n *__i!help__* : Affiche ce message.\n *__i!poll__* : Crée un sondage.\n *__i!ost__* : Génère une OST aléatoire.\n *__i!id__* : Prends l'ID de quelqu'un.\n *__i!warns__* : Vois tes avertissements.",
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


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="orihelp", aliases=["ori?"])
    async def help(self, ctx, command=""):
        com = command.lower()
        if com == "":
            embed = discord.Embed(title="Les commandes d'i20 :",
                                  color=0x110b7a,
                                  description="---\ni20 est un bot possédant plein de commandes, les voici :")
            embed.add_field(name="Fun :",
                            value="*__i!interesting__* : Intéressant...\n *__i!flip__* : Pile ou face ?\n *__i!meme__* : Génère un meme aléatoire.\n *__i!date__* : romance.\n *__i!ping__* : NOTIFICATION INTENSIFIES\n *__i!say__* : Faites dire quelque chose à i20 ! Ne dites pas de gros mots ou gare à vous !\n *__i!quote__* : Les citations cultes d'Yvain et PetitFrapo !\n *__i!embed__* : Crée un embed (càd un texte stylé et encadré et tout!).",
                            inline=False)

            embed.add_field(name="Modération :",
                            value="*__i!ban__* : B O N K le marteau\n *__i!unban__* : uaetram el K N O B\n *__i!kick__* : Pour kick les gens pas trétré genti\n *__i!clear__* : Supprime des messages du salon.",
                            inline=False)
            embed.add_field(name="Utile :",
                            value="*__i!invite__* : Crée une invitation du serveur.\n *__i!avatar__* : Obtient l'avatar du membre.\n *__i!help__* : Affiche ce message.\n *__i!poll__* : Crée un sondage.\n *__i!warns__* : Vois tes avertissements.\n *__i!info__* : Informations sur i20",
                            inline=False)
            embed.add_field(name="__*Pour avoir plus de précision sur une commande, veuillez faire 'i!help nomDeLaCommande'.*__",
                            value="Merci à Amaury pour l'aide qu'il a donnée pour la commande <3\n Vous pouvez aussi faire **i!help syntax** pour en apprendre plus sur la syntaxe utilisée dans l'explication des utilisations des commandes.\n---",
                            inline=False)
        elif com == "avatar":
            embed = discord.Embed(title="Avatar :",
                                  description="*__i!avatar__* : Pour prendre l’avatar de quelqu’un ou le sien, mentionnez celui dont vous souhaitez la pp. Prend en charge les jpgs.\n\n L'utilisation est **i!avatar {user}**.",
                                  colour=0x110b7a)
        elif com == "clear":
            embed = discord.Embed(title="Clear :",
                                  description="*__i!clear__* : Supprimez un certain nombre de messages dans le salon où la commande a été exécutée, insérez une valeur après pour renseigner le nombre de messages a supprimer. Cette commande est utilisable seulement par les modérateurs.\n\n L'utilisation est **i!clear {number}**.",
                                  colour=0x110b7a)
        elif com == "ban":
            embed = discord.Embed(title="Ban :",
                                  description="*__i!ban__* : Quelqu’un de pas sage? B O N K bannissez le. Mentionnez le après la commande. Cette commande est utilisable seulement par les modérateurs.\n\n L'utilisation est **i!ban {member}**.",
                                  colour=0x110b7a)
        elif com == "code":
            embed = discord.Embed(title="Code :",
                                  description="*__i!code__* : i20 est un bot très intéressant, si vous souhaitez accéder à son code vous pouvez via cette commande.\n\n L'utilisation est **i!code** tout simplement.",
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
        elif com == "warns":
            embed = discord.Embed(title="Warnings :",
                                  description="*__i!warns__* : Tu veux voir combien de fautes tu as commis sur le serveur ? Utilise la commande !\n\n L'utilisation est **i!warns {member}**.",
                                  colour=0x110b7a)
        elif com == "syntax":
            embed = discord.Embed(title="Syntaxe :",
                                  description="La syntaxe n'est pas bien dure à comprendre !\n **[argument]** : L'argument est obligatoire.\n **{argument}** : L'argument est optionnel.\n Et rien de plus ! Amusez-vous bien avec le bot !",
                                  colour=0x110b7a)
        elif com == "say":
            embed = discord.Embed(title="Say :",
                                  description="Faites dires des choses loufoques à i20. Il y a néanmoins un filtre de mot.\n PS : On aime pas la choucroute ni le haggis.\n\n L'utilisation est **i!say [textÀDire]**.",
                                  colour=0x110b7a)
        else:
            await ctx.send(f"La commande {com} n'existe pas !")
            return

        await ctx.send(embed=embed)


    @commands.command(name="help", aliases=["?"])
    async def helpui(self, ctx: commands.Context, command: str=""):
        com = command.lower()
        if com == "":
            embed = discord.Embed(title="Menu d'aide d'i20 :",
                                  description="Veuillez choisir une catégorie.",
                                  colour=0x110b7a)
            await ctx.send(embed=embed, view=SelectView())
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
        else:
            await ctx.send(f"La commande {com} n'existe pas !")
            return

        if com != "":
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))