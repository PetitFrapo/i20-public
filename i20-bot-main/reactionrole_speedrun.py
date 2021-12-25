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

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 853687348302053426:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'speedrocket':
            role = discord.utils.get(guild.roles, name="Speedrunner")

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
    if message_id == 853687348302053426:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'speedrocket':
            role = discord.utils.get(guild.roles, name="Speedrunner")

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

