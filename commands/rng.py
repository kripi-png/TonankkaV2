# Made by Jugi
from random import randint
async def execute(msg, args):
    value = 0
    if len(args) == 1: # if you enter no value, command will randomize between 0 and 100
        value = randint(0, 100)

    elif len(args) == 2 and args[1].isnumeric(): # if only one number is given and is a numeral,
        value = randint(0, int(args[1])) # will randomize between 0 and given number.

    elif not args[1].isnumeric() or not args[2].isnumeric(): # if input is not a numeral, will output message
        await msg.channel.send("Can't randomize numbers from words.")
        return

    else:
        value = randint(int(args[1]), int(args[2])) # the 2 numbers after command defines the range of number generator

    await msg.channel.send("Generated: " + str(value))


commandData = {
    "name": "rng",
    "execute": lambda msg,arguments,*args : execute(msg, arguments) # katso ping.py:stä selitys *args-argumentille
}
