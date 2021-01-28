async def execute(msg, args):
    await msg.channel.send("**hello** - esittelee Tonankan \n" # creates a list with each command on their own line
        "**help** - listaa komennot ja niiden selitykset \n"
        "**ping** - näyttää botin pingin \n"
        "**rng** - antaa satunnaisen numeron kahden annetun, tai ennalta määritetyn " + \
        "numeron väliltä")

commandData = {
    "name": "help",
    "execute": lambda msg,arguments,*args : execute(msg, arguments) # katso ping.py:stä selitys *args-argumentille
}
