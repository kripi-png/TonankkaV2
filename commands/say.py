# Made by X
async def execute(msg, args, client):
    if len(args[1:]) <= 0: return
    await msg.channel.send(" ".join(args[1:]))
    await msg.delete()


commandData = {
    "name": "say",
    "description": "Anna Tonankalle puheenvuoro",
    "author": "kripi",
    "execute": lambda msg,arguments, client, *args : execute(msg, arguments, client) # katso ping.py:stä selitys *args-argumentille
}
