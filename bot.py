import os

import discord
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    bot_guild = None
    for guild in client.guilds:
        if guild.name == GUILD:
            bot_guild = guild

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{bot_guild.name}(id: {bot_guild.id}'
    )

    for channel in bot_guild.channels:
        print(f'Channel Name: {channel.name}')

    for member in bot_guild.members:
        if member.name == "Collin Kleest":
            i = 0
            while (i < 100):
                await member.create_dm()
                await member.dm_channel.send("Sup lil bitch, your lucky they rate limit the discord api ")
                i += 1


@client.event
async def on_member_join(member):
    print("Member just joined!")
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

client.run(TOKEN)
