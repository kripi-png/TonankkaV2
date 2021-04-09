import json, os

def getFile(name): return "database/{}.json".format(name) # for this file only
def isTable(name): return os.path.exists(getFile(name)) # check if a table with given name already exists

def createTable(name, overwrite=False):
    if not os.path.exists('database/'): os.mkdir('database') # if database folder does not exist, create one
    # if file with the same name already exists and user has not specified
    # whether or not they wish to overwrite the file, raise an error
    if os.path.exists(getFile(name)) and not overwrite:
        raise(Exception("A database with name {} already exists. ".format(name+'.json') + \
                        "If you wish to overwrite this database, " + \
                        "add 'overwrite=True' into the createTable-function as an argument."))

    # create a database file and enter {}; an empty json-file
    with open(getFile(name), 'w') as outfile:
        json.dump({}, outfile)

def removeTable(name):
    if not os.path.exists(getFile(name)): # fails if there's no databases with given name
        raise(Exception("No database with name {} found.".format(name+'.json')))
    os.remove(getFile(name)) # delete the database file

def readTable(name): # returns all the data from the file
    with open(getFile(name), encoding='utf-8') as json_file:
        return json.load(json_file)

def writeTable(name, data):
    with open(getFile(name), 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)
        outfile.close()

def eraseFromTable(name, key): # remove a key/value pair from a database
    data = readTable(name) # load the data into a temporary variable
    data.pop(key, None) # delete the key & value
    writeTable(name, data) # update the file with the edited data
