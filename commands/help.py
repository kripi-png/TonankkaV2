async def execute(msg, args, commands):
    helpMessage = "\n".join([f"**{commands[x]['name']}** - {commands[x]['desc']}" for x in commands])
    await msg.channel.send(helpMessage)

commandData = {
    "name": "help",
    "author": "jugi & kripi",
    "description": "Lista kaikista komennoista ja niiden descriptioneista",
    "execute": lambda msg,arguments,client,commands,*args : execute(msg, arguments,commands) # katso ping.py:stä selitys *args-argumentille
}
