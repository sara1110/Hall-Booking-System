import utility as util
import json

# HALL ENTRY FORMAT
#    "hallID"
#    "HallName"
#    "description"
#    "pax"
#    "availability"
#    "dailyRate"

HALLID = "Hall ID"
HALLNAME = "Hall Name"
HALLDESCRIPTION = "Hall Description"
HALLPAX = "Hall Pax"
HALLAVAILABILITY = "Hall Availability"
HALLPRICERATE = "Hall Price"
HALLTYPE = "Hall Type"
# Possible values for Hall Type :
HALLTYPE_AUDITORIUM = "Auditorium"
HALLTYPE_BANQUET = "Banquet"
HALLTYPE_MEETING = "Meeting"
HALLTYPES = [HALLTYPE_AUDITORIUM, HALLTYPE_BANQUET, HALLTYPE_MEETING]

HALL_PROPERTIES = [HALLID, HALLNAME, HALLDESCRIPTION, HALLPAX, HALLAVAILABILITY, HALLPRICERATE, HALLTYPE]
HALLDATA_FILEPATH = "files/hall_data.txt"

ENTRYNOTFOUND = [{}, 0]

def printHallEntry(entry : dict):
    print(util.turnYellow("Hall ID : ") + str(entry[HALLID]))
    print(util.turnYellow("Hall Name : ") + str(entry[HALLNAME]))
    print(util.turnYellow("Hall Description : ") + str(entry[HALLDESCRIPTION]))
    print(util.turnYellow("Hall Pax : ") + str(entry[HALLPAX]))
    print(util.turnYellow("Hall Available : ") + str(entry[HALLAVAILABILITY]))
    print(util.turnYellow("Hall Price : ") + str(entry[HALLPRICERATE]))
    print(util.turnYellow("Hall Type : ") + str(entry[HALLTYPE])  + "\n")

def readHallEntries() -> list:
    
    hallStrings = []
    with open(HALLDATA_FILEPATH, 'r') as file:
        hallStrings = file.readlines()
    file.close()

    hallList = [json.loads(hallString) for hallString in hallStrings]

    return hallList

def addHallEntry(hall_dict: dict, verbose: bool):

    #first check if entry exists already

    keys = hall_dict.keys()
    errorFlag = False
    for key in keys:
        if not key in HALL_PROPERTIES:
                if verbose:
                    print("Error: user property " + key + "is not valid!")
                errorFlag = True
                break
    
    if(hall_dict[HALLTYPE]):
        if not hall_dict[HALLTYPE] in HALLTYPES:
            if verbose:
                print("Error: Invalid hall type!")
            errorFlag = True
    
    if errorFlag: return

    with open(HALLDATA_FILEPATH, 'a') as file:
         json.dump(hall_dict, file)
         file.write('\n')

    if(verbose):
         print(util.turnGreen("Hall added succesfully"))

# Searchs for a hall entry in its database
# Returns a list with the hall entry at i=0, and 
# the index of the entry at i=1.
# If the entry isnt found, returns ENTRYNOTFOUND 
def searchHallEntry(hallID: int):
    hall_entries = readHallEntries()

    hallFound = False
    
    hallEntryIndex = 0
    for entry in hall_entries:
        if entry[HALLID] == hallID:
            hallFound = True
            break
        else:
             hallEntryIndex+=1
    
    if(hallFound):
        # returns an array with the entry and its index
        return [hall_entries[hallEntryIndex], hallEntryIndex]
    else:
        return ENTRYNOTFOUND

def removeHallEntry(hallID: int, verbose: bool):
    hall_entries = readHallEntries()

    entry = searchHallEntry(hallID)
    
    if(entry[0] == {}):
        print("Hall database: removeHallEntry(): Non registered hall entry!")    
        return
    
    hall_entries[entry[1]] = {}
    hall_entries.remove({})

    handle = open(HALLDATA_FILEPATH, "w")
    handle.close()

    for entry in hall_entries:
        addHallEntry(entry, False)

    if verbose:
        print(util.turnGreen("Hall removed succesfully"))     

def setHallEntry(hallID: int, newEntry: dict, verbose : bool):
    hall_entries = readHallEntries()

    if(hall_entries == []):
        if verbose:
            print(util.turnRed(
                "Hall Databse: setHallEntry(): No hall entries!"))
        return

    entry = searchHallEntry(hallID)
    if(entry[0] == {}):
        if verbose: 
            print(util.turnRed(
                "Hall Database: setHallEntry(): No registered hall entry!"))
        return
    
        
    #if(entry[HALLTYPE]):
    if not (entry[HALLTYPE] in HALLTYPES):
        if verbose:
            print(util.turnRed("Hall Database: setHallEntry(): Invalid Hall Type!"))
        return

    hall_entries[entry[1]] = newEntry

    handle = open(HALLDATA_FILEPATH, "w")
    handle.close()

    for entry in hall_entries:
        addHallEntry(entry, False)

    if(verbose):
        print(util.turnGreen("Hall set successfully"))
    

