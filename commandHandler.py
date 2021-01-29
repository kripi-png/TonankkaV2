import os, importlib

def loadCommands():
    print("Loading Commands...")
    # luo lista kaikkien komentojen nimistä.
    # x on komennon tiedoston nimi (ie. ping.py), joten x[0:-3] poistaa file-extensionin (.py)
    commandList = [x[0:-3] for x in os.listdir('commands') if x.endswith(".py") and not x.startswith('_')]
    commands = {}
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
