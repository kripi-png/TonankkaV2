import requests
from datetime import datetime
from utils import createEmbed
from databaseHandler import *
from settings import engineerColor, notificationChannelID

KIDE_LOGO = "https://kide.app/content/images/themes/kide/favicon/launcher-icon-4x.png?v=020221"

def getEventImageLink(str): return "https://portalvhdsp62n0yt356llm.blob.core.windows.net/bailataan-mediaitems/" + str;
def fromWeirdTime(n,format="%Y-%m-%dT%H:%M:%S%z"): return datetime.strptime(n, format)
def toNormalTime(n): return datetime.strftime(n, "%d.%m.%Y @ %H:%M")
def fromNormalTime(n): return datetime.strptime(n, "%d.%m.%Y @ %H:%M")
def toNormalTimeWithoutTime(n): return datetime.strftime(fromNormalTime(n), "%d.%m.%Y")
def fromDatabaseTime(d): return datetime.strptime(d,"%Y-%m-%d %H:%M:%S")

def isNewer(date):
    """compares 'date' and the date saved in the database, returns true if database time was before"""
    return fromDatabaseTime(readTable("database")["lastEventLoopDateCheck"]) < date

async def postNewEvents(client):
    r = requests.get("https://api.kide.app/api/products?city=Turku&productType=1")
    data = r.json()["model"] # where the actual data is
    parsed_data = parseData(data) # remove unnecessary stuff and convert timestamps
    new_events = checkForNewEvents(parsed_data)
    if len(new_events) > 0:
        print("New Events!")
        for x in parsed_data:
            embed = createEventEmbed(x)
            await client.get_channel(notificationChannelID).send(embed=embed)

def checkForNewEvents(events):
    new_events = []
    for x in events:
        if isNewer(x["datePublishFrom"]): new_events.append(x)
    return new_events

def createEventEmbed(event):
    title = event["name"]
    eventImageLink = event['eventImageLink']
    price = getEventPrice(event)
    fields = [
        { "name": "Hinta",
            "value": f"{price}" },
        { "name": "Järjestäjä",
            "value": f"{event['companyName']}",
            "inline": True },
        { "name": "Tapahtumapaikka",
            "value": f"{event['place']}",
            "inline": True },
        { "name": "Päivämäärä",
            "value": f"{event['dateActualFrom']} - {event['dateActualUntil']}" },
        { "name": "Linkki",
            "value": f"[Kide.app]({event['link']})" }
    ]

    return createEmbed(title=title, fields=fields, image=eventImageLink, thumbnail=KIDE_LOGO)

def getEventPrice(event):
    # stuff based on whether or not ticket sales have ended
    if event['salesEnded']:
        price = "**Myynti loppunut** :pensive:"
    elif len(event['maxPrice']) and len(event['minPrice']):
        price = f":ticket: {format(event['minPrice']['eur']/100,'.2f')}€ - {format(event['maxPrice']['eur']/100,'.2f')}€"
    else:
        price = ":ticket: Ilmaislippuja"

    # add ticket sale dates if tickets are still for sale
    if price != "**Myynti loppunut** :pensive:":
        # remove time from the timestamp to make the string a bit shorter
        price += f"\n(Lippuja myydään {toNormalTimeWithoutTime(event['dateSalesFrom'])} - {toNormalTimeWithoutTime(event['dateSalesUntil'])})"

    return price

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
            'eventImageLink': getEventImageLink(e['mediaFilename']),

            # convert timestamps from some wacky UTC format
            'dateSalesFrom': toNormalTime(fromWeirdTime(e['dateSalesFrom'])),
            'dateSalesUntil': toNormalTime(fromWeirdTime(e['dateSalesUntil'])),
            'dateActualFrom': toNormalTime(fromWeirdTime(e['dateActualFrom'])),
            'dateActualUntil': toNormalTime(fromWeirdTime(e['dateActualUntil'])),
            'datePublishFrom': fromWeirdTime(e['datePublishFrom'][0:19], format="%Y-%m-%dT%H:%M:%S"),
        }
        parsed_data.append(entry)
    return parsed_data
