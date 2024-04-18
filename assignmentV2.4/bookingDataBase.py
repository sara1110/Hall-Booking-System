import utility as util
import datetime
import json

# BOOKING FORMAT
#   'booking ID'
#   'user'
#   'start' 
#   'end'
#   'hallID'
#   'date'   
#   'hallType'
#    HallTypes: 
#    - Auditorium : 1000pax , 300rm/h 
#    - Banquet hall: 300pax , 100rm/h
#    - Meeting room: 30pax , 50rm/h

BOOKINGDATA_FILEPATH = 'files/booking_data.txt'

BOOKING_ID = 'BookingID'
BOOKING_USER = 'User'
BOOKING_START = 'StartTime'
BOOKING_END = 'EndTime'
BOOKING_HALLID = 'HallID'
BOOKING_DATE = 'BookingDate'
BOOKING_PROPERTIES = [BOOKING_ID, BOOKING_USER, BOOKING_START, 
                      BOOKING_END, BOOKING_HALLID, BOOKING_DATE]

# Opening and closing time during the day
# (00:00hs to 23:59hs)
BOOKING_OPENINGTIME = 8
BOOKING_CLOSINGTIME = 18

ENTRYNOTFOUND = [{}, 0]

# These two variables need to 
# be serialized as well...
orphanIDs = []
lastID = 0
# Serialization filepath: 
METADATA_FILEPATH = "files/bookdbmeta.txt"

# Deserialize metadata
def loadMetadata():
    metadata = {}
    with open(METADATA_FILEPATH, "r") as file:
        lines = file.readlines()
        metadata = json.loads(lines[0])

    return metadata

# Serialize metadata
def saveMetadata():    
    metadata = {
        'orphanIDs' : orphanIDs,
        'lastID' : lastID
        }

    with open(METADATA_FILEPATH, "w") as file:
        json.dump(metadata, file)

def printBookingEntry(entry: dict):
    print(util.turnYellow(BOOKING_ID + ": ") + str(entry[BOOKING_ID]))
    print(util.turnYellow(BOOKING_USER + ": ") + str(entry[BOOKING_USER]))
    print(util.turnYellow(BOOKING_START + ": ") + str(entry[BOOKING_START]))
    print(util.turnYellow(BOOKING_END + ": ") + str(entry[BOOKING_END]))
    print(util.turnYellow(BOOKING_HALLID + ": ") + str(entry[BOOKING_HALLID]))
    print(util.turnYellow(BOOKING_DATE + ": ") + str(entry[BOOKING_DATE])+"\n")

def addBookingEntry(newBooking: dict, verbose: bool):
    keys = newBooking.keys()
    errorFlag = False
    for key in keys:
        if not (key in BOOKING_PROPERTIES):
            errorFlag = True
            break

    if(errorFlag): 
        if verbose:
            print(util.turnRed("Booking database: addBookingEntry(): invalid booking format provided"))
        return

    with open(BOOKINGDATA_FILEPATH, 'a') as file:
        json.dump(newBooking, file)
        file.write("\n")

    global lastID
    lastID = newBooking[BOOKING_ID]
    if(verbose):
        print(util.turnGreen("Booking Entry added succesfully"))
        print(util.turnYellow("Note: ") + "the booking will be automatically removed once its due")

def readBookingEntries() -> list:
    bookingStrings = [] 

    with open(BOOKINGDATA_FILEPATH, 'r') as file:
        bookingStrings = file.readlines()
    file.close()

    bookingList = [json.loads(bookingString) for bookingString in bookingStrings]
    return bookingList

def searchBookingEntry(bookingID: int) -> list:
    booking_entries = readBookingEntries()

    if booking_entries == []:
        return ENTRYNOTFOUND

    bookingFound = False
    entryIndex = 0
    for entry in booking_entries:
        if entry[BOOKING_ID] == bookingID: 
            bookingFound = True
            break
        else:
            entryIndex+=1

    if(bookingFound):
        # returns an array with the entry and its index
        return [booking_entries[entryIndex], entryIndex]
    else:
        return ENTRYNOTFOUND

def searchBookingEntryForUser(bookingID : int, username:str) -> list:
    booking_entries = readBookingEntries()

    if booking_entries == []:
        return ENTRYNOTFOUND

    bookingFound = False
    entryIndex = 0
    for entry in booking_entries:
        if(entry[BOOKING_USER] == username):
            if entry[BOOKING_ID] == bookingID: 
                bookingFound = True
                break
        else:
            entryIndex+=1

    if(bookingFound):
        # returns an array with the entry and its index
        return [booking_entries[entryIndex], entryIndex]
    else:
        return ENTRYNOTFOUND

# Returns True if the given time is taken for the given hall 
def isTimeBooked(t1: int, t2: int, hallID : int, date : str) -> bool:
    booking_entries = readBookingEntries()
    # Collission detection algorithm in one dimension
    # Applicable for time
    timeCollision = False
    for entry in booking_entries:
        if (int(entry[BOOKING_HALLID]) == hallID) and (entry[BOOKING_DATE] == date): 
            if (t1 >= int(entry[BOOKING_START]) and t1 <= int(entry[BOOKING_END])) or (
                t2 >= int(entry[BOOKING_START]) and t2 <= int(entry[BOOKING_END])): 
                timeCollision = True
                break    
    return timeCollision

# Returns True if the given time is taken for the given hall 
# Excludes the specific bookID provided
def isTimeBookedExcept(t1: int, t2: int, hallID : int, date : str, excludeID : int) -> bool:
    booking_entries = readBookingEntries()
    # Collission detection algorithm in one dimension
    # Applicable for time
    timeCollision = False
    for entry in booking_entries:
        if(int(entry[BOOKING_ID]) != excludeID):
            if (int(entry[BOOKING_HALLID]) == hallID) and (entry[BOOKING_DATE] == date): 
                if (t1 >= int(entry[BOOKING_START]) and t1 <= int(entry[BOOKING_END])) or (
                    t2 >= int(entry[BOOKING_START]) and t2 <= int(entry[BOOKING_END])): 
                    timeCollision = True
                    break    
    return timeCollision

def removeBookingEntry(bookingID: int, verbose: bool):
    booking_entries = readBookingEntries()

    entry = searchBookingEntry(bookingID)
    if(entry == ENTRYNOTFOUND):
        print(util.turnRed("Booking Database: removeBookingEntry(): Non registered booking entry!"))
        return

    else:
        booking_entries[entry[1]] = {}
        booking_entries.remove({})
            
        handle = open(BOOKINGDATA_FILEPATH, "w")
        handle.close()

        orphanIDs.append(bookingID)
        
        for entry in booking_entries:
            addBookingEntry(entry, False)

        if(verbose):
            print(util.turnGreen("Hall removed succesfully"))

def setBookingEntry(bookingID: int, newEntry: dict):
    booking_entries = readBookingEntries()

    if(booking_entries == []):
        print(util.turnRed("Booking Database: setBookingEntry(): No booking entries!"))
        return

    search = searchBookingEntry(bookingID)
    if(search == ENTRYNOTFOUND):
        print(util.turnRed("Booking Database: setBookingEntry(): bookingID doesnt exist !")) 
        return  
    
    #entry = search[0]
    booking_entries[search[1]] = newEntry

    handle = open(BOOKINGDATA_FILEPATH, "w")
    handle.close()

    for b in booking_entries:
        addBookingEntry(b, False)

def removeOutdatedBookings():
    entries = readBookingEntries()
    if entries == []: return

    todayDate = datetime.date.today()
    todayDate = util.force2Digits(todayDate.day) + util.force2Digits(todayDate.month) + str(todayDate.year) 
    #print(todayDate)
    for e in entries:
        if(util.dateMoreRecentThan(todayDate, str(e[BOOKING_DATE]))) == util.DATEMORERECENT:
            removeBookingEntry(e[BOOKING_ID], False)

def generateBookingID() -> int:    
    if len(orphanIDs) > 0:
        return orphanIDs.pop()
    else:
        outID = lastID + 1 

        # This loop iterates until the 
        # generated ID is not taken
        while searchBookingEntry(outID) != ENTRYNOTFOUND:
            outID+=1

        return outID


        

