import discord
import os

from youtube_dl import YoutubeDL

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
def findSongByQuery(query): return query
def deleteSong(path): os.remove(path)
def download_song(arg, url=True):
    with YoutubeDL(ydl_opts) as ydl:
        query = f"ytsearch:{arg}" if url else arg
        data = ydl.extract_info(query, download=True)
    return data['entries'][0]
def display_info(data):
    video_info = {
        'title': data['title'],
        'duration': data['duration'],
        'uploader': data['uploader'],
        'thumbnail': data['thumbnail'],
        'url': data['webpage_url'],
        'channel': data['channel_url']
    }
    for key, val in video_info.items():
        print(f"{key}: {val}")

async def play(msg, args, client):
    args = " ".join(args[1:])
    video_link = args
    url = True if video_link.startswith("http") else False

    if not msg.author.voice:
        await msg.channel.send("Sinun on oltava äänikanavalla!")
        return
    else:
        channel = msg.author.voice.channel

    data = download_song(video_link, url)
    # display_info(data) # TODO: use this to send a nice embed message

    if not is_connected(msg, client): voice_client = await channel.connect()
    else: voice_client = discord.utils.get(client.voice_clients, guild=msg.guild)


    await msg.channel.send("Now playing: " + args)
    path = "song.mp3"
    voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: deleteSong(path))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)


commandData = {
    "name": "play",
    "description": "Soita linkattu kappale (!play linkki)",
    "author": "kripi",
    "execute": lambda msg,arguments,client,*args : play(msg, arguments, client) # katso ping.py:stä selitys *args-argumentille
}
