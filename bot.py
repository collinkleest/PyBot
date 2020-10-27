from __future__ import unicode_literals
import os

import logger
import discord
from discord.ext import commands
import dotenv
import random as ran
import requests as req

import youtube_dl

logger = logger.Logger()
dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
FFMPEG = os.getenv('FFMPEG_PATH')
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }],
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'prefer_ffmpeg': True,
    'keepvideo': True,
    'outtmpl': 'song.mp3'
}

intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.

client = commands.Bot(command_prefix='/', intents=intents)
global voiceclient

# executed when bot starts


@client.event
async def on_ready():
    print(f'{client.user} connected to Discord!')


# ping bot to make sure it is running
@client.command()
async def ping(ctx):
    logger.info(
        f'Bot: {client.user} pinged from {ctx.message.channel} channel pinged by user: {ctx.message.author.name}')
    await ctx.message.channel.send(f'{client.user} is active')


# play music from youtube url
@client.command()
async def play(ctx, url: str):
    global voiceclient
    if os.path.exists("song.mp3"):
        os.remove("song.mp3")
    voice_channel = ctx.message.author.voice.channel
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    voiceclient = await voice_channel.connect()
    voiceclient.play(discord.FFmpegPCMAudio(
        "song.mp3", executable=FFMPEG))


# pause if voiceclient is currently playing music
@client.event
async def pause(ctx):
    global voiceclient
    if voiceclient.is_connected() and voiceclient.is_playing():
        voiceclient.pause()


# welcome message event handler for new user
@client.event
async def on_member_join(member):
    if member == client:
        return
    dm_msg = await member.create_dm()
    await dm_msg.send(f'Hi {member.name} welcome to {member.guild} !')


# move memeber around voice channels
@client.command()
@commands.has_role(['Admin'])
async def channelTroll(ctx, member_name: str):
    guild = ctx.guild
    member = discord.utils.get(guild.members, name=member_name)
    if member != None:
        for i in range(3):
            for channel in guild.voice_channels:
                await member.move_to(channel)


# stop music
@client.command()
async def stop(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        voice.stop()
        await voice.disconnect()


# get active bitcoin price
@client.command(name='bitcoin', help='Gets the current price of bitcoin')
async def bitcoin(ctx):
    bitcoin_request = req.get(
        "https://api.coindesk.com/v1/bpi/currentprice.json")
    if bitcoin_request.status_code != 200:
        await ctx.message.channel.send("Couldn't get the curren price of bitcoin")
    bitcoin_data = bitcoin_request.json()
    bitcoin_price_usd = bitcoin_data['bpi']['USD']['rate']
    bitcoin_price_gbp = bitcoin_data['bpi']['GBP']['rate']
    bitcoin_price_eur = bitcoin_data['bpi']['EUR']['rate']
    message = f'BitCoin USD: {bitcoin_price_usd}\nBitCoin GBP: {bitcoin_price_gbp}\nBitCoin Euro: {bitcoin_price_eur}'
    await ctx.message.channel.send(message)


# generate random number for user
@client.command(name='randomnumber', help="Displays a random number from 1 to 100, you can pass in a starting number and ending number as well")
async def randomnumber(ctx, start: int = 1, end: int = 100):
    ran_num = ran.randint(start, end)
    await ctx.message.channel.send(f'Your random number is: {ran_num}')


client.run(TOKEN)
