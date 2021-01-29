# Made by Jugi
from random import randint
async def execute(msg, args):
    value = 0
    if len(args) == 1: # if you enter no value, command will randomize between 0 and 100
        value = randint(0, 100)

    elif len(args) == 2 and args[1].lstrip("-").isnumeric(): # if only one number is given and is a numeral,
        if int(args[1]) < 0: # if number is <0, command will randomize between given number and 0
            value = randint(int(args[1]), 0)
        else:
            value = randint(0, int(args[1])) # will randomize between 0 and given number.

    elif not args[1].lstrip("-").isnumeric() or not args[2].lstrip("-").isnumeric(): # if input is not a numeral, will output message
        await msg.channel.send("Can't randomize numbers from words.")
        return

    else:
        if args[2] < args[1]: # checks if second number is smaller than the first one
            value = randint(int(args[2]), int(args[1]))
        else:
            value = randint(int(args[1]), int(args[2])) # the 2 numbers after command defines the range of number generator

    await msg.channel.send(value)


commandData = {
    "name": "rng",
    "author": "jugi",
    "description": "antaa satunnaisen numeron kahden annetun, tai ennalta määritetyn numeron väliltä",
    "execute": lambda msg,arguments,*args : execute(msg, arguments) # katso ping.py:stä selitys *args-argumentille
}
