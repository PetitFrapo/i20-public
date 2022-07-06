# Cette partie du cog représente la commande help, et oui c'est vachement long.

from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands
from cogs.cogutils import MyBotTreeCopyToYvain, help_embed_maker

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBotTreeCopyToYvain(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents, application_id=853301761572732928)


class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Commandes classiques", emoji="🔧", description="Les commandes classiques  !"),
            discord.SelectOption(label="Commandes slash", emoji="🔨", description="Les commandes slash !"),
            discord.SelectOption(label="Commandes de données", emoji="⛏️", description="Les commandes de données (nouveauté) !")
        ]
        super().__init__(placeholder="Veuillez choisir une catégorie de commandes", max_values=1, min_values=1,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Commandes classiques":
            classhelp = discord.Embed(title="Les commandes d'i20 :",
                                      color=0x110b7a,
                                      description="---\ni20 est un bot possédant plein de commandes, les voici :")
            classhelp.add_field(name="Fun :",
                                value="*__i!flip__* : Pile ou face ?\n *__i!date__* : romance.\n *__i!say__* : Faites dire quelque chose à i20 ! Ne dites pas de gros mots ou gare à vous !\n *__i!quote__* : Les citations cultes d'Yvain et PetitFrapo !\n *__i!throw__* : Lance quelque chose sur quelqu'un.\n *__i!ship__* : uwu~\n *__i!random__* : Génère un ou plusieurs message aléatoire d'un salon.\n *__i!meme__* : Prends un meme aléatoire du subreddit donné (par défaut dans r/memes).\n *__i!edit__* : Modifie un message d'i20.\n *__i!reply__* : Comme i!say, mais i20 répond à un message.",
                                inline=False)

            classhelp.add_field(name="Modération :",
                                value="*__i!ban__* : B O N K le marteau\n *__i!unban__* : uaetram el K N O B\n *__i!kick__* : Pour kick les gens pas trétré genti\n *__i!clear__* : Supprime des messages du salon.\n *__i!pin__* : Épingle le message qui est répondu.\n *__i!warn__* : Permet de warn un utilisateur.\n *__i!removewarn__* : Retire un warn à quelqu'un.\n *__i!warns__* : Vois tes avertissements.\n *__i!mute__* : Mute un utilisateur.\n *__i!unmute__* : Unmute un utilisateur.\n *__i!record__* : Montre le \"casier judiciaire\" d'un utilisateur.",
                                inline=False)
            classhelp.add_field(name="Utile :",
                                value="*__i!invite__* : Crée une invitation du serveur.\n *__i!avatar__* : Obtient l'avatar du membre.\n *__i!help__* : Affiche ce message.\n *__i!poll__* : Crée un sondage.\n *__i!ost__* : Génère une OST aléatoire.\n *__i!id__* : Prends l'ID de quelqu'un.\n *__i!embed__* : Crée un embed (càd un texte stylé et encadré et tout!).\n *__i!profile__* : Montre le profil détaillé d'un utilisateur.\n *__i!submit__* : Propose tes idées pour i20, ça m'aide beaucoup !\n *__i!source__* : Regarde le code source d'une commande.\n *__i!raw__* : Obtiens l'image d'un emoji.",
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
                                value="*__/8ball__* : Demandez une question à i20, il vous répondra !\n *__/flip__* : Pile ou face ?\n *__/meme__* : Prends un meme aléatoire du subreddit donné (par défaut dans r/memes).",
                                inline=False)
            slashhelp.add_field(name="Modération :",
                                value="*__/ban__* : B O N K le slashteau",
                                inline=False)
            slashhelp.add_field(name="Utile :",
                                value="*__/math__* : Utilise une calculette divine !\n *__/poll__* : Crée un sondage.\n *__/embed__* : Crée un embed.\n *__/hexa__* : Traduis un nombre en héxadécimal.\n *__/shorten__* : Raccourcis une URL.\n *__/help__* : Affiche ce message.\n *__/info__* : Informations supplémentaires sur i20.\n *__/submit__* : Propose une idée pour i20, ça m'aide beaucoup !")
            slashhelp.add_field(
                name="__*Pour avoir plus de précision sur une commande, veuillez faire 'i!help nomDeLaCommande'.*__",
                value="Merci à Amaury pour l'aide qu'il a donnée pour la commande <3\n Vous pouvez aussi faire **/help syntax** pour en apprendre plus sur la syntaxe utilisée dans l'explication des utilisations des commandes.\n---",
                inline=False)
            await interaction.response.edit_message(embed=slashhelp)
        elif self.values[0] == "Commandes de données":
            dbhelp = discord.Embed(title="Les commandes de données d'i20 :",
                                   description="---\ni20 possède désormais une troisième et dernière catégorie de commandes : les commandes de données ! Ces commandes sont une révolution pour i20, car elle vous permettent d'utiliser pleinement de l'enregistrement dans une table.\n**Veuillez noter que ces commandes sont __à la fois__ classiques et slash**.",
                                   colour=0x110b7a)
            dbhelp.add_field(name="Enregistrer des valeurs :",
                             value="*__register__* : Manier des données dans un tableau. Possède des sous-commandes que voici :\n *__register add__* : Ajoute une donnée dans un tableau.\n *__register remove__* : Retire la valeur associée à une clé.\n *__register get__* : Obtiens la valeur associée à une clé.\n *__register show__* : Montre l'entièreté de la table.",
                             inline=False)
            dbhelp.add_field(name="Enregistrer des embeds :",
                             value="*__regembed__* : Créer et envoyer un embed dans un tableau. Possède des sous-commandes que voici :\n *__regembed add__* : Ajoute un embed dans un tableau.\n *__regembed remove__* : Retire l'embed associé à l'étiquette donnée.\n *__regembed send__* : Envoie l'embed associée à l'étiquette donnée.\n *__regembed show__* : Montre l'entièreté de la table.",
                             inline=False)
            dbhelp.add_field(name="Enregistrer des boutons :",
                             value="*__button__* : Enregistre un bouton dans un tableau. Possède des sous-commandes que voici :\n *__button add__* : Ajoute un bouton dans un tableau.\n *__button remove__* : Retire le bouton associé à l'étiquette donnée.\n *__button send__* : Envoie le bouton associée à l'étiquette donnée.\n *__button show__* : Montre l'entièreté de la table.",
                             inline=False)
            dbhelp.add_field(name="Enregistrer ton annviersaire :",
                             value="*__birthday__* : Une fonctionnalité _très_ attendue. Et je pèse mes mots. Possède des sous-commandes que voici :\n *__birthday set__* : Enregistre ton anniversaire.\n *__birthday remove__* : Retire ton anniversaire de la base de données d'i20.\n *__birthday list__* : Liste les anniversaires du serveur.",
                             inline=False)
            dbhelp.add_field(name="Et, pour mélanger tout ça :",
                             value="*__send__* : Permets d'envoyer un message avec, facultativement, un embed et jusqu'à trois boutons, enregistrés préalablement.",
                             inline=False)
            await interaction.response.edit_message(embed=dbhelp)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout=360):
        super().__init__(timeout=timeout)
        self.add_item(Select())


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", aliases=["?"], description="Menu d'aide d'i20.")
    @app_commands.describe(command="La commande dont tu veux obtenir les détails.")
    async def helpui(self, ctx: commands.Context, *, command: Optional[str] = ""):
        com = command.lower()
        if com == "":
            embed = discord.Embed(title="Menu d'aide d'i20 :",
                                  description="Veuillez choisir une catégorie.",
                                  colour=0x110b7a)
            await ctx.send(embed=embed, view=SelectView())

        # CLASSIC COMMANDS
        # FUN COMMANDS
        elif com == "flip":
            embed = discord.Embed(title="La commande hybride flip :",
                                  description="Âmes joueuses ? Embarquez dans un pile ou face avec du suspense !\n L'utilisation est **i!flip** tout simplement.",
                                  colour=0x110b7a)
        elif com == "date":
            embed = discord.Embed(title="La commande date :",
                                  description="Vous vouliez l’heure ? Eh bien non, pourquoi ne pas passer le temps en faisant faire des rendez-vous entre les gens !\n L'utilisation est **i!date {user1} {user2}**.\n **{user1}** correspond au premier utilisateur.\n **{user2}** correspond au second utilisateur.\n\n PS : Tu as trouvé le secret d'i20, essaie donc la commande **i!bonk** ! ",
                                  colour=0x110b7a)
        elif com == "say":
            embed = discord.Embed(title="La commande say :",
                                  description="Faites dires des choses loufoques à i20. Il y a néanmoins un filtre de mot.\n PS : On aime pas la choucroute ni le haggis.\n L'utilisation est **i!say [texteÀDire]**\n **[texteÀDire]** correspond au... texte à... dire ?.",
                                  colour=0x110b7a)
        elif com == "quote":
            embed = discord.Embed(title="La commande quote :",
                                  description="Yvain et les modos, les grands cultes, vous proposent de nombreuses citations aussi inspirantes les unes que les autres. Découvrez les avec cette commande.\n L'utilisation est **i!quote** tout simplement.",
                                  colour=0x110b7a)
        elif com == "throw":
            embed = discord.Embed(title="La commande throw :",
                                  description="Vous avez toujours rêvé de lançer des choses sur des gens ? Et bien ~~vous êtes bizarre~~ cette commande est faite pour vous !\n L'utilisation est **i!throw [victime]**.\n **[victime]** correspond à la personne sur laquelle vous voulez lancer quelque chose.",
                                  colour=0x110b7a)
        elif com == "ship":
            embed = discord.Embed(title="La commande ship :",
                                  description="On se sent un peu trop Cupidon ces temps-ci ? Pas de problème, i20 prend le relais et trouve les tourtereaux parfaits à votre place !\n L'utilisation est **i!ship {member1} {member2}**.\n **{member1}** correspond au premier membre a ship, si vous ne voulez pas d'aléatoire.\n **{member1}** correspond au secind membre à ship, si vous ne voulez pas d'aléatoire.",
                                  colour=0x110b7a)
        elif com == "random":
            embed = discord.Embed(title="La commande random :",
                                  description="Sentiments de nostalgie ? Pas de problème, cette commande cherche un ou plusieurs message aléatoire dans ce ou un autre salon !\n L'utilisation est **i!random {nombre} {salon}**.\n **{nombre}** correspond au nombre de messages à obtenir. Si non spécifié, il vaut 1.\n **{salon}** correspond au salon dans lequel les messages doivent être obtenus. Si non spécifié, c'est le salon de la commande.",
                                  colour=0x110b7a)
        elif com == "meme":
            embed = discord.Embed(title="La commande hybride meme :",
                                  description="Obtiens un meme aléatoire de Reddit. C'est toujours sympa de temps en temps !\n L'utilisation est **i!meme {subreddit}**.\n **{subreddit}** correspond au subreddit (sans le \"r/\").",
                                  colour=0x110b7a)
        elif com == "edit":
            embed = discord.Embed(title="La commande edit :",
                                  description="Modifie un message que i20 a écrit, par exemple après une faute avec i!say.\n L'utilisation est **i!edit [newText]** en répondant au message à modifier.\n **{newText}** correspond au nouveau texte.",
                                  colour=0x110b7a)
        elif com == "reply":
            embed = discord.Embed(title="La commande reply :",
                                  description="Exactement comme i!say, cependant i20 répondra à un message.\n L'utilisation est **i!reply [texteÀDire]** en répondant au message à répondre.\n **[texteÀDire]** correspond au texte à dire.",
                                  colour=0x110b7a)

        # MODERATION COMMANDS
        elif com == "ban":
            embed = discord.Embed(title="La commande hybride ban :",
                                  description="Quelqu’un de pas sage ? B O N K bannissez le. Cette commande est utilisable seulement par les modérateurs.\n L'utilisation est **i!ban [member]**.\n **[member]** correspond au membre à bannir.",
                                  colour=0x110b7a)
        elif com == "unban":
            embed = discord.Embed(title="La commande unban :",
                                  description="Finalement il a été sage U N B O N K ! Débanissez le. Cette commande est utilisable seulement par les modérateurs.\n\n L'utilisation est **i!unban {user}**.\n **{user}** correspond au __nom et tag__ de l'utilisateur à débannir.",
                                  colour=0x110b7a)
        elif com == "kick":
            embed = discord.Embed(title="La commande kick :",
                                  description="GET THE FRICK OUT OF HERE, autrement dit faites le partir aussi vite qu'il est venu ! Cette commande est utilisable uniquement par les modérateurs.\n L'utilisation est **i!kick [member]**.\n **[member]** correspond à l'utilisateur à kick.",
                                  colour=0x110b7a)
        elif com == "clear":
            embed = discord.Embed(title="La commande clear :",
                                  description="Supprimez un certain nombre de messages dans le salon où la commande a été exécutée. Cette commande est utilisable seulement par les modérateurs.\n L'utilisation est **i!clear [number]**.\n **[number]** correspond au nombre de messages.",
                                  colour=0x110b7a)
        elif com == "pin":
            embed = discord.Embed(title="La commande pin :",
                                  description="Vous avez envie d'épingler un message mais vous êtes sur mobile et, pfiou trop la flemme ? Cette commande est donc trop cool ! Cette commande est utilisable uniquement par les modérateurs.\n L'utilisation est **i!pin** tout en répondant à un message.",
                                  colour=0x110b7a)
        elif com == "warn":
            embed = discord.Embed(title="La commande warn :",
                                  description="Quelqu'un a fait quelque chose de pas gentil et tu veux qu'il s'en souvienne ? Mets-lui un avertissement, tu verras, c'est rigolo ! Cette commande est utilisable seulement par les modérateurs.\n L'utilisation est **i!warn [member] {reason}**.\n **[member]** correspond au membre a warn.\n **{reason}** correspond à la raison du warn. Si rien n'est spécifié, aucune raison n'est donnée.",
                                  colour=0x110b7a)
        elif com == "removewarn":
            embed = discord.Embed(title="La commande removewarn :",
                                  description="moooooh vous êtes trop sympa comme modo, excuse quelqu'un lui retirant son dernier warn !\n L'utilisation est **i!removewarn [membreÀExcuser]**.\n **[membreÀExcuser]** correspond au membre à excuser.",
                                  colour=0x110b7a)
        elif com == "warns":
            embed = discord.Embed(title="La commande warns :",
                                  description="Tu veux voir combien de fautes tu as commis sur le serveur ? Utilise la commande !\n L'utilisation est **i!warns {member}**.\n **{member}** correspond au membre dont vous voulez voir les avertissements. Si non précisé, il devient l'utilisateur de la commande.",
                                  colour=0x110b7a)
        elif com == "mute":
            embed = discord.Embed(title="La commande mute :",
                                  description="Un membre ne respecte pas les règles, mais pas au point de lui mettre un warn ? Mute-le donc grâce à cette commande ! Cette commande est utilisable seulement par les modérateurs.\n L'utilisation est **i!mute [member] [hours] {reason}**.\n **[member]** correspond au membre à mute.\n **[hours]** correspond au nombre d'heures le membre doit être mute.\n **{reason}** correspond à la raison du mute. Si non précisé, aucune raison ne sera donnée.",
                                  colour=0x110b7a)
        elif com == "unmute":
            embed = discord.Embed(title="La commande unmute :",
                                  description="Tu as mute un membre trop longtemps, et il s'est gentiment excusé ? Retire-lui son mute avec cette commande... Cette commande est utilisable seulement par les modérateurs.\n L'utilisation est **i!unmute [member] {reason}**.\n **[member]** correspond au membre à unmute.\n **{reason}** correspond à la raison de l'unmute. Si non précisé, aucune raison ne sera donnée.",
                                  colour=0x110b7a)
        elif com == "record":
            embed = discord.Embed(title="La commande record :",
                                  description="Tu es modo et tu veux un pôle de toutes les actions de modération ? Alors, cette commande est faite pour toi ! Cette commande est utilisable seulement par les modérateurs.\n L'utilisation est **i!record [member]**.\n **[member]** correspond au membre dont vous voulez voir le casier.",
                                  colour=0x110b7a)

        # USEFUL COMMANDS
        elif com == "invite":
            embed = discord.Embed(title="La commande invite :",
                                  description="Générez rapidement un lien d’invitation pour faire augmenter la populace !\n L'utilisation est **i!invite** tout simplement.",
                                  colour=0x110b7a)
        elif com == "avatar":
            embed = discord.Embed(title="La commande avatar :",
                                  description="Pour prendre l’avatar de quelqu’un ou le sien, mentionnez (ou donnez l'identifiant de) celui dont vous souhaitez la photo de profil.\n L'utilisation est **i!avatar {user}**.\n **{user}** correspond à l'utilisateur (ID ou mention).",
                                  colour=0x110b7a)
        elif com == "help":
            embed = discord.Embed(title="La commande hybride help :",
                                  description="C'est pas bien dur, vous venez de le faire ! Cette commande affiche ce message !\n L'utilisation est **i!help {commande}**.\n **{commande}** correspond a la commande pour laquelle vous voulez obtenir plus d'informations.",
                                  colour=0x110b7a)
        elif com == "poll":
            embed = discord.Embed(title="La commande hybride poll :",
                                  description="Êtes-vous le seul à vous poser cette question bête ? Faites-le savoir en entrant la commande. Le sondage sera envoyé dans le salon adéquat. Deux réponses minimum sont attendues.\n L'utilisation est **i!poll [question] [réponse1] [réponse2] {réponse3} {réponse4}**.\n **[question]** correspond à la question du sondage.\n **[réponse1]** correspond à la première réponse.\n **[réponse2]** correspond à la seconde réponse.\n **{réponse3}** correspond à la troisième réponse.\n **{réponse4}** correspond à la quatrième réponse.\n\n PS : Chaque question et réponse doit être entre guillemets.",
                                  colour=0x110b7a)
        elif com == "ost":
            embed = discord.Embed(title="La commande ost :",
                                  description="Envie d'écouter une OST de jeux vidéos ? Parfait ! La commande vous en passe une super cool !\n L'utilisation est **i!ost** tout simplement.",
                                  colour=0x110b7a)
        elif com == "id":
            embed = discord.Embed(title="La commande id :",
                                  description="Tu veux utiliser une commande comme **i!date** mais tu n'as pas envie de mentionner la personne car c'est un modérateur ou car tu ne veux pas gêner la personne ? Et bien utilise cette commande, et remplace la mention de la personne par son identifiant. Tu verras ça marche ! \n\n L'utilisation est **i!id [memberName]**.\n **[memberName]** correspond à la mention/le nom du membre.",
                                  colour=0x110b7a)
        elif com == "embed":
            embed = discord.Embed(title="La commande hybride embed :",
                                  description="Vous avez envie de faire des textes ultra stylax comme celui-ci ? Cette commande est faite pour vous !\n L'utilisation est **i!embed [title] [description] {champ1} {desc_champ1} {champ2} {desc_champ2}**.\n **[title]** correspond au titre de l'embed.\n **[description]** correspond à la description de l'embed.\n **{champ1}** correspond au titre du premier champ de l'embed.\n **{desc_champ1}** correspond à la description du premier champ de l'embed.\n **{champ2}** correspond au titre du second champ de l'embed.\n **{desc_champ2}** correspond à la description du second champ de l'embed.\n\n PS : Les modérateurs peuvent rajouter 'hidename' **__à la fin__** de leur message afin de cacher leur identité.",
                                  colour=0x110b7a)
        elif com == "profile":
            embed = discord.Embed(title="La commande profile :",
                                  description="En savoir plus sur quelqu'un, c'est toujours sympa non ? Avec cette commande, obtiens une petite fiche !\n L'utilisation est **i!profile [member]**.\n **[member]** correspond au membre dont vous voulez obtenir la fiche.",
                                  colour=0x110b7a)
        elif com == "submit":
            embed = discord.Embed(title="La commande hybride submit :",
                                  description="Parfois, on a des idées pour i20, et on ne sait pas comment les donner... Eh bien, utilisez cette commande et remplissez le questionnaire. Ça m'aide beaucoup <:Yvlove:968153859103014962> !!\n L'utilisation est **i!submit** tout simplement.",
                                  colour=0x110b7a)
        elif com == "source":
            embed = discord.Embed(title="La commande source :",
                                  description="\"Il est vachement bien codé ce bot dites donc 👀, si seulement je pouvais en obtenir le code source, mais raah flemme de chercher dans le GitHub, je veux juste UNE commande en particulier... Ah mais attends, mais oui, LA COMMANDE SOURCE !\"\n L'utilisation est **i!source [commande]**.\n **[commande]** correspond à la commande dont vous voulez obtenir le code source.",
                                  colour=0x110b7a)
        elif com == "raw":
            embed = discord.Embed(title="La commande raw :",
                                  description="Vous aimez bien un emoji du serveur, et vous voulez le même sur le vôtre ? Cette commande est pour vous !\n L'utilisation est **i!raw [emoji]**.\n **[emoji]** correspond à l'emoji dont vous voulez obtenir l'image source.",
                                  colour=0x110b7a)

        # SYNTAX HELP
        elif com == "syntax":
            embed = discord.Embed(title="Aide par rapport à la syntaxe des aides :",
                                  description="La syntaxe n'est pas bien dure à comprendre !\n **[argument]** : L'argument est obligatoire.\n **{argument}** : L'argument est optionnel.\n Et rien de plus ! Amusez-vous bien avec le bot !",
                                  colour=0x110b7a)

        # SLASH COMMANDS
        elif com == "8ball":
            embed = discord.Embed(title="La commande slash 8ball :",
                                  description="Une question vous turlupine ? Posez-la donc à i20 !\n L'utilisation est **/8ball [question]**.\n **[question]** correspond à la question que vous voulez poser.",
                                  colour=0x110b7a)
        elif com == "math":
            embed = discord.Embed(title="La commande slash math :",
                                  description="Vous voulez faire un calcul complexe, mais flemme de chercher la calculette ? Demandez à i20 !\n L'utilisation est **/math [terme1] [operateur] [terme2]**.\n **[terme1]** correspond au premier terme du calcul.\n **[operateur]** correspond à l'opérateur du calcul.\n **[terme2]** correspond au second terme du calcul.\n\n PS : Les opérateurs possibles sont :\n  - **+** : correspond à une addition.\n  - **-** : correspond à une soustraction.\n  - **\*** : correspond à une multiplication.\n  - **\*\*** : correspond à \"puissance\" ou \"exposant\".\n  - **/** : correspond à une division.\n  - **//** : correspond au quotient d'une division euclidéenne.\n  - **%** : correspond au modulo (reste d'une division euclidéenne).",
                                  colour=0x110b7a)
        elif com == "hexa":
            embed = discord.Embed(title="La commande slash hexa :",
                                  description="Transformer un nombre en hexadécimal, c'est toujours pratique ! i20 peut donc le faire !\n L'utilisation est **/hexa [nombre]**.\n **[nombre]** correspond au nombre à convertir.",
                                  colour=0x110b7a)
        elif com == "shorten":
            embed = discord.Embed(title="La commande slash shorten :",
                                  description="Parfois, on veut faire un rickroll, mais mettre le lien c'est cramé... Donc utilisez l'API de cutt.ly pour raccourcir et changer vos liens !\n L'utilisation est **/shorten [lien]**.\n **[lien]** correspond au lien à raccourcir.",
                                  colour=0x110b7a)

        # DATA COMMANDS
        elif com == "register":
            embed = help_embed_maker("de données register",
                                     "Parfois on veut noter des choses, mais on oublie. Que ce soit pour réviser des trucs ou juste de se mettre des petits rappels, la commande register peut vous aider ! Veuillez noter qu'elle ne peut pas être utilisée telle quelle car c'est un **groupe** de commandes.",
                                     use="register [add|remove|get|show]")
        elif com == "register add":
            embed = help_embed_maker("de données register add",
                                     "Sert à ajouter les données dans le tableau. Il faut préciser une clé et une valeur. La clé est en quelque sorte le \"prénom\" de la valeur.",
                                     use="register add [key] [value]",
                                     argsuse={"[key]": "au nom de la clé de la valeur", "[value]": "à la valeur"})
        elif com == "register remove":
            embed = help_embed_maker("de données register remove",
                                     "Sert à retirer une valeur dans le tableau.",
                                     use="register remove [key]",
                                     argsuse={"[key]": "au nom de la clé de la valeur à retirer"})
        elif com == "register get":
            embed = help_embed_maker("de données register remove",
                                     "Obtiens une valeur du tableau.",
                                     use="register get [key]",
                                     argsuse={"[key]": "au nom de la clé de la valeur à obtenir"})
        elif com == "register show":
            embed = help_embed_maker("de données register show",
                                     "Montre l'entièreté de la table à l'utilisateur. Utile pour obtenir le nom des clés avant de les retirer.",
                                     use="register show tout simplement")
        elif com == "regembed":
            embed = help_embed_maker("de données regembed",
                                     "Vous voulez envoyer des embeds trop cools, plusieurs fois ? Alors enregistrez-le ! Cette commande peut paraître complexe mais elle ne l'est pas ! Veuillez noter qu'elle ne peut pas être utilisée telle quelle car c'est un **groupe** de commandes.",
                                     use="regembed [add|send|remove|show]")
        elif com == "regembed add":
            embed = help_embed_maker("de données regembed add",
                                     "Ajoute un embed dans votre table d'embeds. Il faut préciser une étiquette. L'étiquette vous servira à retrouver l'embed pour le supprimer ou l'envoyer.",
                                     use="regembed add [etiquette] [title] [description] {footer} {titrechamp1} {descchamp1} {titrechamp2} {descchamp2}",
                                     argsuse={"[etiquette]": "à l'étiquette à donner à l'embed", "[title]": "au titre de l'embed",
                                              "[description]": "à la description de l'embed", "{footer}": "au footer (texte en bas) de l'embed",
                                              "{titrechamp1}": "au titre du premier champ de l'embed", "{descchamp1}": "à la description du premier champ de l'embed",
                                              "{titrechamp2}": "au titre du second champ de l'embed", "{descchamp2}": "à la description du second champ de l'embed"})
        elif com == "regembed remove":
            embed = help_embed_maker("de données regembed remove",
                                     "Sert à retirer un embed du tableau.",
                                     use="regembed remove [etiquette]",
                                     argsuse={"[etiquette]": "à l'étiquette de l'embed à retirer"})
        elif com == "regembed send":
            embed = help_embed_maker("de données regembed send",
                                     "Envoie un embed du tableau. Il faut l'avoir créé préalablement avec **regembed add**.",
                                     use="regembed send [etiquette] {texte}",
                                     argsuse={"[etiquette]": "à l'étiquette de l'embed à envoyer", "{texte}": "au texte à envoyer avec l'embed."})
        elif com == "regembed show":
            embed = help_embed_maker("de données regembed show",
                                     "Montre l'entièreté de la table des embeds à l'utilisateur. Utile pour obtenir le nom des embeds avant de les envoyer.",
                                     use="regembed show tout simplement")
        elif com == "button":
            embed = help_embed_maker("de données button",
                                     "Vous voulez envoyer des boutons trop cools, qui peuvent rediriger vers des liens, exécuter du code ? Utilisez une des sous-commandes ! Cette commande peut paraître complexe mais elle ne l'est pas ! Veuillez noter qu'elle ne peut pas être utilisée telle quelle car c'est un **groupe** de commandes.",
                                     use="button [add|send|remove|show]")
        elif com == "button add":
            embed = help_embed_maker("de données button add",
                                     "Ajoute un bouton dans votre table d'embeds. Il faut préciser une étiquette. L'étiquette vous servira à retrouver l'embed pour le supprimer ou l'envoyer.",
                                     use="button add [etiquette] [label] [style] {url} {code}",
                                     argsuse={"[etiquette]": "à l'étiquette à donner au bouton", "[label]": "au texte écrit sur le bouton",
                                              "[style]": "à la couleur du bouton",
                                              "{url}": "à l'URL auquelle le bouton redirigera (notez que le style sera forcément gris si une URL est précisée)",
                                              "{code}": "au code qui s'exécutera quand le bouton sera cliqué.\n\n __**Codes possible**__ :\n - 1. envoyer \"message\" : Enverra le message précisé **dans les guillemets** dans le salon du bouton lors d'un clic.\n - 2. mp \"message\" : Enverra le message précisé **dans les guillemets** en message privé à la personne qui clique le bouton.\n - 3. mentionner \"utilisateur\" : Mentionnera l'utilisateur dont le nom est précisé lors d'un clic.\n Veuillez noter que pour les 3 actions peut être rajouté un nombre d'exécutions, en rajoutant \"x\" et le nombre de fois (ex: x10).\n\n Par exemple, on peut mettre \"envoyer \"coucou les chenapans\" x10\", et cela enverra 10 fois le message \"coucou les chenapans.\""})
        elif com == "button remove":
            embed = help_embed_maker("de données button remove",
                                     "Sert à retirer un bouton du tableau.",
                                     use="button remove [etiquette]",
                                     argsuse={"[etiquette]": "à l'étiquette du bouton à retirer"})
        elif com == "button send":
            embed = help_embed_maker("de données button send",
                                     "Envoie un bouton du tableau. Il faut l'avoir créé préalablement avec **regembed add**.",
                                     use="button send [etiquette] {texte}",
                                     argsuse={"[etiquette]": "à l'étiquette du bouton à envoyer", "{texte}": "au texte à envoyer avec le bouton."})
        elif com == "button show":
            embed = help_embed_maker("de données button show",
                                     "Montre l'entièreté de la table des boutons à l'utilisateur. Utile pour obtenir le nom des boutons avant de les envoyer.",
                                     use="button show tout simplement")
        elif com == "birthday":
            embed = help_embed_maker("de données birthday",
                                     "Aaaaah, les anniversaires... C'est bien non ? Et bien, ça peut être encore mieux, car i20 peut vous le souhaiter. AVEC DES MESSAGES PERSOS AAAAH TROP BI1!!!! Veuillez noter qu'elle ne peut pas être utilisée telle quelle car c'est un **groupe** de commandes.",
                                     use="birthday [set|remove|list]")
        elif com == "birthday set":
            embed = help_embed_maker("de données birthday set",
                                     "Ouvre un menu vous permettant de rentrer votre anniversaire. NE MARCHE PAS SUR MOBILE.",
                                     use="birthday set tout simplement")
        elif com == "birthday remove":
            embed = help_embed_maker("de données birthday remove",
                                     "Retire votre anniversaire de i20, si vous voulez ne plus être notifié. Vous serez aussi bien évidemment retiré de la liste de **birthday list**.",
                                     use="birthday remove tout simplement")
        elif com == "birthday list":
            embed = help_embed_maker("de données birthday list",
                                     "Liste tous les anniversaires du serveur.",
                                     use="birthday list tout simplement")
        elif com == "send":
            embed = help_embed_maker("hybride send",
                                     "Permet d'envoyer un message, accompagné d'éléments tels que des embeds ou des boutons. Il faut les créer préalablement avec **regembed add** et **button add**.",
                                     use="send [message] {embed} {button1} {button2} {button3}",
                                     argsuse={"[message]": "au texte à envoyer.",
                                              "{embed}": "à l'étiquette du embed à joindre",
                                              "{button1}": "au premier bouton à joindre",
                                              "{button2}": "au second bouton à joindre",
                                              "{button3}": "au troisième bouton à joindre"})


        else:
            await ctx.send(f"La commande {com} n'existe pas !")
            return

        if com != "":
            await ctx.send(embed=embed)


# On ajoute le cog au bot.
async def setup(bot):
    await bot.add_cog(Help(bot))