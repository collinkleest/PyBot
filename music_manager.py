import discord
import os
import youtube_dl


class MusicManager(object):

    queue = {}
    FFMPEG = os.getenv('FFMPEG_PATH')

    def __init__(self):
        pass

    def add_song(self, url_id: str, url: str):
        self.queue[url] = url_id

    def queue_size(self) -> int:
        return len(queue)

    def remove_song(self, id: str):
        return queue.pop(id)

    def download_song(self, url: str):
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
        if os.path.exists(yt_id):
            pass
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

    def play_next(self, user: str, vc):
        song_id = self.queue.pop(next(iter(self.queue.keys())))
        song_path = "resources/music/" + song_id + ".mp3"
        if (vc.is_connected() and vc.is_playing()):
            vc.pause()
            vc.play(discord.FFmpegPCMAudio(
                song_path, executable=self.FFMPEG))
        else:
            vc.play(discord.FFmpegPCMAudio(
                song_path, executable=self.FFMPEG))
