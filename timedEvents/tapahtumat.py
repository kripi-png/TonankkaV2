import requests
from datetime import datetime
from utils import createEmbed
from databaseHandler import *
from settings import engineerColor, notificationChannelID, debugChannelID

KIDE_LOGO = "https://kide.app/content/images/themes/kide/favicon/launcher-icon-4x.png?v=020221"

def getEventImageLink(str): return "https://portalvhdsp62n0yt356llm.blob.core.windows.net/bailataan-mediaitems/" + str;
def fromFeedTimeformat(n,format="%Y-%m-%dT%H:%M:%S%z"): return datetime.strptime(n, format)
def toEmbedTimeformat(n): return datetime.strftime(n, "%d.%m.%Y @ %H:%M")
def fromEmbedtimeformat(n): return datetime.strptime(n, "%d.%m.%Y @ %H:%M")
def toEmbedTimeformatWithoutTime(n): return datetime.strftime(fromEmbedtimeformat(n), "%d.%m.%Y")
def fromDatabaseTimeformat(d): return datetime.strptime(d,"%Y-%m-%d %H:%M:%S")

def isNewer(date):
    """Compares 'date' and the date saved in the database, returns true if database time was before"""
    return fromDatabaseTimeformat(readTable("database")["lastEventLoopDateCheck"]) < date

async def postNewEvents(client):
    """
    Get a list of all currently listed events, remove unnecessary data from them,
    check if any of them are new (as in yet to be posted on the Discord channel),
    create embed messages of them and then post the message
    """
    r = requests.get("https://api.kide.app/api/products?city=Turku&productType=1")
    data = r.json()["model"] # where the actual data is
    parsed_data = parseData(data) # remove unnecessary stuff and convert timestamps
    new_events = checkForNewEvents(parsed_data)
    if len(new_events) > 0:
        print("New Events!")
        for x in parsed_data:
            embed = createEventEmbed(x)
            await client.get_channel(debugChannelID).send(embed=embed)

def checkForNewEvents(events):
    """"""
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
        price += f"\n(Lippuja myydään {toEmbedTimeformatWithoutTime(event['dateSalesFrom'])} - {toEmbedTimeformatWithoutTime(event['dateSalesUntil'])})"

    return price

def parseData(data):
    """For each event, create a new dictionary with only required information in it,
    make a list of them and return the list"""
    parsed_data = []
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
            'dateSalesFrom': toEmbedTimeformat(fromFeedTimeformat(e['dateSalesFrom'])),
            'dateSalesUntil': toEmbedTimeformat(fromFeedTimeformat(e['dateSalesUntil'])),
            'dateActualFrom': toEmbedTimeformat(fromFeedTimeformat(e['dateActualFrom'])),
            'dateActualUntil': toEmbedTimeformat(fromFeedTimeformat(e['dateActualUntil'])),
            'datePublishFrom': fromFeedTimeformat(e['datePublishFrom'][0:19], format="%Y-%m-%dT%H:%M:%S"),
        }
        parsed_data.append(entry)
    return parsed_data
