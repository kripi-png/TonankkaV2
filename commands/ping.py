async def execute(msg, args, client):
    # print(client.latency)
    await msg.channel.send("pong! {0}ms".format(round(client.latency * 1000))) # client.latency palauttaa viiveen sekunteina

commandData = {
    "name": "ping",
    "execute": lambda msg,arguments,client,*args : execute(msg, arguments, client)  # eri komennot vaativat eri määrän argumentteja
                                                                                    # jos komentoa kutsuttaessa funktiolle annetaan liikaa argumentteja,
                                                                                    # ohjelma palauttaa erroreita. *args muodostaa listan kaikista "ylimääräisistä"
                                                                                    # argumenteista, jolloin erroreita ei synny.
}
