import os

import discord
from discord.ext import commands
import dotenv

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

BOT_PREFIX = '/'

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix=BOT_PREFIX)


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')


@client.event
async def on_ready():
    bot_guild = None
    for guild in client.guilds:
        if guild.name == GUILD:
            bot_guild = guild

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{bot_guild.name}(id: {bot_guild.id})'
    )


@client.event
async def on_member_join(member):
    print("Member just joined!")
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

client.run(TOKEN)
