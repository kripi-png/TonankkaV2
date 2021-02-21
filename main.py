import discord
import settings, botToken
import commandHandler, databaseHandler as db

client = discord.Client()
commands = commandHandler.loadCommands()
if not db.existsTable("haalarimerkit"): db.createTable("haalarimerkit")

async def runStartUpTasks():
    # check for new patches and post them on the general chat if there are any
    # (x,y) x = server id, y = channel id
    await commands["haalarimerkit"]["execute"](settings.generalChannelID, None, calledFromOutside=True, client=client)

@client.event
async def on_ready():
    print("Running Start Up tasks")
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
