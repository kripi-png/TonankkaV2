import requests
import xmltodict

from bs4 import BeautifulSoup
from utils import createEmbed
from datetime import datetime
from settings import engineerColor, notificationChannelID, debugChannelID
from databaseHandler import *

# TODO: rewrite this shit someday


# functions for converting time from one format to another
# fromRSSTime is for converting from the format used in the RSS feed
def fromRSSTime(n): return datetime.strptime(n,"%a, %d %b %Y %H:%M:%S")
# no clue what this does actually, it's not used anywhere
# it seems to have been used to convert the time to the format used in the embed message but I don't know
def toNormalTime(n): return datetime.strftime(n, "%d.%m.%Y @ %H:%M")
def fromDatabaseTime(d): return datetime.strptime(d,"%Y-%m-%d %H:%M:%S")

async def postNewPatches(client):
    """Get data, parse data, and post new patches on Discord as an embedded message"""
    data = parseData(await getRequestData())
    newPatchLinks = checkForNewPatches(data)
    if len(newPatchLinks) > 0:
        print("New patches!")
        for link in newPatchLinks:
            productData = await getProductDataByLink(link)
            print(f"DEBUG>> {productData['title']}      {productData['image']}")
            embed = createProductEmbed(productData, link)
            await client.get_channel(notificationChannelID).send(embed=embed)

async def getRequestData():
    """Get and return the RSS feed of the recent patches"""
    r = requests.get('https://www.merkattu.fi/tuote-osasto/haalarimerkit/feed/')
    patchData = xmltodict.parse(r.text) # XML -> dictionary
    patchData = patchData["rss"]["channel"]["item"] # go to actual data
    return patchData

def parseData(data):
    """create a new list of dictionaries of key-value pairs that are actually needed"""
    parsed_data = []
    for entry in data:
        _entry = {
            "link": "/".join(entry["link"].split("/")[0:5]), # remove the query string
            "pubDate": fromRSSTime(entry["pubDate"].split(" +")[0]), # remove the +0000 suffix thingy and everything after it
        }
        parsed_data.append(_entry)
    return parsed_data

def checkForNewPatches(data):
    """
    Compare the publishing date of a patch to the lastDateChecked date
    If a new patch is found, add it to a list and return the list
    """
    newPatches = []
    lastDateChecked = dbRead()

    for patch in data:
        if lastDateChecked < patch["pubDate"]:
            newPatches.append(patch["link"])
    return newPatches

async def getProductDataByLink(link):
    """"Use BeautifulSoup to yoink, parse and return some data (eg. price, stock, image) from the actual product site of a patch"""
    r = requests.get(link).text
    soup = BeautifulSoup(r, "html.parser")

    title = soup.find("h1", {"class": "product_title"}).get_text()
    image = soup.find("meta", property="og:image").get("content")
    price = soup.find("div", {"class": "summary-container"}).find("bdi").get_text()
    stock = soup.find("p", {"class": "stock"}).get_text()
    description = soup.find("div", {"class": "woocommerce-product-details__short-description"}).find("p").get_text()

    return {
        "title": title,
        "desc": description,
        "image": image,
        "price": price,
        "stock": stock
    }

def createProductEmbed(productData, link):
    """Create and return a Embed message which is then sent on Discord"""
    title = productData["title"]
    desc = productData["desc"]
    price = productData["price"]
    image = productData["image"]
    stock = productData["stock"]

    return createEmbed(title=title, desc=f"**{price}**\n{desc}\n[__**Linkki**__]({link})", image=image, color=engineerColor)

def dbRead():
    """Get lastDateChecked date from the database"""
    return fromDatabaseTime(readTable("database")["lastEventLoopDateCheck"])
