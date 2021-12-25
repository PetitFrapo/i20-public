import os
import discord
from dotenv import load_dotenv
default_intents = discord.Intents.default()
default_intents.members = True

load_dotenv(dotenv_path="config")

client = discord.Client(intents=default_intents)

@client.event
async def on_ready():
    print("Le bot est prêt !")


# GENRE

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


# LANGUE

@client.event
async def on_raw_reaction_add(payload):
    global role
    message_id = payload.message_id
    if message_id == 853635182551498762:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'Fr':
            role = discord.utils.get(guild.roles, name="Français")
        elif payload.emoji.name == "eng2":
            role = discord.utils.get(guild.roles, name="English")
        else:
            role = None
            print(role)

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
    global role
    message_id = payload.message_id
    if message_id == 853635182551498762:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'Fr':
            role = discord.utils.get(guild.roles, name="Français")
        elif payload.emoji.name == "eng2":
            role = discord.utils.get(guild.roles, name="English")

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

