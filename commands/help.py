async def execute(msg, args, commands):
    print(commands)
    await msg.channel.send("**hello** - esittelee Tonankan \n" # creates a list with each command on their own line
        "**help** - listaa komennot ja niiden selitykset \n"
        "**ping** - näyttää botin pingin \n"
        "**rng** - antaa satunnaisen numeron kahden annetun, tai ennalta määritetyn " + \
        "numeron väliltä")

commandData = {
    "name": "help",
    "author": "jugi & kripi",
    "description": "Lista kaikista komennoista ja niiden descriptioneista",
    "execute": lambda msg,arguments,client,commands,*args : execute(msg, arguments,commands) # katso ping.py:stä selitys *args-argumentille
}
