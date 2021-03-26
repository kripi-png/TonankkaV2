import discord
import os
import datetime

from utils import createEmbed
from youtube_dl import YoutubeDL

path = "song.mp3"
ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist':'True',
    'outtmpl': 'song.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def is_connected(msg, client):
    voice_client = discord.utils.get(client.voice_clients, guild=msg.guild)
    return voice_client and voice_client.is_connected()

def endSong(path):
    os.remove(path)
    # TODO: next in queues

def download_song(arg, url=True):
    with YoutubeDL(ydl_opts) as ydl:
        query = f"ytsearch:{arg}" if not url else arg
        data = ydl.extract_info(query, download=True)
    return data['entries'][0]

def display_info(data):
    return {
        'title': data['title'],
        'duration': data['duration'],
        'uploader': data['uploader'],
        'thumbnail': data['thumbnail'],
        'url': data['webpage_url'],
        'channel': data['channel_url']
    }

async def play(msg, args, client):
    args = " ".join(args[1:])
    video_link = args
    url = True if video_link.startswith("http") else False

    if not msg.author.voice:
        return await msg.channel.send("Sinun on oltava äänikanavalla!")
    else:
        channel = msg.author.voice.channel

    data = download_song(video_link, url)
    info = display_info(data)

    t = info["title"]
    desc = info["url"]
    fields = [
        {"name": "Uploader", "value": f"[{info['uploader']}]({info['channel']})", "inline": True},
        {"name": "Duration", "value": str(datetime.timedelta(seconds=info["duration"])), "inline": True},
    ]
    nowPlayingEmbed = createEmbed(title=t, desc=desc, fields=fields, thumbnail=info["thumbnail"])

    if not is_connected(msg, client): voice_client = await channel.connect()
    else: voice_client = discord.utils.get(client.voice_clients, guild=msg.guild)

    await msg.channel.send("Now Playing", embed=nowPlayingEmbed)
    voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(path))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

commandData = {
    "name": "play",
    "description": "Soita kappale (!play [linkki/hakusanay])",
    "author": "kripi",
    "execute": lambda msg,arguments,client,*args : play(msg, arguments, client) # katso ping.py:stä selitys *args-argumentille
}
