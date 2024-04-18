import json
import utility as util

# USER ENTRY FORMAT
#   'username'
#   'password'
#   'firstname'
#   'lastname'
#   'dob'
#   'contactNo'
#   'email'

USERNAME = 'username'
PASSWORD = 'password'
FIRSTNAME = 'firstname'
LASTNAME = 'lastname'
DOB = 'dob'
CONTACTNO = 'contactNo'
EMAIL = 'email'

USERPROPERTIES = [USERNAME, PASSWORD, FIRSTNAME, 
                  LASTNAME, DOB, CONTACTNO, EMAIL]

TEXTPATH = "files/user_data.txt"

TESTUSER1 = {
    USERNAME: 'sgd',
    PASSWORD: '1234',
    FIRSTNAME: 'Santiago',
    LASTNAME: 'Gallardo Dominguez',
    DOB: '09042003',
    CONTACTNO: '142191218',
    EMAIL: 'sagallardodom@gmail.com'
}

TESTUSER2 = {
    USERNAME: 'nnn',
    PASSWORD: '1234',
    FIRSTNAME: 'Nway',
    LASTNAME: 'Yupar Aung',
    DOB: '09042003',
    CONTACTNO: '142191218',
    EMAIL: 'nway@gmail.com'
}

ENTRYNOTFOUND = [{}, 0]

def printUserEntry(entry: dict):
    print(util.turnYellow(USERNAME + ": ") + str(entry[USERNAME]))
    print(util.turnYellow(PASSWORD + ": ") + str(entry[PASSWORD]))
    print(util.turnYellow(FIRSTNAME + ": ") + str(entry[FIRSTNAME]))
    print(util.turnYellow(LASTNAME + ": ") + str(entry[LASTNAME]))
    print(util.turnYellow(DOB + ": ") + str(entry[DOB]))
    print(util.turnYellow(CONTACTNO + ": ") + str(entry[CONTACTNO]))
    print(util.turnYellow(EMAIL + ": ") + str(entry[EMAIL]))

def addUserEntry(user_dict : dict, verbose: bool):
    if(searchUserEntry(user_dict[USERNAME]) != [{}, 0]):
        print("User Database: addUserEntry: Username already registered!")
        return

    keys = user_dict.keys()
    errorFlag = False
    for key in keys:
        if not key in USERPROPERTIES:
            #error
            print("Error: user property " + key + " is not valid!")
            errorFlag = True
            break

    if(errorFlag): return

    with open(TEXTPATH, 'a') as file:
        json.dump(user_dict, file)
        file.write("\n")

    if(verbose):
        print("User added succesfully")

def readUserEntries() -> list:
    userStrings = []
    with open(TEXTPATH, "r") as file:
        userStrings = file.readlines()
    file.close()

    userList = [json.loads(userString) for userString in userStrings]
    
    return userList

def searchUserEntry(username : str):
    user_entries = readUserEntries()

    userFound = False

    userEntryIndex = 0
    for user in user_entries:
        if user_entries[userEntryIndex][USERNAME] == username:
            userFound = True
            break
        else:
            userEntryIndex+=1
    
    if(userFound):
        # returns an array with the entry and its index
        return [user_entries[userEntryIndex], userEntryIndex]
    else:
        return ENTRYNOTFOUND

def setUserEntry(username : str, newEntry: dict):
    user_entries = readUserEntries()

    if(user_entries == []):
        print("User Database: setUserEntry(): No user entries!")
        return
    
    entry = searchUserEntry(username)
    if(entry[0] == {}):
        print("User Database: setUserEntry(): Non registered user entry!")
        return
    
    user_entries[entry[1]] = newEntry

    # These two lines clear the file content    
    handle = open(TEXTPATH, "w")
    handle.close()

    # Rewrite the content
    for entry in user_entries:
        addUserEntry(entry, False)

def removeUserEntry(username : str, verbose : bool):
    user_entries = readUserEntries()
    
    entry = searchUserEntry(username)

    if(entry[0] == {}):
        print("User Database: removeUserEntry(): Non registered user entry!")
        return
    
    user_entries[entry[1]] = {} 
    user_entries.remove({})

    # These two lines clear the file content    
    handle = open(TEXTPATH, "w")
    handle.close()
    
    # Rewrite the content
    for entry in user_entries:
        addUserEntry(entry, False)

    if verbose:
        print(util.turnGreen("User deleted successfully"))

