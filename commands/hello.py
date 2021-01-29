async def execute(msg, args):
    await msg.channel.send("Hello, {0}! I'm Tonankka!".format(msg.author))

commandData = {
    "name": "hello",
    "author": "kripi",
    "description": "Esittelee Tonankan.",
    "execute": lambda msg,arguments,*args : execute(msg, arguments) # katso ping.py:stä selitys *args-argumentille
}
