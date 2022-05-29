import requests

from datetime import datetime
from dateutil.tz import tzoffset
from dataclasses import dataclass, field
from dateutil.parser import parse

from utils import createEmbed, detailed_exc_msg

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

    def format_date(self, date_format: str = '%d.%m.%Y, %H:%M') -> str:
        """Format and return date depending on whether
        the event is a single day event.

        Method is automatically called and set to date_string property
        when an instance is created, but it can also be called separately
        with optional date_format string as an argument.
        """
        date_from = self.date_event_from
        date_to = self.date_event_to

        # if the event is a single day event, the format is:
        # 25.05.2022, 17:30 - 18:30
        if date_from.date() == date_to.date():
            date = f"{date_from.strftime('%d.%m.%Y')}, {date_from.strftime('%H:%M')} - {date_to.strftime('%H:%M')}"
        # otherwise go with
        # 19.05.2022, 17:00 - 20.05.2022, 02:00
        else:
            _date_from = datetime.strftime(date_from, date_format)
            _date_to = datetime.strftime(date_to, date_format)
            date = f"{_date_from} - {_date_to}"

        return date

    date_string = property(format_date)

    @property
    def price_string(self) -> str:
        """Format price in different ways depeding on various conditions such as
        whether the event is free, if the sales have ended etc.
        """
        # default
        price_str = str(event.price)

        if event.sales_paused:
            price_str = "**Myynti on tauolla** :pause_button:"
        elif event.sales_ended:
            price_str = "**Myynti on loppunut** :pensive:"
        else:
            if not event.price[0] or not event.price[1]:
                min_price, max_price = 0, 0
            else:
                min_price = format(event.price[0]/100,'.2f')
                max_price = format(event.price[1]/100,'.2f')

            if min_price == max_price:
                price_str = f":ticket: {min_price}€"
            else:
                price_str = f":ticket: {min_price}€ - {max_price}€"

        # add ticket sale dates if tickets are still for sale
        if not event.sales_ended:
            date = format_date(event)
            price_str += f"\n(Lippuja myydään {date})"

        return price_str

async def postNewEvents(client, channel_id: int, last_check_date: datetime) -> None:
    """Request a list of recently published events and, if there are any,
    generate and post an embed message on designated Discord channel."""
    parsed_data = parse_data(get_event_data())
    new_events_data = filter_new_events(parsed_data, last_check_date)
    completed_events_data = get_accurate_addresses(new_events_data)

    if len(completed_events_data) > 0:
        print("New Events!")
        [print(event) for event in completed_events_data]
        for event in completed_events_data:
            embed = create_event_embed(event)
            await client.get_channel(channel_id).send(embed=embed)

def get_event_data() -> list:
    """Request a list of all events."""
    try:
        r = requests.get('https://api.kide.app/api/products?city=Turku&productType=1')
        events_data = r.json()['model']
        return events_data
    except Exception as e:
        print(f"{r.status_code=}")
        detailed_exc_msg(e)

def parse_data(raw_data: list) -> list:
    """Go through the raw data and create a list of Event objects."""
    def create_event_object(event_data: dict) -> Event:
        """Create and return an Event object using data provided."""
        _miprice = event_data['minPrice']
        _maprice = event_data['maxPrice']

        min_price = _miprice['eur'] if 'eur' in _miprice else None
        max_price = _maprice['eur'] if 'eur' in _maprice else None
        try:
            return Event(
                name = event_data['name'],
                company_name = event_data['companyName'],
                place = event_data['place'],
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
        except KeyError as e:
            print(f"Error while parsing event: {event_data['name']}")
            print(f"KeyError: {e=}")
        except Exception as e:
            print(f"Error while parsing event: {event_data['name']}")
            detailed_exc_msg(e)

    parsed_data = [create_event_object(event) for event in raw_data]
    return parsed_data

def filter_new_events(event_list: list, last_check_date: datetime) -> list:
    """Return a list of events published after date given. Date is gotten from the database."""
    new_events = list(filter(lambda event: event.date_publish_from > last_check_date, event_list))
    return new_events

def get_accurate_addresses(event_list: list) -> list:
    """Request more data by ID and concate more accurate address to the previous one."""
    def request_additional_data(event):
        r = requests.get(f'https://api.kide.app/api/products/{event.id}')
        data = r.json()['model']
        city = data['company']['city']
        street_address = data['company']['streetAddress']

        event.place += f", {street_address}, {city}"
        return event

    new_event_list = [request_additional_data(event) for event in event_list]
    return event_list

def create_event_embed(event: Event):
    """Create fields etc. for the final embed message that will be sent on Discord."""
    title = event.name
    eventImageLink = f'https://portalvhdsp62n0yt356llm.blob.core.windows.net/bailataan-mediaitems/{event.media_filename}'
    fields = [
        { "name": "Hinta",
            "value": f"{event.price_string}" },
        { "name": "Järjestäjä",
            "value": f"{event.company_name}",
            "inline": True },
        { "name": "Tapahtumapaikka",
            "value": f"{event.place}",
            "inline": True },
        { "name": "Päivämäärä",
            "value": f"{event.date_string}" },
        { "name": "Linkki",
            "value": f"[Kide.app]({'https://kide.app/fi/events/' + event.id})" }
    ]

    KIDE_LOGO = "https://kide.app/content/images/themes/kide/favicon/launcher-icon-4x.png?v=020221"
    return createEmbed(title=title, fields=fields, image=eventImageLink, thumbnail=KIDE_LOGO)
