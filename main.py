import discord
import random

from datetime import datetime
from discord.ext import tasks
from timedEvents import haalarimerkit, tapahtumat

import settings
import botToken
import commandHandler
import databaseHandler as db
from utils import detailed_exc_msg

DEBUG_MODE = True

def get_last_check_date() -> datetime:
    """Get date of last event/patch check.
    Used to check for new events and patches."""
    raw_date = db.readTable('database')['lastEventLoopDateCheck']
    # remove milliseconds
    raw_date = raw_date.split('.')[0]
    return datetime.strptime(raw_date, '%Y-%m-%d %H:%M:%S')

async def change_bot_status() -> None:
    """Get the list of possible activities containing various games, songs etc.
    and set one of them as the status."""
    # get and select a status by random
    dbData = db.readTable('activities')
    selected_activity = random.choice(dbData)

    # all string items are games
    if type(selected_activity) is str:
        # create discord.Game activity type and set it as status
        game = discord.Game(selected_activity)
        await client.change_presence(activity=game)
    else:
        # all activities other than games have a type value
        # use that value to select corresponding activity type
        types = {
            'WATCHING': discord.ActivityType.watching,
            'LISTENING': discord.ActivityType.listening,
            'COMPETING': discord.ActivityType.competing,
        }
        activity = discord.Activity(
            type = types[selected_activity['type']],
            name = selected_activity["name"]
        )
        await client.change_presence(activity=activity)

@tasks.loop(hours=1.0)
async def timed_event_loop() -> None:
    """Function that is automatically ran every one hour. Contains
    calls for the patch and event systems and bot status/presence change."""
    print(f"[{datetime.strftime(datetime.now(), '%H:%M')}] Timed Events")
    await change_bot_status()
    try:
        if DEBUG_MODE:
            print(" >>>> Started in debug mode, posting on debug channel <<<<", end="\n\n")
            channel_id = settings.debugChannelID
        else:
            channel_id = settings.notificationChannelID

        check_date = get_last_check_date()
        channel_id = settings.debugChannelID
        await tapahtumat.postNewEvents(client, channel_id, check_date)
        await haalarimerkit.postNewPatches(client, channel_id, check_date)

    except Exception as e:
        detailed_exc_msg(e)

    finally:
        db.writeTable('database', {'lastEventLoopDateCheck': datetime.now()})

# ------- MAIN ---------
client = discord.Client()
commands = commandHandler.loadCommands()

# create database file if it does not exist
if not db.isTable('database'):
    db.createTable('database')
    db.writeTable('database', {'lastEventLoopDateCheck': datetime.now()})

@client.event
async def on_ready():
    """Function to be ran automatically once the bot has loaded and logged in."""
    print("Running Start Up tasks...")
    # start the event loop
    timed_event_loop.start()

    print("All done!")
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    """Function for handling new messages."""
    # prevent the bot from reacting to its own messages
    if message.author == client.user: return
    # ignore messages that do not start with the defined command prefix
    if not message.content.startswith(settings.commandPrefix): return

    # remove prefix and split command to arguments
    message.content = message.content[1:]
    args = message.content.split()

    # if the command is valid, run the execute function
    # located in the file of respective command
    if( args[0] in commands.keys() ):
        await commands[args[0]]['execute'](message, args, client,commands)

client.run(botToken.token)
