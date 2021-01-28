# Made by Jugi
from random import randint
async def execute(msg, args):
    value = randint(int(args[1]), int(args[2])) #the 2 numbers after command defines the range of number generator
    await msg.channel.send("Generated: " + str(value))


commandData = {
    "name": "rng",
    "execute": lambda msg,arguments,*args : execute(msg, arguments) # katso ping.py:stä selitys *args-argumentille
}
