import discord
import random
from discord.ext import tasks
from timedEvents import haalarimerkit, tapahtumat
from datetime import datetime
import settings, botToken
import commandHandler, databaseHandler as db

def toDatabaseTime(d): return datetime.strftime(d,"%Y-%m-%d %H:%M:%S")

client = discord.Client()
commands = commandHandler.loadCommands()
if not db.isTable("database"): db.createTable("database")

async def changePresence():
    dbData = db.readTable("activities")
    activityToBeSet = random.choice(dbData)
    game = discord.Game(activityToBeSet)
    await client.change_presence(activity=game)

@tasks.loop(hours=1.0)
async def timedEventLoop():
    print(f"[{datetime.strftime(datetime.now(), '%H:%M')}] Timed Events")
    await changePresence()
    await tapahtumat.postNewEvents(client)
    await haalarimerkit.postNewPatches(client)
    db.writeTable("database", {"lastEventLoopDateCheck": toDatabaseTime(datetime.now())})

async def runStartUpTasks():
    print("Running Start Up tasks...")
    timedEventLoop.start() # start the loop

@client.event
async def on_ready():
    await runStartUpTasks()
    print("All done!")
    print('We have logged in as {0.user}'.format(client)) # lähetä viesti konsoliin, kun botti käynnistyy

@client.event
async def on_message(message):
    if message.author == client.user: return # estä bottia vastaamsta itselleen, jos viestin lähettäjä on sama kuin botti
    if not message.content.startswith(settings.commandPrefix): return # jos viesti EI ala settings.py-tiedostossa määritetyllä prefixillä, peruuta

    message.content = message.content[1:] # poista viestistä prefix
    args = message.content.split() # splitataan viestin/komennon sanat välilyönnin kohdalla -> luodaan lista

    if( args[0] in commands.keys() ): # jos viestin ensimmäinen sana on jokin komennoista commands-dictionaryssä
        await commands[args[0]]["execute"](message, args, client,commands) # suorita execute-funktio kutsutun komennon tiedostossa

client.run(botToken.token)
