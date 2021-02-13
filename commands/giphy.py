import requests
from random import randint

async def execute(msg, args):
    hakuSanat = "+".join(args[1:]) # luo muuttujan hakuSanat ja antaa sille arvoiksi käytetyt hakusanat
    # hakee Giphy:stä hakusanoilla linkkejä
    r = requests.get("https://api.giphy.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&q={0}&limit=10".format(hakuSanat))

    data = r.json()["data"] # polku data kansioon asti

    l = len(data) # data kansion pituus
    if l == 0: # jos botti ei löydä gifiä hakusanalla, palauttaa lauseen
        return await msg.channel.send("No Gifs found.")
    # tekee requestista json:in, mistä otetaan kymmenestä osumasta randomilla yhden url
    # hakee siis jsonin sisältä koodissa mainituista "kansioista" linkin
    url = data[randint(0, 9 if l > 9 else l)]["images"]["original"]["url"]

    await msg.channel.send(url)

commandData = {
    "name" : "gif",
    "author": "jugi",
    "description": "antaa hakusanojen mukaisen gifin Giphy.com sivulta",
    "execute": lambda msg,arguments,*args : execute(msg, arguments)
}
