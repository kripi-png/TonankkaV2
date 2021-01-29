import os, importlib

commandList = [x[0:-3] for x in os.listdir('commands') if x.endswith(".py") and not x.startswith('_')] # luo lista kaikkien komentojen nimistä
commands = {}

def loadCommands():
    print("Loading Commands...")
    for com in commandList:
        commandData = importlib.import_module('commands.{0}'.format(com)).commandData
        commands[commandData['name']] = {
            "name": commandData['name'],
            "desc": commandData['description'],
            "execute": commandData['execute'],
            "author": commandData['author']
        }
    print("Loaded {} commands".format(len(commands)))
    return commands
