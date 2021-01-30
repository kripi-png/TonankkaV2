import requests, json, xmltodict
from datetime import datetime # muuten pitäisi käyttää datetime.datetime..., nyt riittää datetime...
from databaseHandler import *

def convertDateFromRequest(d): return datetime.strptime(d,'%a, %d %b %Y %H:%M:%S %z')
def convertDateFromDatabase(d): return datetime.strptime(d,"%Y-%m-%d %H:%M:%S %z")
def convertDateForDatabase(d): return datetime.strftime(d,"%Y-%m-%d %H:%M:%S %z")

async def execute(msg, args, calledFromOutside=False, client=None): # calledFromOutside is for checking if the code is being run as a command or when the bot boots up
    # if kwargs:
    #     calledFromOutside,client = kwargs["calledFromOutside"],kwargs["client"]
    r = requests.get('https://www.merkattu.fi/kauppa/feed/') # requestaa data
    merkkiData = xmltodict.parse(r.text) # muuttaa data xml -> python dictionary
    merkkiData = merkkiData["rss"]["channel"]["item"] # rajaa listasta vain tarvittava tieto (actual merkkilista)
    # merkkiData = merkattu.fi-sivustolta tuleva tieto, dbData = databasesta tuleva tieto
    dbData = readTable("mainData")
    # päivämäärä ja kellonaika, jolloin uudet merkit on viimeksi tarkistettu
    lastDateChecked = convertDateFromDatabase(dbData["haalarimerkit"]["lastDateChecked"])
    newPatches = [] # luodaan lista, johon uudet merkit kerätään dictionaryna

    for item in merkkiData:
        convertedDate = convertDateFromRequest(item["pubDate"]) # muuta merkin julkaisupäivämäärä vertailtavaan muotoon
        if lastDateChecked < convertedDate: # jos merkki on julkaistu myöhemmin kuin lastDateChecked, on se uusi merkki
            # lisätään merkki uusien merkkien listaan; .split():llä linkistä poistetaan turha osa
            newPatches.append({"name": item["title"], "date": convertedDate, "link": item["link"]})

    newCount = len(newPatches)
    updateMessage = '__**Viimeisimmät merkit: ({})**__\n'.format(str(newCount)+" uutta")

    if not calledFromOutside: # jos komentoa suoritetaan komentona
        while len(newPatches) < 3: # jos uusia merkkejä on vähemmän kuin 3, täydennetään listaa vanhemmilla
            newPatches.append(
                {"name": merkkiData[len(newPatches)]["title"],
                "date": convertDateFromRequest(merkkiData[len(newPatches)]["pubDate"]),
                "link": merkkiData[len(newPatches)]["link"]
            })

    for merkki in newPatches: # luodaan viesti merkkient nimistä ja linkeistä
        updateMessage += "**{}** - {}\n".format(merkki["name"], merkki["link"].split('?')[0]) # .split lyhentää linkkiä poistamalla turhan osan

    if newCount > 0 and calledFromOutside: # jos komentoa kutsutaan käynnistyksen yhteydessä, msg on general channelin ID
        await client.get_channel(msg).send(updateMessage)
    else:
        await msg.channel.send(updateMessage)

    dbData["haalarimerkit"]["lastDateChecked"] = convertDateForDatabase(datetime.now())+'+0000'
    writeTable("mainData", dbData)


commandData = {
    "name": "haalarimerkit",
    "author": "kripi",
    "description": "Listaa uudet merkit merkattu.fi-sivustolta.",
    # katso ping.py:stä selitys *args-argumentille. **kwargs toimii kuten *args, mutta keyword argumenteille (keyword=value)
    "execute": lambda msg,arguments,*args,**kwargs : execute(msg, arguments, **kwargs)
}
