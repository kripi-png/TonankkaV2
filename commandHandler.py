import os, importlib

commandList = [x[0:-3] for x in os.listdir('commands') if x.endswith(".py") and not x.startswith('_')] # luo lista kaikkien komentojen nimistä
commands = {}

def loadCommands():
    for com in commandList:
        commands[com] = importlib.import_module('commands.{0}'.format(com)) # importtaa komentotiedosto ja aseta se commands-dictionaryyn
    return commands
