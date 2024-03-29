import requests
import xmltodict

from bs4 import BeautifulSoup
from datetime import datetime
from dataclasses import dataclass, field
from dateutil.parser import parse

from utils import createEmbed, detailed_exc_msg

@dataclass
class Patch:
    """Dataclass used to parse necessary information from the raw data"""
    name: str
    publish_date: datetime
    link: str = field(repr=False)
    price: int = field(default=None, repr=False)
    image_link: str = field(default=None, repr=False)
    description: str = field(default=None, repr=False)

async def postNewPatches(client, channel_id, last_check_date) -> None:
    """Request a list of patches, re-format/parse the objects,
    filter recent ones, and post them on specified channel."""
    parsed_data = parse_data(request_patch_data()) # convert raw data from xml and create Patch objects
    new_patches = filter_new_patches(parsed_data, last_check_date) # compare pub date to last_check_date
    completed_patch_data = request_additional_data(new_patches) # get price etc.

    if len(completed_patch_data) > 0:
        print("New Patches!")
        # [print(patch) for patch in completed_patch_data]
        for patch in completed_patch_data:
            embed = create_patch_embed(patch)
            await client.get_channel(channel_id).send(embed=embed)

def request_patch_data() -> list:
    """Get patch data from URL and convert it from XML to python dictionary.
    Then navigate to the data needed before returning the list of patches."""
    try:
        r = requests.get('https://merkattu.fi/tuote-osasto/haalarimerkit/feed/')
        raw_data = xmltodict.parse(r.text)
        # navigate to the patch list
        raw_data = raw_data['rss']['channel']['item']
        return raw_data
    except Exception as e:
        print("Request status:", r.status_code)
        print(e)

def parse_data(raw_data: list) -> list:
    """Go through the patches in the list and create
    a list of dataclasses"""
    def create_patch_object(item):
        """Helper function for converting patches to dataclasses."""
        try:
            return Patch(
                name = item['title'],
                link = item['guid']['#text'],
                publish_date = parse(item['pubDate']).replace(tzinfo=None),
            )
        except Exception as e:
            detailed_exc_msg(e)

    # convert each patch from OrderedDict to normal dictionary
    raw_data = [dict(x) for x in raw_data]
    parsed_data = [create_patch_object(item) for item in raw_data]
    return parsed_data

def filter_new_patches(patch_data: list, last_check_date: datetime) -> list:
    """Return a list of patches published after given date.
    The date is loaded from the database and passed all the way from main.py."""
    new_patches = list(filter(lambda patch: patch.publish_date > last_check_date, patch_data))
    return new_patches

def request_additional_data(patch_data: list) -> list:
    """Request additional data such as price from the
    patches' individual store pages by using the link attribute.
    Uses BeautifulSoup to parse requested html."""
    def get_data(patch: Patch) -> Patch:
        try:
            r = requests.get(patch.link)
            soup = BeautifulSoup(r.text, 'html.parser')

            # get needed info
            price = soup.find('meta', attrs={'property': 'product:price:amount'})['content']
            image_link = soup.find('meta', attrs={'property': 'og:image'})['content']
            desc_elem_list = soup.select('#tab-description > .post-content > p')
            # get text from first element
            description = desc_elem_list[0].text

            # set needed info
            patch.price = price
            patch.image_link = image_link
            patch.description = description
            return patch

        except Exception as e:
            detailed_exc_msg(e)

    completed_patch_data = [get_data(patch) for patch in patch_data]
    return completed_patch_data

def create_patch_embed(patch: Patch):
    """Create fields etc. for the final embed message that will be sent on Discord."""
    title = patch.name
    price = patch.price
    web_link = patch.link
    image_link = patch.image_link
    description = patch.description

    fields = [
        { "name": "Hinta :label:",
            "value": f"{price} €" },
        { "name": "Kuvaus :page_facing_up:",
            "value": f"{description}" },
        { "name": "Linkki",
            "value": f"[Merkattu.fi]({web_link})" }
    ]

    MERKATTU_LOGO = 'https://merkattu.fi/wp-content/uploads/Favicon-64x64-1.png'
    return createEmbed(title=title, fields=fields, image=image_link, thumbnail=MERKATTU_LOGO)
