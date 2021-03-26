async def uusiKomento(msg, args):
    # await msg.channel.send("Hello!")


commandData = {
    "name": "test",
    "description": "desc",
    "author": "author",
    "execute": lambda msg,arguments,*args : uusiKomento(msg, arguments) # katso ping.py:stä selitys *args-argumentille
}
