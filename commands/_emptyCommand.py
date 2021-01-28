# Made by X
async def execute(msg, args):
    # await msg.channel.send("Hello!")


commandData = {
    "name": "",
    "execute": lambda msg,arguments,*args : execute(msg, arguments) # katso ping.py:stä selitys *args-argumentille
}
