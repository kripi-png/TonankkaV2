import discord
import settings, botToken
import commandHandler

client = discord.Client()
commands = commandHandler.loadCommands()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client)) # lähetä viesti konsoliin, kun botti käynnistyy

@client.event
async def on_message(message):
    if message.author == client.user: # estä bottia vastaamsta itselleen, jos viestin lähettäjä on sama kuin botti
        return

    if not message.content.startswith(settings.commandPrefix): # jos viesti EI ala setings.py-tiedostossa määritetyllä prefixillä, peruuta
        return

    message.content = message.content[1:] # poista viestistä prefix
    args = message.content.split() # splitataan viestin/komennon sanat välilyönnin kohdalla -> luodaan lista

    if( args[0] in commands.keys() ): # jos viestin ensimmäinen sana on jokin komennoista commands-dictionaryssä
        await commands[args[0]]["execute"](message, args, client,commands) # suorita execute-funktio kutsutun komennon tiedostossa

client.run(botToken.token)
