import discord
import youtube_dl
import logger
import os
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup as bs


class MusicManager(object):

    queue = {}
    logger = logger.Logger()

    def __init__(self, ffmpeg_path):
        self.FFMPEG = ffmpeg_path
        self.voice_client = None
        self.current_song_title = ""
        self.current_song_url = ""
        self.current_song_path = ""

    """
    queues song to an active queue
    :param ctx: dict
    :param url_id: str
    :param url: str
    :returns None
    """
    async def queue_song(self, ctx, url_id: str, url: str) -> None:
        if not self.queue.__contains__(url_id):
            song_title = await self.getYoutubeTitleFromUrl(url)
            self.queue[url_id] = {
                'url': url,
                'title': song_title
            }
            return self.queue, False
        else:
            self.logger.info(
                f'{ctx.message.author} tried to queue a song that is already in the queue at position {self.get_song_position(url_id)}')
            return self.queue, True

    """
    get the size of the queue
    :param self: object
    :returns int
    """

    def queue_size(self) -> int:
        return len(self.queue)

    # TODO: IMPLEMENT THIS
    def remove_song(self, id: str):
        return queue.pop(id)

    """
    returns the postion of a song in the queue by the song id
    not zero based, we add one to the actual list index positon
    :param self: object
    :param song_id: int 
    """

    def get_song_position(self, song_id) -> int:
        if self.queue.__contains__(song_id):
            return list(self.queue).index(song_id) + 1
        else:
            self.logger.warning('Song is not inside queue')

    async def view_queue(self, ctx):
        message = ""
        if (self.queue_size() > 0):
            i = 1
            for song in self.queue.keys():
                message += str(i) + " | " + self.queue[song]["title"] + "\n"
                i += 1
        await ctx.message.channel.send(message)

    """
    downloads song to local directory for bot to play
    uses youtube dl to download, composes mp3 files
    :param self: object
    :param url: str
    :returns None
    """

    def download_song(self, url: str) -> None:
        yt_id = url.split("v=", 1)[1]
        if not (self.songExists(yt_id)):
            self.logger.info("Downloading Song!")
            ydl_opts = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}], 'postprocessor_args': [
                '-ar', '16000'], 'prefer_ffmpeg': True, 'keepvideo': True, 'outtmpl': self.current_song_path, }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            if (self.songExists(yt_id)):
                self.logger.success("Song Successfully Downloaded")
            else:
                self.logger.debug("Song failed to Download")
        else:
            self.logger.info("Song already exists")

    """
    sets current_song_path var
    checks if current song exists in 'resources/music' folder
    :param self: object 
    :param song_id: str
    :returns bool
    """

    def songExists(self, song_id: str) -> bool:
        self.current_song_path = 'resources/music/%s.mp3' % (song_id)
        if os.path.exists(self.current_song_path):
            return True
        else:
            return False

    """
    pauses current song playing
    :param ctx: dict
    :returns None
    """
    async def pause_song(self, ctx):
        if self.voice_client:
            if self.voice_client.is_connected() and self.voice_client.is_playing():
                self.voice_client.pause()
                self.logger.info(
                    f'{ctx.message.author} paused {self.current_song_title}')
                await ctx.message.channel.send(f'{ctx.message.author.mention} paused song: {self.current_song_title}')
            elif self.voice_client.is_connected() and not self.voice_client.is_playing():
                self.logger.warning(
                    f'{ctx.message.author} tried to pause music when music was not playing')
                await ctx.message.channel.send(f'{ctx.message.author.mention} you cannot pause music when the voice client is not playing')
        else:
            self.logger.warning(
                f'{ctx.message.author} tried to pause song when no client is connected / playing a song')
            await ctx.message.channel.send(f'{ctx.message.author.mention} you cannot pause a song that is not playing or connected to the voice client')

    """
    resumes the current song that was playing
    :param ctx: dict
    :returns None
    """
    async def resume_song(self, ctx):
        if self.voice_client:
            if self.voice_client.is_connected() and self.voice_client.is_paused():
                self.voice_client.resume()
                self.logger.info(
                    f'{ctx.message.author} resuming song: {self.current_song_title}')
                await ctx.message.channel.send(f'{ctx.message.author.mention} resumed song: {self.current_song_title}')
            elif self.voice_client.is_connected() and self.voice_client.is_playing():
                self.logger.info(
                    f'{ctx.message.author} tried to resume song: {self.current_song_title} but it is already playing')
                await ctx.message.channel.send(f'{ctx.message.author.mention} {self.current_song_title} is already playing!')
        else:
            self.logger.warning(
                f'{ctx.message.author} tried to resume song when no client is connected / playing a song')
            await ctx.message.channel.send(f'{ctx.message.author.mention} you cannot resume a song that is not connected / currently in playing queue')

    async def play_next(self, ctx, voice_clients):
        if len(self.queue) > 0:
            song_id = list(self.queue.keys())[0]
            song = self.queue.pop(list(self.queue.keys())[0])
            song_path = "resources/music/" + song_id + ".mp3"
            voice_channel = ctx.message.author.voice.channel
            if len(voice_channel.members) > 0:
                if len(voice_clients) == 0:
                    self.voice_client = await voice_channel.connect()
                    await self.trigger_play(ctx)
                else:
                    self.voice_client = voice_clients[0]
                    await self.trigger_play(ctx)
            else:
                self.logger.warning(f'No one present in channel to play music')
        else:
            self.logger.error('Queue is empty cannot play next song')
            await ctx.message.channel.send(f'{ctx.message.author.mention} queue is empty, use command /queue <song_url> to add to the queue')

    async def stop_song(self, ctx, channel, voice_clients):
        if self.voice_client and self.voice_client.is_connected():
            self.voice_client.stop()
            await self.voice_client.disconnect()
            self.logger.info(
                f'{ctx.message.author} stopped currently playing music')
        elif not self.voice_client:
            self.logger.error(f'No voice client is currently connected')
        else:
            self.logger.error(
                f'{ctx.message.author} tried to stop music that was not playing')

    async def play_song(self, ctx, url):
        yt_id = self.getYoutubeIdFromUrl(url)
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
        self.current_song_title = await self.getYoutubeTitleFromUrl(url)
        if os.path.exists(yt_id):
            self.voice_client = await voice_channel.connect()
            self.voice_client.play(discord.FFmpegPCMAudio(
                yt_id, executable=self.FFMPEG))
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.voice_client = await voice_channel.connect()
            self.voice_client.play(discord.FFmpegPCMAudio(
                yt_id, executable=self.FFMPEG))

    def getYoutubeIdFromUrl(self, url: str):
        return url.split("v=", 1)[1]

    async def getYoutubeTitleFromUrl(self, url: str):
        self.logger.info(f'Getting Title for URL: {url}')
        session = AsyncHTMLSession()
        response = await session.get(url)
        await response.html.arender(sleep=1)
        soup = bs(response.html.html, "html.parser")
        self.current_song_title = soup.find("h1").text.strip()
        return self.current_song_title

    async def trigger_play(self, ctx):
        self.voice_client.play(discord.FFmpegPCMAudio(
            self.current_song_path, executable=self.FFMPEG))
        if self.voice_client.is_playing():
            self.logger.info(
                f'{ctx.message.author.mention} is playing {self.current_song_path}')
            await ctx.message.channel.send(f'{ctx.message.author.mention} is playing {self.current_song_path}')
