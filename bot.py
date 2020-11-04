from __future__ import unicode_literals
import os

import music_manager
import logger
import discord
from discord.ext import commands
import dotenv
import random as ran
import requests as req

import youtube_dl

logger = logger.Logger()
music_manager = music_manager.MusicManager()
dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
FFMPEG = os.getenv('FFMPEG_PATH')


intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.

client = commands.Bot(command_prefix='/', intents=intents)
global voiceclient


# executed when bot starts
@client.event
async def on_ready():
    logger.info(f'{client.user} connected to Discord!')


# ping bot to make sure it is running
@client.command(name='ping', help='Ping the bot to make sure it is running')
async def ping(ctx):
    logger.info(
        f'Bot: {client.user} pinged from {ctx.message.channel} channel pinged by user: {ctx.message.author.name}')
    await ctx.message.channel.send(f'{client.user} is active')


# funny spam command
@client.command()
async def spamVin(ctx, numberOfMessages: int):
    guild = ctx.guild
    member = discord.utils.get(guild.members, name="ProdyV")
    for i in range(numberOfMessages | 200):
        dm_msg = await member.create_dm()
        await dm_msg.send(f'Hi fucker!')


# send message to user from bot
# @params user, msg
@client.command(name='message', help='Send message from bot | (user, messsage)')
async def message(ctx, user: str, msg: str):
    guild = ctx.guild
    target_member = discord.utils.get(guild.members, name=user)
    if target_member:
        logger.info(
            f'{ctx.message.author} sent a message: "{msg}" to {target_member}')
        dm_msg = await target_member.create_dm()
        await dm_msg.send(msg)
    else:
        logger.error(
            f'{ctx.message.author} tried to send message: "{msg}" to {user} but user was not found')


# queue song
@client.command(name='queue', help='Queue Song | (url)')
async def queue(ctx, url: str):
    url_id = url.split("=", 1)[1]
    music_manager.download_song(url)
    music_manager.add_song(url_id, url)
    logger.info(f'{ctx.message.author} queued song {url}')


# play music from youtube url
@client.command(name='play', help='Play song with youtube url')
async def play(ctx, url: str):
    global voiceclient
    yt_id = url.split("=", 1)[1]
    yt_id = "resources/music/" + yt_id + ".mp3"
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
        'outtmpl': yt_id,
    }
    voice_channel = ctx.message.author.voice.channel
    if os.path.exists(yt_id):
        voiceclient = await voice_channel.connect()
        voiceclient.play(discord.FFmpegPCMAudio(
            yt_id, executable=FFMPEG))
    else:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        voiceclient = await voice_channel.connect()
        voiceclient.play(discord.FFmpegPCMAudio(
            yt_id, executable=FFMPEG))


# pause if voiceclient is currently playing music
@client.command(name='pause', help='Pause the current song that is playing.')
async def pause(ctx):
    global voiceclient
    if voiceclient.is_connected() and voiceclient.is_playing():
        voiceclient.pause()
        logger.info(f'{ctx.message.author} paused currently playing song')
    else:
        logger.error(
            f'{ctx.message.author} tried to pause song that is not playing')


# resume playing music if voice client is connected and in a paused state
@client.command(name='resume', help='Resume playing current music')
async def resume(ctx):
    global voiceclient
    if voiceclient.is_connected() and voiceclient.is_paused():
        voiceclient.resume()
        logger.info(f'{ctx.message.author} resumed currently playing song')
    else:
        logger.error(
            f'{ctx.message.author} tried to resume song that is not playing')


@client.command(name='play_next', help='Play next song in queue')
async def play_next(ctx):
    global voiceclient
    music_manager.play_next(ctx.message.author, voiceclient)


# welcome message event handler for new user
@client.event
async def on_member_join(member):
    if member == client:
        return
    dm_msg = await member.create_dm()
    await dm_msg.send(f'Hi {member.name} welcome to {member.guild} !')


# move memeber around voice channels
@client.command(name='channelTroll', help='Troll someone by moving them around discord voice channels (admin only)')
@commands.has_role('Admin')
async def channelTroll(ctx, member_name: str):
    guild = ctx.guild
    member = discord.utils.get(guild.members, name=member_name)
    if member != None:
        for i in range(3):
            for channel in guild.voice_channels:
                await member.move_to(channel)


# stop music
@client.command(name='stop', help='Stops currently playing music')
async def stop(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        voice.stop()
        await voice.disconnect()
        logger.info(f'{ctx.message.author} stopped currently playing music')
    else:
        logger.error(
            f'{ctx.message.author} tried to stop music that was not playing')


# get active bitcoin price
@client.command(name='bitcoin', help='Get current price of bitcoin')
async def bitcoin(ctx):
    bitcoin_request = req.get(
        "https://api.coindesk.com/v1/bpi/currentprice.json")
    if bitcoin_request.status_code != 200:
        logger.error(
            f'{ctx.message.author} requested current bitcoin price, but request failed with status_code: {bitcoin_request.status_code}')
        await ctx.message.channel.send("Couldn't get the curren price of bitcoin")
    bitcoin_data = bitcoin_request.json()
    bitcoin_price_usd = bitcoin_data['bpi']['USD']['rate']
    bitcoin_price_gbp = bitcoin_data['bpi']['GBP']['rate']
    bitcoin_price_eur = bitcoin_data['bpi']['EUR']['rate']
    message = f'BitCoin USD: {bitcoin_price_usd}\nBitCoin GBP: {bitcoin_price_gbp}\nBitCoin Euro: {bitcoin_price_eur}'
    logger.info(f'{ctx.message.author} requested bitcoin price and got USD: {bitcoin_price_usd} EURO: {bitcoin_price_eur} GBP: {bitcoin_price_gbp}')
    await ctx.message.channel.send(message)


# generate random number for user
@client.command(name='random', help="Displays Random Number | (start, end)")
async def random(ctx, start: int = 1, end: int = 100):
    ran_num = ran.randint(start, end)
    logger.info(
        f'{ctx.message.author} requested a random number in between {start} - {end} and got {ran_num}')
    await ctx.message.channel.send(f'Your random number is: {ran_num}')


client.run(TOKEN)
