import hallDataBase as halldb
import bookingDataBase as bookdb
import userDataBase as userdb
import utility as util
import pseudoGraphics as psgfx
from datetime import date
import CLIelements as cli 

# Once logged in, the credentials
# of the user are stored here
currentLoggedUser = {}

def userMenuInterface(noargs):
    bookdb.removeOutdatedBookings()
    psgfx.printUserLogo()
    print("Welcome, " + util.turnYellow(currentLoggedUser[userdb.USERNAME]))

def userRegister(args):

    if(len(args) != len(userdb.USERPROPERTIES)):
        return cli.STATEFUNCTIONFAIL

    # Check information format
    DoBerr = not util.checkDate(args[4])
    if DoBerr: print(util.turnRed("Wrong date of birth format"))
    
    ContactErr = not util.checkContactNumber(args[5])
    if ContactErr: print(util.turnRed("Wrong contact number format"))

    EmailErr = not util.checkEmail(args[6])
    if EmailErr: print(util.turnRed("Wrong email format"))

    if not (DoBerr or ContactErr or EmailErr):

        newEntry = {
            userdb.USERNAME : args[0],
            userdb.PASSWORD : args[1],
            userdb.FIRSTNAME : args[2],
            userdb.LASTNAME : args[3],
            userdb.DOB : args[4],
            userdb.CONTACTNO : args[5],
            userdb.EMAIL : args[6]
        }

        userdb.addUserEntry(newEntry, True)
    cli.okPrompt()

def userLogin(args):
    if len(args) != 2:
        return cli.STATEFUNCTIONFAIL

    searchResult = userdb.searchUserEntry(args[0])
    userFound = searchResult != userdb.ENTRYNOTFOUND
    correct_password = 0

    if userFound:
        correct_password = searchResult[0][userdb.PASSWORD]
  
    if not userFound:
        print(util.turnRed("User is not registered!"))
        cli.okPrompt()        
        return cli.STATEFUNCTIONFAIL
    else:
        if args[1] == correct_password:
            global currentLoggedUser
            currentLoggedUser = searchResult[0] # Store the logged user here
            print(util.turnGreen("Login sucessful")) 
            cli.okPrompt()
            return cli.STATEFUNCTIONSUCESS
        else:
            print(util.turnRed("Wrong password"))
            cli.okPrompt()
            return cli.STATEFUNCTIONFAIL

def displayDateSchedule(args:list):
    if(len(args) != 2):
        return cli.STATEFUNCTIONFAIL

    hallID = int(args[0])
    inDate = args[1]

    if (inDate != "TODAY") and (not util.checkDate(inDate)):
        print(util.turnRed("Error: invalid date provided!"))

    todayDate = ''
    if inDate == "TODAY":
        todayDate = date.today()
        print(util.turnYellow("Today's Date : ") + str(todayDate.day) 
            + util.turnYellow("/") + str(todayDate.month) 
            + util.turnYellow("/") + str(todayDate.year))

        todayDate = str(todayDate.day)+str(todayDate.month)+str(todayDate.year)
    else:
        outInDate = inDate[0] + inDate[1] + util.turnYellow("/") 
        outInDate+= inDate[2] + inDate[3] + util.turnYellow("/")
        outInDate+= inDate[4] + inDate[5] + inDate[6] + inDate[7]

        print(util.turnYellow("Date : ") + outInDate)

    # Each time slot is of 30 minutes, represented as 0.5 hours
    timeSlots = []
    slotAvailables = [] # booleans for each slot (True = free, False = taken)
    slotCounter = bookdb.BOOKING_OPENINGTIME
    while slotCounter < bookdb.BOOKING_CLOSINGTIME:
        timeSlots.append(slotCounter)
        slotAvailables.append(True) 
        slotCounter += 0.5
    
    # Now iterate each slot through the existing entries to check collision
    i = 0
    for slot in timeSlots:
        if(inDate == "TODAY"):
            if bookdb.isTimeBooked(slot, slot, hallID, todayDate):    
                slotAvailables[i] = False # slot is taken
        else:
            if bookdb.isTimeBooked(slot, slot, hallID, inDate):    
                slotAvailables[i] = False # slot is taken
        i+=1    
    
    # Finally print the daily schedule for the hall
    availableStr = ""
    for i in range(0, len(timeSlots)):
        if(slotAvailables[i]):
            availableStr = util.turnGreen("Available")
        else:
            availableStr = util.turnRed("Taken")

        print(str(util.decimalHourToSexagesimal(timeSlots[i])) + "\t: " + str(availableStr))

    cli.okPrompt()

def viewAvailableHalls(noargs):

    entries = halldb.readHallEntries()

    counter = 0
    for h in entries:
        if (bool(h[halldb.HALLAVAILABILITY])):

            hallType = h[halldb.HALLTYPE]
            # Print pseudographic according to its type
            if(hallType == halldb.HALLTYPE_AUDITORIUM):
                psgfx.printAuditorium()
            if(hallType == halldb.HALLTYPE_BANQUET):
                psgfx.printBanquetHall()
            if(hallType == halldb.HALLTYPE_MEETING):
                psgfx.printMeetingHall()

            halldb.printHallEntry(h)
            counter+=1

    if(counter == 0):
        print(util.turnRed("No available halls in this moment..."))

# - User should not enter 'bookingID'
# This will be generated automatically
# according to the existant bookings
# - User shouldnt enter his username since
# its already logged in
def makeBooking(args):

    if(len(args) != len(bookdb.BOOKING_PROPERTIES)):
        return cli.STATEFUNCTIONFAIL

    hallIDerr = False

    # Use this in case the hall availability is False
    hallCurrNotAvailable = False

    invalidTimeErr = False
    takenSlotErr = False
    dateFormatErr = False
        
    start = int(args[0])
    end = int(args[1])
    hallID = int(args[2])
    indate = args[3]

    hallSearchData = halldb.searchHallEntry(hallID) 
    hallData = hallSearchData[0] 

    if(hallSearchData == halldb.ENTRYNOTFOUND):
        hallIDerr = True
        print(util.turnRed("hallID does not exist!"))        

    if(start < bookdb.BOOKING_OPENINGTIME 
       or end > bookdb.BOOKING_CLOSINGTIME):
        invalidTimeErr = True
        print(util.turnRed("Given time is outside of working hours!"))        

    if(bookdb.isTimeBooked(start, end, hallID, indate)):
        takenSlotErr = True
        print(util.turnRed("Given time clashes with another booking!"))

    if(not util.checkDate(indate)):
        dateFormatErr = True
        print(util.turnRed("Wrong date format. Please use the DDMMYYYY format."))

    if not (hallIDerr or hallCurrNotAvailable or invalidTimeErr 
       or takenSlotErr or dateFormatErr):
        
        newID = bookdb.generateBookingID() 

        newBooking = {
            bookdb.BOOKING_ID : newID,
            bookdb.BOOKING_USER : currentLoggedUser[userdb.USERNAME],
            bookdb.BOOKING_START : start,
            bookdb.BOOKING_END : end, 
            bookdb.BOOKING_HALLID : hallID,
            bookdb.BOOKING_DATE : indate
        }

        bookdb.addBookingEntry(newBooking, True)

        hallRate = int(hallData[halldb.HALLPRICERATE])
        bookingPrice = (end-start) * hallRate
        print(util.turnYellow("The price of your booking: ") + "RM" + str(bookingPrice) )

        cli.okPrompt()

        return cli.STATEFUNCTIONSUCESS
    else:
        cli.okPrompt()
        return cli.STATEFUNCTIONFAIL
    
def viewBookings(noargs):

    allBookings = bookdb.readBookingEntries()
    thisUserBookings = []

    # Search all bookings that are from the
    # currentLoggedUser
    for b in allBookings:
        if(b[bookdb.BOOKING_USER] == currentLoggedUser[userdb.USERNAME]):
            thisUserBookings.append(b)

    # Print all of these
    if len(thisUserBookings) > 0:
        for ub in thisUserBookings:
            bookdb.printBookingEntry(ub)
    else:
        print(util.turnRed("No bookings yet !"))

# Technically the two main properties
# to edit in a booking are the start and end time
# For other cases, just delete the existing booking
# and create a new one
def editBooking(args):

    if(len(args) != 3):
        return cli.STATEFUNCTIONFAIL

    bookID = int(args[0])
    newStart = int(args[1])
    newEnd = int(args[2])

    searchOutput = bookdb.searchBookingEntry(bookID)
    prevBooking = searchOutput[0]

    if searchOutput == bookdb.ENTRYNOTFOUND:
        print(util.turnRed("Booking ID doesnt exist..."))
    else:
        # Calculate the timing difference, this is, the additional timing
        # that needs to be allocated. If the difference is negative,
        # then there is no problem with allocation since the time slot
        # is "shrinking", just set it to the new start/end
        startDiff = prevBooking[bookdb.BOOKING_START] - newStart
        if startDiff < 0:
            startDiff = newStart
        endDiff = newEnd - prevBooking[bookdb.BOOKING_END]
        if endDiff < 0:
            endDiff = newEnd

        # Check that the new timing doesnt collide 
        # with another boooking
        # The existing booking is excluded from the search
        if bookdb.isTimeBookedExcept(startDiff, endDiff, 
                               prevBooking[bookdb.BOOKING_HALLID],
                               prevBooking[bookdb.BOOKING_DATE],
                               bookID):
            print(util.turnRed("New timing clashes with another booking!"))                 
        
        else:
            newBooking = {
                bookdb.BOOKING_ID : bookID,
                bookdb.BOOKING_USER : currentLoggedUser[userdb.USERNAME],
                bookdb.BOOKING_START : newStart,
                bookdb.BOOKING_END : newEnd,
                bookdb.BOOKING_HALLID : prevBooking[bookdb.BOOKING_HALLID],
                bookdb.BOOKING_DATE : prevBooking[bookdb.BOOKING_DATE]  
            }

            bookdb.setBookingEntry(bookID ,newBooking)
            print(util.turnGreen("Booking edited successfully"))
    cli.okPrompt()

def cancelBooking(args):

    if(len(args) != 2):
        return

    if(args[1]) == "n":
        return

    bookID = int(args[0])
    
    if bookdb.searchBookingEntry(bookID) == bookdb.ENTRYNOTFOUND:
        print(util.turnRed("Booking ID doesnt exist!"))
    else:
        bookdb.removeBookingEntry(bookID, True)

    cli.okPrompt()

def searchBooking(args):
    if(len(args) != 1):
        return

    if(args[0] == cli.DEFAULTSCAPESEQ):
        return
    
    bookID = int(args[0])

    searchOutput = bookdb.searchBookingEntryForUser(bookID, currentLoggedUser[userdb.USERNAME])

    if(searchOutput != bookdb.ENTRYNOTFOUND):
        print(util.turnYellow("Booking found:"))
        bookdb.printBookingEntry(searchOutput[0])
    else:
        print(util.turnRed("Booking not found..."))
        pass

    cli.okPrompt()

def showProfile(noargs):   
    psgfx.printUserLogo() 
    print(util.turnYellow("Username: ") + currentLoggedUser[userdb.USERNAME])
    print(util.turnYellow("First name: ") + currentLoggedUser[userdb.FIRSTNAME])
    print(util.turnYellow("Last name(s): ") + currentLoggedUser[userdb.LASTNAME])
    print(util.turnYellow("Date of birth: ") + currentLoggedUser[userdb.DOB])
    print(util.turnYellow("Contact number: ") + currentLoggedUser[userdb.CONTACTNO])
    print(util.turnYellow("E-mail: ") + currentLoggedUser[userdb.EMAIL])
    pass

def editProfile(args):
    
    if(len(args) != len(userdb.USERPROPERTIES)): 
        return

    usernameChanged = False

    newVars = []

    global currentLoggedUser
    # If input == "PASS", just assign the previous value
    for i in range(0, len(userdb.USERPROPERTIES)):
        if args[i] == "PASS":
            newVars.append(currentLoggedUser[userdb.USERPROPERTIES[i]])
            pass
        else:
            if(i == 0):
                usernameChanged = True
            newVars.append(args[i])
            pass

    inUsername = newVars[0] 
    inPassword = newVars[1]
    inFirstName = newVars[2]
    inLastName = newVars[3]
    inDoB = newVars[4]
    inContact = newVars[5]
    inEmail = newVars[6]
    
    userErr = False
    passwErr = False
    DoBerr = False
    contactErr = False
    emailErr = False

    # Check if new username is taken
    if(usernameChanged):
        searchOutput = userdb.searchUserEntry(inUsername)
        if searchOutput != userdb.ENTRYNOTFOUND:
            userErr = True 
            print(util.turnRed("Username is taken already !"))

    if len(inPassword) == 0:
        print(util.turnRed("Incorrect password format"))     
        passwErr = True

    if not util.checkDate(inDoB):
        print(util.turnRed("Incorrect Date of Birth format"))
        DoBerr = True

    if not util.checkContactNumber(inContact):
        print(util.turnRed("Incorrect contact number format"))
        contactErr = True

    if not util.checkEmail(inEmail):
        print(util.turnRed("Incorrect e-mail format"))
        emailErr = True

    if not (userErr or passwErr or DoBerr 
            or contactErr or emailErr):

        newProfile = {
            userdb.USERNAME : inUsername,
            userdb.PASSWORD : inPassword,
            userdb.FIRSTNAME : inFirstName,
            userdb.LASTNAME : inLastName,
            userdb.DOB : inDoB,
            userdb.CONTACTNO : inContact,
            userdb.EMAIL : inEmail
        }

        userdb.setUserEntry(currentLoggedUser[userdb.USERNAME], newProfile)

        # Update currentLoggedUser
        updateSearch = userdb.searchUserEntry(inUsername)
        if(updateSearch != userdb.ENTRYNOTFOUND):
            print(util.turnGreen("User profile successfully edited"))
            currentLoggedUser = updateSearch[0]
        else:
            print(util.turnRed("Something went wrong..."))

    cli.okPrompt()