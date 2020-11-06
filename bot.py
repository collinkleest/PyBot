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
dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
FFMPEG = os.getenv('FFMPEG_PATH')
music_manager = music_manager.MusicManager(FFMPEG)

intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.

client = commands.Bot(command_prefix='/', intents=intents)


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


"""
puts song in a queue to play
:param ctx: dict
:param url: str
"""


@client.command(name='queue', help='Queue Song | (url)')
async def queue(ctx, url: str):
    url_id = url.split("v=", 1)[1]
    music_manager.download_song(url)
    current_queue, is_present = await music_manager.queue_song(ctx, url_id, url)
    if is_present == False:
        queue_position = list(current_queue).index(url_id) + 1
        logger.info(
            f'{ctx.message.author} queued song: {current_queue[url_id]["title"]} at queue position {queue_position}')
        message = f'{ctx.message.author.mention} queued song: {current_queue[url_id]["title"]} at queue position: {queue_position}'
        await ctx.message.channel.send(message)
    else:
        message = f'{ctx.message.author.mention} this song is already in the queue at position {music_manager.get_song_position(url_id)}'
        await ctx.message.channel.send(message)


"""
plays a song inside of a voice channel
will target the vocie channel that the command 
sender is presently in
:param ctx: dict 
:param url: str
"""


@client.command(name='play', help='Play song with youtube url')
async def play(ctx, url: str):
    await music_manager.play_song(ctx, url)


"""
pauses the current song playing if there is a client
playing music inside a voice channel
:param ctx: dict
"""


@client.command(name='pause', help='Pause the current song that is playing.')
async def pause(ctx):
    await music_manager.pause_song(ctx)


# resume playing music if voice client is connected and in a paused state
@client.command(name='resume', help='Resume playing current music')
async def resume(ctx):
    await music_manager.resume_song(ctx)


@client.command(name='play_next', help='Play next song in queue')
async def play_next(ctx):
    await music_manager.play_next(ctx, client.voice_clients)


@client.command(name='view_queue', help='View what is currently inside the queue')
async def view_queue(ctx):
    await music_manager.view_queue(ctx)

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
    await music_manager.stop_song(ctx, channel, client.voice_clients)


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
