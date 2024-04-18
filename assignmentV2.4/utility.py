import os
from sys import platform
import errorlog
import math

#============ ANSI Terminal utilities ==============#

def printRed(txt : str):
    print("\033[31m" + txt + "\033[m")

def printGreen(txt : str):
    print("\033[32m" + txt + "\033[m")

def printYellow(txt : str):
    print("\033[33m" + txt + "\033[m")

def turnRed(txt : str) -> str:
    return "\033[31m" + txt + "\033[m"

def turnGreen(txt : str) -> str:
    return "\033[32m" + txt + "\033[m"

def turnYellow(txt : str) -> str:
    return "\033[33m" + txt + "\033[m"

def clearScr():
    # Windows (CMD / Powershell)
    if platform == "win32":
        os.system("cls")
    # OS X or Linux (Unix based)
    elif platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system("clear")

#========================================================#

#=============== String/list utilities ==================#

# Removes the white space from a string    
def trimStr(s : str) -> str:
    output = ""
    for char in s:
        if(char != ' '):
            output+=char
        
    return output

def trimEdges(s : str) -> str:
    output = ""

    # The first char that is not whitespace
    startIndex = 0
    # The last char that is not whitespace
    endIndex = 0

    # First loop: frontwards
    # Get startIndex
    counter = 0
    while(True):
        if(s[counter] != ' '):
            startIndex = counter
            break    
        if(counter == len(s)-1):
            break
        else:
            counter+=1

    # Second loop: backwards
    # Get endIndex
    counter = len(s)-1
    while(True):
        if(s[counter] != counter):
            endIndex = counter
            break
        if(counter == 0):
            break
        else:
            counter-=1

    sliceobj = slice(startIndex, endIndex+1)
    output = s[sliceobj]
    return output

# Returns True if a list is of a given type
def isListType(lst : list, t : type) -> bool:
    isType = True
    for item in lst:
        if type(item) != t:
            isType = False
            break

    return isType

#==========================================================#

#========== Data format conversion/validation =============# 

# Set of special chars used for data validation
SPECIALCHARS = ["+", "!", "<", ":", "-", 
                "?", ">", ";", "*", "^",
                "(", ")", "/", '"', ".",
                ",", "=", "'", "[", "]",
                "%", "~", "&", "\\", "{",
                "}", "#", "|"]

def isLeapYear(year: int) -> bool:
    output = False
    if(year % 4 == 0):
        if(year % 100 == 0):
            if(year % 400 == 0):
                output = True
            else:
                output = False    
        else:
            output = True
    return output
    
# Checks the format of a date
# Format is DDMMYYYY
# Returns True if the format is valid
DATESIZE = 8
def checkDate(date: str ) -> bool:

    if len(date) != DATESIZE:
        return False
    
    date = trimStr(date)

    # Check there are 8 decimal digits
    isDoBvalid = (len(date) == 8) and date.isdecimal() 

    # Check the month
    month = int(date[2] + date[3]) # append digit 2 and 3, then convert to int
    isDoBvalid = isDoBvalid and ((month >= 1) and (month <= 12)) # update the 'validity' boolean

    # Check the year
    year = int(date[4] + date[5] + date[6] + date[7]) 
    # Year must be less than the current year minus 18 (legal age for making the booking)  
    #isDoBvalid = isDoBvalid and (year <= (date.today().year - 18)) 
    
    # Check the day
    day = int(date[0] + date[1])
    # February has 28 or 29 days (leap year)
    if month == 2:
        if(isLeapYear(year)):        
            isDoBvalid = isDoBvalid and ((day >=1) and (day <= 29))
        else:
            isDoBvalid = isDoBvalid and ((day >=1) and (day <= 28))
    # Months with 30 days:
    # Apr, Jun, Sep, Nov
    elif month == 4 | 6 | 9 | 11:
        isDoBvalid = isDoBvalid and ((day >=1) and (day <= 30))
    # Months with 31 days:
    # Jan, March, May, Jul, Aug, Oct, Dec
    else:
        isDoBvalid = isDoBvalid and ((day >=1) and (day <= 31))  

    return isDoBvalid

#MALAYSIACOUNTRYCODE = '60'
#INTERNATIONALPHONEPREFIX = '011' 

# 4 different parts 
# +CC AAA PPPP PPPP
E164LEN_A = 4

# 3 different parts
# +CC AAA PPPPPPPP
E164LEN_B = 3

# Contact number should have E.164 format (separated with spaces):
# +CC AAA PPPP PPPP 
# +CC -> Country code
# AAA -> Area code
# PPPP PPPP -> Phone number
def checkContactNumber(num: str) -> bool:
    
    # Empty str means error...
    if(len(num) == 0):
        return False

    numCodes = num.split()

    if len(numCodes) != E164LEN_A:
        return False

    countryCode = numCodes[0]
    areaCode = numCodes[1]
    phoneNumber = numCodes[2] + numCodes[3]

    invalidCountryCode = False
    invalidAreaCode = False
    invalidPhoneNumber = False

    # Check country code
    if(countryCode[0] == '+'):
        countryCode = countryCode.removeprefix('+')
        if ((len(countryCode) < 2 or len(countryCode) > 4)  
            or not (countryCode.isdecimal()) 
            or int(countryCode) <= 0): 

            invalidCountryCode = True
    else:
        if ((len(countryCode) < 1 or len(countryCode) > 3)  
            or not (countryCode.isdecimal()) 
            or int(countryCode) <= 0): 

            invalidCountryCode = True

    # Check area code
    if((len(areaCode) < 1 or len(areaCode) > 5)
       or not areaCode.isdecimal()
       or int(areaCode) <= 0):    

        invalidAreaCode = True
        
    # Check phone number
    if(len(phoneNumber) > 8 or len(phoneNumber)  < 1
       or not phoneNumber.isdecimal()
       or int(phoneNumber) <= 0):
        
        invalidPhoneNumber = True

    return not (invalidCountryCode or invalidAreaCode or invalidPhoneNumber)

# Email should be provided only with the "email"
# suffix to avoid checking every single mail out there....
# The email should consist of three parts:
# <mailuser> @email .com 
def checkEmail(email: str) -> bool:

    # First check the .com through reverse iteration 
    i = len(email)-1

    # The 'stop' char is at position len(email) - 5
    stop = len((email))-len(".com")-1 
    charbuffer = "" 
    while i > stop: 
        charbuffer += email[i] 
        i -= 1

    charbuffer = charbuffer[::-1] # Reverse the buffer
    comSuffixErr = (charbuffer != ".com")

    # Clear charbuffer  
    charbuffer = ""

    # Then check the @email
    i = len(email)-5
    stop = i - len("@email") 
    charbuffer = "" 
    while i > stop: 
        charbuffer += email[i] 
        i -= 1

    charbuffer = charbuffer[::-1] # Reverse the buffer

    emailNameErr = (charbuffer != "@email")        

    # Finally check the user 
    # Should not contain any special char 
    # OR be empty OR start with a number
    charbuffer = ""
    i = len(email) - len("@email.com") -1 
    stop = 0

    while i >= stop:
        charbuffer += email[i]
        i-=1

    charbuffer = charbuffer[::-1] 
    noName = len(charbuffer) == 0 # Check if its empty
    startsWithNumber = False
    if not noName:
        startsWithNumber = charbuffer[0].isdecimal()

    # Check if the name has any special char
    nameHasSpecialChar = False
    for c in charbuffer:
        if c in SPECIALCHARS:
            nameHasSpecialChar = True
            break

    return not (comSuffixErr or emailNameErr 
                or nameHasSpecialChar or noName or startsWithNumber)

# Compares two dates in string format    
# Returns DATEBIGGER if the greaterDate is more recent than lesserDate
DATEMORERECENT = 0
DATELESSRECENT = 1 
DATEEQUAL = 2
DATEERROR = 3

# Compares two dates
# Returns true if greaterDate is more recent
# than lesserDate
# i.e. dateMoreRecentThan(2015, 2000) should return True 
def dateMoreRecentThan(greaterDate: str, lesserDate: str) -> int:

    if not checkDate(greaterDate):
        errorlog.logError("dateMoreRecentThan(): INVALID GREATERDATE FORMAT!")
        errorlog.logError("Date inputed: " + greaterDate)
        return DATEERROR
    if not checkDate(lesserDate):
        errorlog.logError("dateMoreRecentThan(): INVALID LESSERDATE FORMAT!")
        errorlog.logError("Date inputed: " + lesserDate)
        return DATEERROR

    greaterDateDay = int(greaterDate[0]+greaterDate[1])
    greaterDateMonth = int(greaterDate[2] + greaterDate[3])
    greaterDateYear = int(greaterDate[4] + greaterDate[5] + greaterDate[6] + greaterDate[7])
    
    lesserDateDay = int(lesserDate[0]+lesserDate[1])
    lesserDateMonth = int(lesserDate[2]+lesserDate[3])
    lesserDateYear = int(lesserDate[4]+lesserDate[5]+lesserDate[6]+lesserDate[7])
    
    if(greaterDateYear > lesserDateYear):
        return DATEMORERECENT
    elif(lesserDateYear > greaterDateYear):
        return DATELESSRECENT
    else:
        if(greaterDateMonth > lesserDateMonth):
            return DATEMORERECENT
        elif(lesserDateMonth > greaterDateMonth):
            return DATELESSRECENT
        else:
            if(greaterDateDay > lesserDateDay):
                return DATEMORERECENT
            elif(lesserDateDay > greaterDateDay):
                return DATELESSRECENT
            else:
                return DATEEQUAL

# This function gets an int, and returns its 
# formatted str with an additional '0' in case it is required
# Used for avoiding size problems with date management 
# 1 -> 01
def force2Digits(inint:int):
    if(inint < 10):
        return '0' + str(inint)
    else:
        return str(inint)

# Returns a string representing the sexagesimal 
# conversion of a decimal expression of an hour 
# Note:(only values between 00:00 and 24:00 allowed)
# i.e. 6.5 -> 06:30
def decimalHourToSexagesimal(decHour : float) -> str:
    intPart = math.trunc(decHour)
    
    floatPart = float(decHour - math.trunc(decHour)) * 10
    floatPart *= int(60/10)

    strIntPart = str(intPart)
    if(intPart < 10):
        strIntPart = "0"+strIntPart
    
    strFloatPart = str(int(floatPart))
    if(int(floatPart) < 10):
        strFloatPart = strFloatPart+"0"

    return(strIntPart+":"+strFloatPart)

SEGHOURLEN_A = 5 # 2 digits for hour, 1 digit for ':', 2 digits for minutes
SEGHOURLEN_B = 4 # 2 digits for hour, 2 digits for minutes

# Converts an hour in the format of HH:MM
# to a float
# Returns -1 in case the input is invalid
def sexagesimalHourToDecimal(segHour : str) -> float:

    invalidLength = False
    invalidMinutes = False

    if(len(segHour) != SEGHOURLEN_A and len(segHour) != SEGHOURLEN_B):
        return -1        

    # HH:MM    
    elif(len(segHour) == SEGHOURLEN_A):
        hourPart = segHour[0] + segHour[1]
        minutesPart = segHour[3] + segHour[4]
    # HHMM
    elif(len(segHour) == SEGHOURLEN_B):
        hourPart = segHour[0] + segHour[1]
        minutesPart = segHour[2] + segHour[3]

    hourPart = int(hourPart)
    minutesPart = int(minutesPart)

    # Not a valid hour
    if(hourPart >= 24 or hourPart < 0):
        return -1
    elif(minutesPart >= 60 or minutesPart < 0):
        return -1

    minutesPartf = minutesPart / 60
    return hourPart + minutesPartf

#==================================================#