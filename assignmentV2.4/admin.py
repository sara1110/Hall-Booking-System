import hallDataBase as halldb
import bookingDataBase as bookdb
import userDataBase as userdb
import utility as util
import CLIelements as cli
import pseudoGraphics as psgfx

# Hardcoded Admin credentials
ADMINUSERNAME = "localadmin"
ADMINPASSWORD = "Cognos#1776"

def adminMenu(args):
    bookdb.removeOutdatedBookings()
    psgfx.printlocaladminLogo()

# args is provided as a simple list with
# the input from the MultipleInput at interface.py
# If the hall exists, overwrites the existing entry
# If not, it creates a new one
def addSetHallInfo(args: dict):
    if(len(args) != len(halldb.HALL_PROPERTIES)):
        return

    # Convert hallID to integer 
    args[0] = int(args[0])
    args[4] = bool(args[4])

    hallExists = halldb.searchHallEntry(args[0]) != halldb.ENTRYNOTFOUND

    # Create new entry dictionary
    newEntry = {
        halldb.HALLID : args[0],
        halldb.HALLNAME : args[1],
        halldb.HALLDESCRIPTION :args[2],
        halldb.HALLPAX : args[3],
        halldb.HALLAVAILABILITY : args[4],
        halldb.HALLPRICERATE : args[5],
        halldb.HALLTYPE : args[6]
    }

    if(hallExists):
        halldb.setHallEntry(newEntry[halldb.HALLID], newEntry, True)
    else:
        halldb.addHallEntry(newEntry, True)
    
    cli.okPrompt()

# noargs is just a placeholder
def showAllHalls(noargs):
    entries = halldb.readHallEntries()
    if(len(entries) == 0):
        print(util.turnRed("No halls registered..."))
    
    for entry in entries:
        if(entry[halldb.HALLTYPE] == halldb.HALLTYPE_AUDITORIUM):
            psgfx.printAuditorium()
        elif(entry[halldb.HALLTYPE] == halldb.HALLTYPE_BANQUET):
            psgfx.printBanquetHall()
        elif(entry[halldb.HALLTYPE] == halldb.HALLTYPE_MEETING):
            psgfx.printMeetingHall()

        halldb.printHallEntry(entry)

def searchHall(IDarg):  
    if(len(IDarg) != 1):
        return

    IDarg[0] = int(IDarg[0])

    searchOutput = halldb.searchHallEntry(IDarg[0])
    if(searchOutput != halldb.ENTRYNOTFOUND):
        print(util.turnGreen("Entry found:"))
        halldb.printHallEntry(searchOutput[0])
    else:
        print(util.turnRed("Entry not found ..."))    

    cli.okPrompt()

def deleteHall(IDarg):
    if(len(IDarg) != 2):
        print(len(IDarg))
        input("")
        return

    IDarg[0] = int(IDarg[0])

    halldb.removeHallEntry(IDarg[0], True)
    cli.okPrompt()

def addSetBooking(args):
    if(len(args) != len(bookdb.BOOKING_PROPERTIES)):
        return
    
    # Convert booking ID and user Id to int
    args[0] = int(args[0])
    args[2] = int(args[2])
    args[3] = int(args[3])
    args[4] = int(args[4])

    userErr = False
    hallIDErr = False
    dateFormatErr = False

    # Check that the provided user is registered
    userSearchOuput = userdb.searchUserEntry(args[1])
    if userSearchOuput == userdb.ENTRYNOTFOUND:
        print(util.turnRed("Error: User provided is not registered..."))
        userErr = True

    if halldb.searchHallEntry(args[4]) == halldb.ENTRYNOTFOUND:
        print(util.turnRed("Error: Chosen hall doesnt exist..."))
        hallIDErr = True

    args[5] = util.trimEdges(args[5])
    if not util.checkDate(args[5]):
        print(util.turnRed("Error: Date provided in the wrong format"))
        dateFormatErr = True

    if not (userErr or hallIDErr or dateFormatErr):
        # Create the new entry
        newEntry = {
            bookdb.BOOKING_ID : int(args[0]),
            bookdb.BOOKING_USER : args[1],
            bookdb.BOOKING_START : args[2],
            bookdb.BOOKING_END : args[3],
            bookdb.BOOKING_HALLID : int(args[4]),
            bookdb.BOOKING_DATE : args[5]
        }

        bookingSearchOutput = bookdb.searchBookingEntry(args[0])
        bookingExists = (bookingSearchOutput != bookdb.ENTRYNOTFOUND)

        if bookingExists:
            print(util.turnGreen("Booking set succesfully"))
            bookdb.setBookingEntry(newEntry[bookdb.BOOKING_ID], newEntry)
        else:
            # Check that the time slot selected is available
            if bookdb.isTimeBooked(args[2], args[3], args[0], args[5]):
                print(util.turnRed("Error: Chosen time slot collides with an existing booking"))
                #timeSlotErr = True
            else:
                print(util.turnGreen("Booking added successfully"))
                bookdb.addBookingEntry(newEntry, False)

    cli.okPrompt()

def searchBooking(IDarg):
    if(len(IDarg) != 1):
        print("searchBooking() : invalid input length")
        return

    IDarg[0] = int(IDarg[0])

    searchOutput = bookdb.searchBookingEntry(IDarg[0])  

    if(searchOutput != bookdb.ENTRYNOTFOUND):
        print(util.turnGreen("Booking found:"))
        bookdb.printBookingEntry(searchOutput[0])
    else:
        print(util.turnRed("Booking not found"))    

    cli.okPrompt()

def viewBookings(noargs):
    entries = bookdb.readBookingEntries()
    for e in entries:
        bookdb.printBookingEntry(e)
        #print("\n")

def deleteBooking(IDarg):
    if(len(IDarg) != 2):
        return
    
    if(IDarg[1] == "n"):
        return

    IDarg[0] = int(IDarg[0])

    bookdb.removeBookingEntry(IDarg[0], True)
    
    cli.okPrompt()

def viewUsers(noargs):

    userEntries = userdb.readUserEntries()
    if userEntries == []:
        print(util.turnRed("No users registered..."))
        return
    
    for user in userEntries:
        userdb.printUserEntry(user)
        print("------\n")

def searchUser(UsernameArg):
    if(len(UsernameArg) != 1):
        return
    #UsernameArg[0] = int(UsernameArg[0])

    searchOutput = userdb.searchUserEntry(UsernameArg[0])

    if searchOutput != userdb.ENTRYNOTFOUND:
        print(util.turnGreen("User found:"))
        userdb.printUserEntry(searchOutput[0])
    else:
        print(util.turnRed("User not found...."))

    cli.okPrompt()

def addSetUser(args):
    if len(args) != len(userdb.USERPROPERTIES):
        return
    
    newUserFlag = False
    searchOutput = userdb.searchUserEntry(args[0])   
    if searchOutput == userdb.ENTRYNOTFOUND:
        newUserFlag = True

    # Format checking
    dobFormatErr = not util.checkDate(args[4])    
    if dobFormatErr: print(util.turnRed("Wrong date of birth format"))

    contactFormatErr = not util.checkContactNumber(args[5])
    if contactFormatErr: print(util.turnRed("Wrong contact number format"))

    emailFormatErr = not util.checkEmail(args[6])
    if emailFormatErr: print(util.turnRed("Wrong email format"))

    #input(util.turnYellow("< OK >"))

    if not (contactFormatErr or dobFormatErr or emailFormatErr):
        
        # Create new user entry
        newEntry = {
            userdb.USERNAME : args[0],
            userdb.PASSWORD : args[1],
            userdb.FIRSTNAME : args[2],
            userdb.LASTNAME : args[3],
            userdb.DOB : args[4],
            userdb.CONTACTNO : args[5],
            userdb.EMAIL : args[6]
        }

        if(newUserFlag):
            userdb.addUserEntry(newEntry, True)
            #print(util.turnGreen("User registered sucessfully"))
        else:
            userdb.setUserEntry(newEntry[userdb.USERNAME], newEntry)
            print(util.turnGreen("User modified sucessfully"))

    cli.okPrompt()    

def deleteUser(UsernameArg):
    if len(UsernameArg) != 2:
        return
    
    userdb.removeUserEntry(UsernameArg[0], True)
    cli.okPrompt()



