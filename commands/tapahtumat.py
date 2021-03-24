import requests
from datetime import datetime
from utils import createEmbed

def fromWeirdTime(n): return datetime.strptime(n, "%Y-%m-%dT%H:%M:%S%z")
def toNormalTime(n): return datetime.strftime(n, "%d.%m.%Y @ %H:%M")
def fromNormalTime(n): return datetime.strptime(n, "%d.%m.%Y @ %H:%M")
def toNormalTimeWithoutTime(n): return datetime.strftime(fromNormalTime(n), "%d.%m.%Y")

async def execute(msg, args):
    r = requests.get("https://api.kide.app/api/products?city=Turku&productType=1")
    data = r.json()["model"] # where the actual data is
    parsed_data = parseData(data) # remove unnecessary stuff and convert timestamps

    message = createMessage(parsed_data)
    await msg.channel.send(embed=message)

def createMessage(data):
    t = "Tapahtumat"
    fields = []
    
    for event in data:
        print(event)
        # stuff based on whether or not ticket sales have ended
        if event['salesEnded']:
            price = "**Myynti loppunut** :pensive:"
        elif len(event['maxPrice']) and len(event['minPrice']):
            price = f"{format(event['minPrice']['eur']/100,'.2f')}€ - {format(event['maxPrice']['eur']/100,'.2f')}€"
        else:
            price = "Ilmaislippuja"

        # add ticket sale dates if tickets are still for sale
        if price != "**Myynti loppunut** :pensive:":
            # remove time from the timestamp to make the string a bit shorter
            price += f" (Lippuja myydään {toNormalTimeWithoutTime(event['dateSalesFrom'])} - {toNormalTimeWithoutTime(event['dateSalesUntil'])})"

        field = {
            "name": event["name"],
            "value":
                f"**Hinta**: {price}\n" +
                f"**Järjestäjä**: {event['companyName']}\n" +
                f"**Missä**: {event['place']}\n" +
                f"**Päivämäärä**: {event['dateActualFrom']} - {event['dateActualUntil']}\n" +
                f"**Linkki**: [Kide.app]({event['link']})"
        }

        fields.append(field)
    return createEmbed(title=t, fields=fields, thumbnail='https://www.pngitem.com/pimgs/b/185-1852551_beer-icon-png.png') # some random beer icon

def parseData(data):
    parsed_data =[]
    for e in data:
        entry = {
            'companyName': e['companyName'],
            'name': e['name'],
            'place': e['place'],
            'maxPrice': e['maxPrice'],
            'minPrice': e['minPrice'],
            'salesStarted': e['salesStarted'],
            'salesEnded': e['salesEnded'],
            'salesOngoing': e['salesOngoing'],
            'salesPaused': e['salesPaused'],
            'link': 'https://kide.app/fi/events/' + e['id'],

            # convert timestamps from some wacky UTC format
            'dateSalesFrom': toNormalTime(fromWeirdTime(e['dateSalesFrom'])),
            'dateSalesUntil': toNormalTime(fromWeirdTime(e['dateSalesUntil'])),
            'dateActualFrom': toNormalTime(fromWeirdTime(e['dateActualFrom'])),
            'dateActualUntil': toNormalTime(fromWeirdTime(e['dateActualUntil'])),
            'datePublishFrom': toNormalTime(fromWeirdTime(e['datePublishFrom'])),
        }
        parsed_data.append(entry)
    return parsed_data


commandData = {
    "name": "tapahtumat",
    "description": "Listaa tulevat tapahtumat",
    "author": "kripi",
    "execute": lambda msg,arguments,*args : execute(msg, arguments) # katso ping.py:stä selitys *args-argumentille
}
