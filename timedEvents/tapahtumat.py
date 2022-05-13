import requests

from datetime import datetime
from dateutil.tz import tzoffset
from dateutil.parser import parse
from dataclasses import dataclass, field

from utils import createEmbed

KIDE_LOGO = "https://kide.app/content/images/themes/kide/favicon/launcher-icon-4x.png?v=020221"

@dataclass
class Event:
    """Dataclass for an event entry"""
    name: str
    company_name: str
    place: str
    price: tuple[int, int]
    availability: int
    id: str = field(repr=False)
    media_filename: str = field(repr=False)

    date_created: str = field(repr=False)
    date_publish_from: str = field(repr=True)

    date_sales_from: datetime = field(repr=False)
    date_sales_to: datetime = field(repr=False)
    date_event_from: datetime = field(repr=False)
    date_event_to: datetime = field(repr=False)

    sales_started: bool = field(repr=False)
    sales_ended: bool = field(repr=False)
    sales_ongoing: bool = field(repr=False)
    sales_paused: bool = field(repr=False)

def getEventImageLink(str):
    return 'https://portalvhdsp62n0yt356llm.blob.core.windows.net/bailataan-mediaitems/' + str;

async def create_event_object(event_data: dict) -> Event:
    """Create and return an Event object using data provided."""
    min_price = None
    max_price = None
    if 'eur' in event_data['minPrice']:
      min_price = event_data['minPrice']['eur']
    if 'eur' in event_data['maxPrice']:
      max_price = event_data['maxPrice']['eur']

    event_obj = Event(
        name = event_data['name'],
        company_name = event_data['companyName'],
        place = f"{event_data['place']}",
        price = (min_price, max_price),
        availability = event_data['availability'],
        media_filename = event_data['mediaFilename'],
        id = event_data['id'],

        date_created = parse(event_data['dateCreated']).replace(tzinfo=None),
        date_publish_from = parse(event_data['datePublishFrom']).replace(tzinfo=None),

        date_sales_from = parse(event_data['dateSalesFrom']).replace(tzinfo=None),
        date_sales_to = parse(event_data['dateSalesUntil']).replace(tzinfo=None),
        date_event_from = parse(event_data['dateActualFrom']).replace(tzinfo=None),
        date_event_to = parse(event_data['dateActualUntil']).replace(tzinfo=None),

        sales_started = event_data['salesStarted'],
        sales_ended = event_data['salesEnded'],
        sales_ongoing = event_data['salesOngoing'],
        sales_paused = event_data['salesPaused'],
    )
    return event_obj

async def get_new_events() -> list:
    """
    Request a list of all events, and then parse
    the events using Event dataclass to get rid of unnecessary info.
    Returns a list of Events."""
    r = requests.get('https://api.kide.app/api/products?city=Turku&productType=1')
    events_data = r.json()['model']

    events = []
    for event in events_data:
      event_obj = await create_event_object(event)
      events.append(event_obj)

    return events

def filter_recent_events(event_list: list, compared_date: datetime) -> list:
    """Return a list of events published after date given. Date is gotten from the database."""
    recent_events = list(filter(lambda event: event.date_publish_from > compared_date, event_list))
    return recent_events

def get_accurate_addresses(event_list: list) -> list:
    """Request more data by ID and concate more accurate address to the previous one."""
    new_event_list = []
    for event in event_list:
        r = requests.get('https://api.kide.app/api/products/' + event.id)
        additional_data = r.json()['model']

        city = additional_data['company']['city']
        street_address = additional_data['company']['streetAddress']

        event.place += f", {street_address}, {city}"

    return event_list

def format_price(event: Event) -> str:
    # default
    price = str(event.price)

    if event.sales_paused:
        price = "**Myynti on tauolla** :pause_button:"
    elif event.sales_ended:
        price = "**Myynti loppunut** :pensive:"
    else:
        if not event.price[0] or not event.price[1]:
            min_price, max_price = 0, 0
        else:
            min_price = format(event.price[0]/100,'.2f')
            max_price = format(event.price[1]/100,'.2f')

        if min_price == max_price:
            price = f":ticket: {min_price}€"
        else:
            price = f":ticket: {min_price}€ - {max_price}€"

    # add ticket sale dates if tickets are still for sale
    if not event.sales_ended:
        date = format_date(event)
        price += f"\n(Lippuja myydään {date})"

    return str(price)

def format_date(event: Event, date_format: str = '%d.%m.%Y, %H:%M') -> str:
    date = ""
    date_from = event.date_event_from
    date_to = event.date_event_to

    if date_from.date() == date_to.date():
        date = f"{date_from.strftime('%d.%m.%Y')} {date_from.strftime('%H:%M')} - {date_to.strftime('%H:%M')}"
    else:
        _date_from = datetime.strftime(date_from, date_format)
        _date_to = datetime.strftime(date_to, date_format)
        date = f"{_date_from} - {_date_to}"

    return date

def createEventEmbed(event: Event):
    title = event.name
    eventImageLink = getEventImageLink(event.media_filename)
    price = format_price(event)
    date = format_date(event)

    fields = [
        { "name": "Hinta",
            "value": f"{price}" },
        { "name": "Järjestäjä",
            "value": f"{event.company_name}",
            "inline": True },
        { "name": "Tapahtumapaikka",
            "value": f"{event.place}",
            "inline": True },
        { "name": "Päivämäärä",
            "value": f"{date}" },
        { "name": "Linkki",
            "value": f"[Kide.app]({'https://kide.app/fi/events/' + event.id})" }
    ]

    return createEmbed(title=title, fields=fields, image=eventImageLink, thumbnail=KIDE_LOGO)

async def postNewEvents(client, channel_id, compared_date: datetime) -> None:
    """
    Request a list of recently published events and, if there are any,
    generate and post an embed message on designated Discord channel.
    """
    event_list = await get_new_events()
    recent_events = filter_recent_events(event_list, compared_date)
    recent_events = get_accurate_addresses(recent_events)

    # [print(x) for x in recent_events]

    if len(recent_events) > 0:
        print("New Events!")
        for event in recent_events:
            embed = createEventEmbed(event)
            await client.get_channel(channel_id).send(embed=embed)
