# Cette partie du code représente tout ce qui est lié aux commandes register, regembed et button.
# Elles sont très complexes à comprendre, c'est normal d'être perdu.

from typing import Optional, List
import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context
from discord import app_commands, ui
from cogs.cogutils import MyBot, get_db

default_intents = discord.Intents.all()
default_intents.members = True
default_intents.message_content = True

bot = MyBot(command_prefix="i!", case_insensitive=True, help_command=None, intents=default_intents,
            application_id=853301761572732928)


class Database(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="register")
    async def registerdb(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Entrez une sous-commande.")

    @registerdb.command(name="add", description="Rajoute une valeur à ta table.")
    @app_commands.describe(key="Le nom de la clé", value="La valeur de la clé.")
    async def add_db(self, ctx: Context, key: str, value: str):
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 981950728056754200, id)
        data[id][key] = value
        try:
            await dictid.edit(content=str(data))
        except discord.HTTPException:
            await ctx.send("Tu ne peux pas rajouter de valeurs car tu as atteint la limite ! Essaie d'en retirer.")
            return
        await ctx.send(f"La valeur **{value}** a bien été associée à la clé **{key}** dans ta table personnelle !")

    @registerdb.command(name="remove", description="Retire une clé de ta table.")
    @app_commands.describe(key="La cle à retirer.")
    async def remove_db(self, ctx: Context, key: str):
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 981950728056754200, id)
        if not id in data.keys():
            await ctx.send("Tu ne peux pas retirer de valeurs puisque tu n'as pas de table !")
        else:
            if key not in data[id].keys():
                await ctx.send(f"La valeur **{key}** n'existe pas ! Tu ne peux donc pas la retirer !")
            else:
                del data[id][key]
                await dictid.edit(content=str(data))
                await ctx.send(f"La clé **{key}** a bien été retirée de ta table !")

    @registerdb.command(name="get", description="Obtiens une valeur de ta table.")
    @app_commands.describe(key="La clé que tu veux obtenir.")
    async def get_db(self, ctx: Context, key: str):
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 981950728056754200, id)
        if key not in data[id].keys():
            await ctx.send(
                f"La valeur **{key}** n'existe pas ! Fais **i!register add {key} [valeur]** pour la rajouter.")
        else:
            lookedfor = data[id][key]
            await ctx.send(f"La clé **{key}** possède la valeur **{lookedfor}** dans ta table !")

    @registerdb.command(name="show", description="Montre tout le contenu de ta table.")
    async def show_db(self, ctx: Context):
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 981950728056754200, id)
        list = []
        prettylist = f""
        for i in data[id].keys():
            list.append([i, data[id][i]])
            prettylist = prettylist + f"**{i}** : {data[id][i]}\n"

        if prettylist == "":
            await ctx.send(
                "Tu n'as aucune valeur dans ta table ! Fais **!data add [nomDeLaClé] [valeur]** pour en rajouter une.")
        else:
            embed = discord.Embed(title=f"Table de {ctx.author.name} :", description=prettylist,
                                  colour=discord.Colour.random())
            await ctx.send(embed=embed)

    @commands.hybrid_group(name="modregister", description="Interface modérateurs de la commande register.")
    async def modregisterdb(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Entrez une sous-commande.")

    @modregisterdb.command(name="add_for", description="Rajoute une valeur à ta table.")
    @app_commands.checks.has_role("Modérateurs")
    @commands.has_role("Modérateurs")
    @app_commands.describe(key="Le nom de la clé", value="La valeur de la clé.", target="La personne à qui tu veux ajouter la clé.")
    async def add_for_db(self, ctx: Context, target: discord.Member, key: str, value: str):
        id = str(target.id)
        data, dictid = await get_db(ctx, self.bot, 981950728056754200, id)
        data[id][key] = value
        try:
            await dictid.edit(content=str(data))
        except discord.HTTPException:
            await ctx.send("Tu ne peux pas rajouter de valeurs car tu as atteint la limite ! Essaie d'en retirer.")
        await ctx.send(f"La valeur **{value}** a bien été associée à la clé **{key}** dans la table de {target.name} !")

    @modregisterdb.command(name="remove_for", description="Retire une clé de la table de quelqu'un.")
    @app_commands.checks.has_role("Modérateurs")
    @commands.has_role("Modérateurs")
    @app_commands.describe(key="La cle à retirer.", target="La personne dont tu veux retirer la valeur.")
    async def remove_for_db(self, ctx: Context, target: discord.Member, key: str):
        id = str(target.id)
        data, dictid = await get_db(ctx, self.bot, 981950728056754200, id)
        if not id in data.keys():
            await ctx.send("Tu ne peux pas retirer de valeurs puisque la cible n'a pas de table !")
        else:
            if key not in data[id].keys():
                await ctx.send(f"La valeur **{key}** n'existe pas ! Tu ne peux donc pas la retirer !")
            else:
                del data[id][key]
                await dictid.edit(content=str(data))
                await ctx.send(f"La clé **{key}** a bien été retirée de la table de {target.name} !")

    @modregisterdb.command(name="get_for", description="Obtiens une valeur de la table de quelqu'un.")
    @app_commands.checks.has_role("Modérateurs")
    @commands.has_role("Modérateurs")
    @app_commands.describe(key="La clé dont tu veux obtenir la valeur.",
                           target="La personne dont tu veux obtenir la valeur.")
    async def get_for_db(self, ctx: Context, target: discord.Member, key: str):
        id = str(target.id)
        data, dictid = await get_db(ctx, self.bot, 981950728056754200, id)
        if key not in data[id].keys():
            await ctx.send(
                f"La valeur **{key}** n'existe pas ! Fais **i!register add_for {key} [valeur] [{target.name}]** pour la rajouter.")
        else:
            lookedfor = data[id][key]
            await ctx.send(f"La clé **{key}** possède la valeur **{lookedfor}** dans la table de {target.name} !")

    @modregisterdb.command(name="show_for", description="Montre tout le contenu de la table de quelqu'un.")
    @app_commands.describe(target="La personne dont tu veux voir la table.")
    @app_commands.checks.has_role("Modérateurs")
    @commands.has_role("Modérateurs")
    async def show_for_db(self, ctx: Context, target: discord.Member):
        id = str(target.id)
        data, dictid = await get_db(ctx, self.bot, 981950728056754200, id)
        list = []
        prettylist = f""
        for i in data[id].keys():
            list.append([i, data[id][i]])
            prettylist = prettylist + f"**{i}** : {data[id][i]}\n"

        if prettylist == "":
            await ctx.send(
                "Il n'y a aucune valeur dans cette table ! Fais **!data add [nomDeLaClé] [valeur]** pour en rajouter une.")
        else:
            embed = discord.Embed(title=f"Table de {target.name} :", description=prettylist,
                                  colour=discord.Colour.random())
            await ctx.send(embed=embed)

    @commands.hybrid_group(name="button")
    async def button_db(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Entrez une sous-commande.")

    @button_db.command(name="add", description="Ajoute un bouton à ta table personnelle.")
    @app_commands.describe(etiquette="Le nom du bouton, pour le réutiliser.", label="Le texte sur le bouton.", style="Le style du bouton.", url="L'URL du bouton.")
    async def add_btn_db(self, ctx: Context, etiquette: str, label: str, style: str, url: Optional[str]):
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 981950835036659742, id)
        if style == "vert":
            style = "discord.ButtonStyle.green"
        elif style == "rouge":
            style = "discord.ButtonStyle.red"
        elif style == "gris":
            style = "discord.ButtonStyle.grey"
        elif style in {"blurple", "url"}:
            style = f"discord.ButtonStyle.{style}"
        else:
            await ctx.send("Le style rentré n'est pas correct !", ephemeral=True)
            return
        data[id][etiquette] = {"label": label, "style": style, "url": url}
        try:
            await dictid.edit(content=str(data))
        except discord.HTTPException:
            await ctx.send("Tu ne peux pas rajouter de boutons car tu as atteint la limite ! Essaie d'en retirer.")
        await ctx.send(f"Le bouton **{etiquette}** a bien été ajouté à ta table personnelle !")

    @add_btn_db.autocomplete("style")
    async def style_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        styles = ["blurple", "vert", "rouge", "url", "gris"]
        return [
            app_commands.Choice(name=style, value=style)
            for style in styles if current.lower() in style.lower()
        ]


    @button_db.command(name="send", description="Envoie un de tes boutons enregistrés.")
    @app_commands.describe(etiquette="L'étiquette du bouton.", texte="Le message à envoyer avant le bouton.")
    async def send_btn_db(self, ctx: Context, etiquette: str, texte: Optional[str] = ""):
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 981950835036659742, id)
        if etiquette not in data[id].keys():
            await ctx.send(f"Le bouton avec comme étiquette \"{etiquette}\" n'existe pas dans ta table !")
            return
        buttondata = data[id][etiquette]

        button = ui.Button(label=buttondata["label"], style=eval(buttondata["style"]), url=buttondata["url"])
        view = ui.View().add_item(button)
        if texte != "":
            await ctx.send(texte, view=view)
        else:
            await ctx.send(view=view)


    @button_db.command(name="remove", description="Retire un bouton de ta table de boutons.")
    @app_commands.describe(etiquette="L'étiquette du bouton.")
    async def rem_btn_db(self, ctx: Context, etiquette: str):
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 981950835036659742, id)
        if etiquette in data[id].keys():
            del data[id][etiquette]
        else:
            await ctx.send(f"Le bouton **{etiquette}** n'existe pas dans ta table !")
            return
        await dictid.edit(content=str(data))
        await ctx.send(f"Le bouton **{etiquette}** a bien été retiré de ta table !")

    @button_db.command(name="show", description="Montre les boutons de ta table.")
    async def show_btn_db(self, ctx: Context):
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 981950835036659742, id)
        tags = []
        i = 0
        for tag in data[id].keys():
            i += 1
            tags.append(f"{i}. {tag}")
        embed = discord.Embed(title=f"Boutons de {ctx.author.name}", description="\n".join(tags), color=discord.Colour.random())
        await ctx.send(embed=embed)

    @commands.hybrid_group(name="regembed")
    async def regembed(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Entrez une sous commande.")

    @regembed.command(name="add", description="Ajoute un embed à ta table.")
    @app_commands.describe(title="Le titre de l'embed.", description="La description de l'embed.", footer="Le texte en bas de l'embed.", titrechamp1="Le titre du premier champ.", descchamp1="La description du premier champ.", titrechamp2="Le titre du deuxième champ.", descchamp2="La description du deuxième champ.")
    async def db_ebd_add(self, ctx: Context, etiquette: str, title: str, description: str, footer: Optional[str] = None, titrechamp1: Optional[str] = None, descchamp1: Optional[str] = None, titrechamp2: Optional[str] = None, descchamp2: Optional[str] = None):
        if (titrechamp1 is not None and descchamp1 is None) or (titrechamp2 is not None and descchamp2 is None) or (titrechamp1 is None and descchamp1 is not None) or (titrechamp2 is None and descchamp2 is not None):
            await ctx.send("Veuillez préciser le titre ET la valeur d'un champ.")
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 981950865348890644, id)
        data[id][etiquette] = {"title": title, "description": description, "fields": []}
        if all([titrechamp1 is not None, descchamp1 is not None]):
            data[id][etiquette]["fields"].append({"inline": False, "name": titrechamp1, "value": descchamp1})
        if all([titrechamp2 is not None, descchamp2 is not None]):
            data[id][etiquette]["fields"].append({"inline": False, "name": titrechamp2, "value": descchamp2})
        if len(data[id][etiquette]["fields"]) == 0:
            del data[id][etiquette]["fields"]
        if footer is not None:
            data[id][etiquette]["footer"] = {"text": footer}

        try:
            await dictid.edit(content=str(data))
        except discord.HTTPException:
            await ctx.send("Tu ne peux pas rajouter d'embeds car tu as atteint la limite ! Essaie d'en retirer.")

        await ctx.send(f"L'embed **{etiquette}** a bien été ajouté à ta table personnelle !")

    @regembed.command(name="send", description="Envoie un embed de ta table.")
    @app_commands.describe(etiquette="L'étiquette du embed à envoyer.")
    async def db_ebd_send(self, ctx: Context, etiquette: str, texte: Optional[str] = None) -> None:
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 981950865348890644, id)
        if etiquette not in data[id].keys():
            await ctx.send(f"L'embed avec comme étiquette \"{etiquette}\" n'existe pas dans ta table !")
            return
        embeddata = data[id][etiquette]

        embed = discord.Embed().from_dict(embeddata)
        await ctx.send(texte, embed=embed)

    @regembed.command(name="remove", description="Retire un embed de ta table.")
    @app_commands.describe(etiquette="L'etiquette de l'embed à retirer.")
    async def db_ebd_rem(self, ctx: Context, etiquette: str):
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 981950865348890644, id)
        if etiquette in data[id].keys():
            del data[id][etiquette]
        else:
            await ctx.send(f"L'embed **{etiquette}** n'existe pas dans ta table !")
            return
        await dictid.edit(content=str(data))
        await ctx.send(f"L'embed **{etiquette}** a bien été retiré de ta table !")

    @regembed.command(name="show", description="Montre les embeds de ta table.")
    async def db_ebd_show(self, ctx: Context):
        id = str(ctx.author.id)
        data, dictid = await get_db(ctx, self.bot, 981950835036659742, id)
        tags = []
        i = 0
        for tag in data[id].keys():
            i += 1
            tags.append(f"{i}. {tag}")
        embed = discord.Embed(title=f"Embeds de {ctx.author.name}", description="\n".join(tags), color=discord.Colour.random())
        await ctx.send(embed=embed)


# On ajoute le cog au bot.
async def setup(bot: MyBot):
    await bot.add_cog(Database(bot))
