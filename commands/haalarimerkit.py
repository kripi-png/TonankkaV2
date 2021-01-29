import requests, json, xmltodict
from datetime import datetime # muuten pitäisi käyttää datetime.datetime..., nyt riittää datetime...

async def execute(msg, args):
    r = requests.get('https://www.merkattu.fi/kauppa/feed/') # requestaa datalista
    data = xmltodict.parse(r.text) # muuta data xml -> python dictionary
    data = data["rss"]["channel"]["item"] # rajaa listasta vain tarvittava tieto
    # päivämäärä ja kellonaika, jolloin uudet merkit on viimeksi tarkistettu
    lastDateChecked = datetime.strptime("Sun, 17 Jan 2021 15:00:00 +0000", '%a, %d %b %Y %H:%M:%S %z');

    newPatches = [] # luodaan lista, johon uudet merkit kerätään dictionaryna
    for item in data:
        convertedDate = datetime.strptime(item["pubDate"], '%a, %d %b %Y %H:%M:%S %z') # muuta merkin julkaisupäivämäärä vertailtavaan muotoon
        if lastDateChecked < convertedDate: # jos merkki on julkaistu myöhemmin kuin lastDateChecked, on se uusi merkki
            newPatches.append({"name": item["title"], "date": item["pubDate"], "link": item["link"].split('?')[0]}) # lisätään merkki uusien merkkien listaan

    updateMessage = '__**Uusia merkkejä!**__\n'
    for merkki in newPatches:
        updateMessage += "**{}** - {}\n".format(merkki["name"], merkki["link"])

    await msg.channel.send(updateMessage)



commandData = {
    "name": "haalarimerkit",
    "author": "kripi",
    "description": "Listaa uudet merkit merkattu.fi-sivustolta.",
    "execute": lambda msg,arguments,*args : execute(msg, arguments) # katso ping.py:stä selitys *args-argumentille
}
