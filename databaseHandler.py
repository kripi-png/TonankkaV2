import os
import json

def _getFile(name):
    """Get and return a file from the database directory called {name}"""
    return f"database/{name}.json"

def isTable(name):
    """Return True if there exists a file/table called {name}"""
    return os.path.exists(_getFile(name))

def createTable(name, overwrite=False):
    """
    Create a table/file called {name}. Create a folder called database if it doesn't exist.
    If file called {name} already exists, raise an Exception UNLESS {overwrite==True}
    """
    if not os.path.exists('database/'):
        os.mkdir('database')

    if os.path.exists(_getFile(name)) and not overwrite:
        raise(Exception(f"A database with name {name+'.json'} already exists. " + \
                        "If you wish to overwrite this database, " + \
                        "use 'overwrite=True' when calling the createTable function."))

    with open(_getFile(name), 'w') as outfile:
        json.dump({}, outfile)

def removeTable(name):
    """Removes a table/database called {name}. Raises an exception if no such file exists."""
    if not os.path.exists(_getFile(name)):
        raise(Exception(f"No database with name {name+'.json'} found."))
    os.remove(_getFile(name))

def readTable(name):
    """Open a file called {name}, parse it as json and return the data"""
    with open(_getFile(name), encoding='utf-8') as json_file:
        return json.load(json_file)

def writeTable(name, data):
    """Open a file called {name} and override everything with {data}"""
    with open(_getFile(name), 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4, default=str)
        outfile.close()

def eraseFromTable(name, key): # remove a key/value pair from a database
    data = readTable(name) # load the data into a temporary variable
    data.pop(key, None) # delete the key & value
    writeTable(name, data) # update the file with the edited data
