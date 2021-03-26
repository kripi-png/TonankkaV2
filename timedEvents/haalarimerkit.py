import requests
import xmltodict

from bs4 import BeautifulSoup
from utils import createEmbed
from datetime import datetime
from settings import engineerColor, notificationChannelID
from databaseHandler import *

def fromWeirdTime(n): return datetime.strptime(n,"%a, %d %b %Y %H:%M:%S")
def toNormalTime(n): return datetime.strftime(n, "%d.%m.%Y @ %H:%M")

def fromDatabaseTime(d): return datetime.strptime(d,"%Y-%m-%d %H:%M:%S")
def toDatabaseTime(d): return datetime.strftime(d,"%Y-%m-%d %H:%M:%S")

async def postNewPatches(client):
    data = parseData(await getRequestData())
    newPatchLinks = checkForNewPatches(data)
    if len(newPatches) > 0: print("New patches!")
    for link in newPatchLinks:
        # print(link)
        productData = await getProductDataByLink(link)
        embed = createProductEmbed(productData, link)
        await client.get_channel(notificationChannelID).send(embed=embed)
    dbSave()

async def getRequestData():
    r = requests.get('https://www.merkattu.fi/kauppa/feed/')
    patchData = xmltodict.parse(r.text) # XML -> dictionary
    patchData = patchData["rss"]["channel"]["item"] # go to actual data
    return patchData

def parseData(data):
    """create a new list of dictionaries of key-value pairs that are actually needed"""
    parsed_data = []
    for entry in data:
        _entry = {
            "link": "/".join(entry["link"].split("/")[0:5]),
            "pubDate": fromWeirdTime(entry["pubDate"].split(" +")[0]),
        }
        parsed_data.append(_entry)
    return parsed_data

def checkForNewPatches(data):
    newPatches = []
    lastDateChecked = dbRead()

    for patch in data:
        if lastDateChecked < patch["pubDate"]:
            newPatches.append(patch["link"])
    return newPatches

async def getProductDataByLink(link):
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
    title = productData["title"]
    desc = productData["desc"]
    price = productData["price"]
    image = productData["image"]
    stock = productData["stock"]

    return createEmbed(title=title, desc=f"**{price}**\n{desc}\n[__**Linkki**__]({link})", image=image, color=engineerColor)

def dbRead(): return fromDatabaseTime(readTable("haalarimerkit")["haalarimerkit"]["lastDateChecked"])
def dbSave():
    dbData = readTable("haalarimerkit")
    dbData["haalarimerkit"]["lastDateChecked"] = toDatabaseTime(datetime.now())
    writeTable("haalarimerkit", dbData)
