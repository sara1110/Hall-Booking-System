import utility as util
import CLIelements as cli
import pseudoGraphics as gfx
import admin
import user

# 1) Define function codes
# 2) Map function codes to functions
# 3) Define state codes
# 4) Create EMPTY state map
# 5) Define UI objects
# 6) Define State objects (CLIstates)
# 7) Map state codes to states
# 8) Update state map reference
# 9) Start state machine (startInterface())

# used as placeholder or 
# for ending the state sequence
def nullFunc(nullargs):
    return

#============= STATE FUNCTION CODES DEFINITION =================#

NULLFUNC = -1
MAINMENULOGOFUNC = 0 
# -- (Admin) Hall management functions --
SETHALLFUNC = 1
VIEWHALLSFUNC = 2
SEARCHHALLFUNC = 3
DELETEHALLFUNC = 4
# -- (Admin) Booking management functions --
ADMINADDBKNGFUNC = 5
SEARCHBOOKINGFUNC = 6
VIEWBOOKINGSFUNC = 7
DELETEBOOKINGFUNC = 8

# -- (Admin) User management functions -- 
ADMINVIEWUSERSFUNC = 9
ADMINSEARCHUSERFUNC = 10
ADMINADDSETUSERFUNC = 11
ADMINDELETEUSERFUNC = 12

# -- User register and login -- 
USERREGISTERFUNC = 13
USERLOGINFUNC = 14

ADMINMENUFUNC = 15
USERMENUFUNC = 16

# -- User session --
USERSCHEDULEFUNC = 17
USERVIEWHALLSFUNC = 18
USERMAKEBOOKINGFUNC = 19
USERVIEWBOOKINGSFUNC = 20
USEREDITBOOKINGFUNC = 21
USERCANCELBOOKINGFUNC = 22
USERSEARCHBOOKINGFUNC = 23
USERPROFILEFUNC = 24
USEREDITPROFILEFUNC = 25
#===============================================================#

#================== STATE FUNCTION MAPPING ===================#

# This map contains all the state functions
# used by interface states
stateFunctionMap = {
    # Placeholder function code
    NULLFUNC : nullFunc,

    MAINMENULOGOFUNC : gfx.printCubeLogo, 
    ADMINMENUFUNC : admin.adminMenu,
    
    # Admin hall management
    SETHALLFUNC : admin.addSetHallInfo,
    VIEWHALLSFUNC : admin.showAllHalls,
    SEARCHHALLFUNC : admin.searchHall,
    DELETEHALLFUNC : admin.deleteHall,
    
    # Admin booking management
    ADMINADDBKNGFUNC : admin.addSetBooking,
    SEARCHBOOKINGFUNC : admin.searchBooking,
    VIEWBOOKINGSFUNC : admin.viewBookings,
    DELETEBOOKINGFUNC : admin.deleteBooking,
    
    # Admin user management
    ADMINVIEWUSERSFUNC : admin.viewUsers,
    ADMINSEARCHUSERFUNC : admin.searchUser,
    ADMINADDSETUSERFUNC : admin.addSetUser,
    ADMINDELETEUSERFUNC : admin.deleteUser,
    
    # User register and login functions
    USERREGISTERFUNC : user.userRegister,
    USERLOGINFUNC : user.userLogin,    

    # User session functions
    USERMENUFUNC : user.userMenuInterface,
    USERSCHEDULEFUNC : user.displayDateSchedule,
    USERVIEWHALLSFUNC : user.viewAvailableHalls,
    USERMAKEBOOKINGFUNC : user.makeBooking,
    USERVIEWBOOKINGSFUNC : user.viewBookings,
    USEREDITBOOKINGFUNC : user.editBooking,
    USERCANCELBOOKINGFUNC : user.cancelBooking,
    USERSEARCHBOOKINGFUNC : user.searchBooking,
    USERPROFILEFUNC : user.showProfile,
    USEREDITPROFILEFUNC : user.editProfile,
}
#===============================================================#

#================= STATE CODES DEFINITION =================#
# Create codes for the stateMap

ENDCODE = -1
MAINMENU = 0
# ---- ADMIN STATES ----
ADMINLOGIN = 1
ADMINMENU = 2
ADMINHALLMNG = 3
ADMINBOOKINGMNG = 4
ADMINUSERMNG = 5

# -- Hall Management -- 
ADMINSETHALL = 6
ADMINVIEWHALLS = 7
ADMINSEARCHHALL = 8
ADMINSEARCHHALL = 9
ADMINEDITHALL = 10
ADMINDELETEHALL = 11

# -- Booking Management -- 
ADMINVIEWBOOKINGS = 12
ADMINSEARCHBKNG = 13
ADMINADDSETBKNG = 14
ADMINDELETEBLOCKBKNG = 15

# -- User Management -- 
ADMINVIEWUSER = 16
ADMINSEARCHUSER = 17
ADMINADDSETUSER = 18
ADMINDELETEBLOCKUSER = 19 

# ---- User functions ----
USERLOGINMENU = 20
USERLOGIN = 21
USERREGISTER = 22
USERMENU = 23
USERDISPLAYSCHEDULE = 24
USERVIEWHALLS = 25
USERMAKEBOOKING = 26
USERVIEWBOOKINGS = 27
USEREDITBOOKING = 28
USERCANCELBOOKING = 29
USERSEARCHBOOKING = 30
USERSHOWPROFILE = 31
USEREDITPROFILE = 32
#===============================================================#

# Initialize the state map.
# It needs to be provided to the UI components as a parameter, 
# this is the reason why it needs to be initialized BEFORE the
# UI component definition
stateMap = {}

#================= USER INTERFACE DEFINITIONS =================#

# Create the empty ui for the end state (ENDCODE)
endElement = cli.endCLIelem()

mainMenu_ui = cli.OptionsMenu("Welcome to HALL SYMPHONY", 
                           ["Login as administrator", "Login as user", "Exit"], 
                           [ADMINLOGIN, USERLOGINMENU, ENDCODE])

adminCredentialPrompts = cli.createMultipleInputFields(["Username", "Password"], [admin.ADMINUSERNAME, admin.ADMINPASSWORD])
adminLogin_ui = cli.MultipleInput(adminCredentialPrompts, ADMINMENU, MAINMENU, stateMap, cli.DEFAULTSCAPESEQ)

adminMenu_ui = cli.OptionsMenu("Welcome, " + util.turnYellow("localadmin"),
                            ["Hall management actions",  "Booking management actions", "User management actions", "Logout"],
                            [ADMINHALLMNG, ADMINBOOKINGMNG, ADMINUSERMNG, MAINMENU])


#----------------- ADMIN HALL MANAGEMENT -----------------#

adminHallMng_ui = cli.OptionsMenu("Hall Management",
                               ["Set hall information", "View all hall information", 
                                "Search hall information", "Delete hall information", "Go back"],
                                [ADMINSETHALL, ADMINVIEWHALLS, 
                                 ADMINSEARCHHALL, ADMINDELETEHALL, ADMINMENU])

hallFields = [
      "Hall ID", "Hall name", "Hall description",
      "Hall pax", "Hall availability", "Hall price rate (RM/hour)", "Hall Type"]
setHallPrompts = cli.createMultipleInputFields(hallFields, [])
adminSetHall_ui = cli.MultipleInput(setHallPrompts, ADMINHALLMNG, ADMINHALLMNG, stateMap, cli.DEFAULTSCAPESEQ)

# No prompts, this interface just shows all the halls
# and waits for user input to go back to the previous menu
adminViewHalls_ui = cli.MultipleInput([], ADMINHALLMNG, ADMINHALLMNG, stateMap, cli.NULLSCAPESEQ)

hallIDprompt = cli.MultipleInputField("Hall ID", cli.EXPECTED_NOCHECK)
adminSearchHall_ui = cli.MultipleInput([hallIDprompt], ADMINHALLMNG, ADMINHALLMNG, stateMap, cli.DEFAULTSCAPESEQ)

#deleteBlockHallPrompts = cli.createMultipleInputFields(["Hall ID", util.turnRed("Are you sure? (y/n)")], [cli.EXPECTED_NOCHECK, ["y", "n"]])
adminDeleteBlockHall_ui = cli.MultipleInput(
    cli.createMultipleInputFields(
        ["Hall ID", util.turnRed("Are you sure? (y/n)")], 
        [cli.EXPECTED_NOCHECK, ["y", "n"]]), 
    ADMINHALLMNG, ADMINHALLMNG, 
    stateMap, cli.DEFAULTSCAPESEQ)

adminBookingMng_ui = cli.OptionsMenu(
    "Booking Management",
    ["View all bookings", "Search a booking",
    "Add/edit a booking", "Delete/cancel booking", "Go back"],
    [ADMINVIEWBOOKINGS, ADMINSEARCHBKNG, 
    ADMINADDSETBKNG, ADMINDELETEBLOCKBKNG, ADMINMENU])

#----------------- ADMIN BOOKING MANAGEMENT -----------------#

adminViewBookings_ui = cli.MultipleInput(
     [], 
     ADMINBOOKINGMNG, ADMINBOOKINGMNG, 
     stateMap, cli.NULLSCAPESEQ)

adminAddSetHallPrompts = cli.createMultipleInputFields(
     ["Booking ID", "User", "Start Time", "End Time", "Hall ID", "Date (DDMMYYYY)"],
     [])

adminAddSetBooking_ui = cli.MultipleInput(
     adminAddSetHallPrompts, 
     ADMINBOOKINGMNG, ADMINBOOKINGMNG, 
     stateMap, cli.DEFAULTSCAPESEQ)

adminSearchBooking_ui = cli.MultipleInput(
    [cli.MultipleInputField("Booking ID", cli.EXPECTED_NOCHECK)],
    ADMINBOOKINGMNG, ADMINBOOKINGMNG, 
    stateMap,cli.DEFAULTSCAPESEQ)

adminDeleteBooking_ui = cli.MultipleInput(
    cli.createMultipleInputFields(
        ["Booking ID", util.turnRed("Are you sure? y/n")],
        [cli.EXPECTED_NOCHECK, ["y", "n"]]),
    ADMINBOOKINGMNG, ADMINBOOKINGMNG,
    stateMap, cli.DEFAULTSCAPESEQ)

#----------------- ADMIN USER MANAGEMENT -----------------#

adminUserMng_ui = cli.OptionsMenu("User management",
                               ["View all the user information", "Search user", 
                                "Add/set user", "Delete/block user", "Go back"],
                               [ADMINVIEWUSER, ADMINSEARCHUSER,  
                                ADMINADDSETUSER, ADMINDELETEBLOCKUSER, ADMINMENU])

# Registered users dump
adminViewUsers_ui = cli.MultipleInput(
    [], ADMINUSERMNG, ADMINUSERMNG, 
    stateMap, cli.NULLSCAPESEQ
)

adminSearchUser_ui = cli.MultipleInput(
    cli.createMultipleInputFields(
        ["Username"], []   
    ),
    ADMINUSERMNG, ADMINUSERMNG,
    stateMap, cli.DEFAULTSCAPESEQ
)

adminAddSetUser_ui = cli.MultipleInput(
    cli.createMultipleInputFields(
        ["Username", "Password", "First name", "Last name",
        "Date of birth (DDMMYYYY)", "Contact number (+CC AAA PPPP PPPP) ", "Email (@email.com)"],
        []
    ),
    ADMINUSERMNG, ADMINUSERMNG,
    stateMap, cli.DEFAULTSCAPESEQ
)

adminDeleteUser_ui = cli.MultipleInput(
     cli.createMultipleInputFields(
          ["Username", util.turnRed("Are you sure? y/n")],
          [cli.EXPECTED_NOCHECK, ["y", "n"]]
     ),
     ADMINUSERMNG, ADMINUSERMNG,
     stateMap, cli.DEFAULTSCAPESEQ
)

#----------------- USER PRE-LOGIN UIS -----------------#

# User login / register menu
userLoginMenu_ui = cli.OptionsMenu("User session",
                                ["Register user", "Login as existing user", "Go back to main menu"],
                                [USERREGISTER, USERLOGIN, MAINMENU])

# User registration UI
userRegistration_ui = cli.MultipleInput(
    cli.createMultipleInputFields(
        ["Username", "Password", "First name", "Lastname",
        "Date of birth (DDMMYYYY)", "Contact number (+CC AAA PPPP PPPP)", "Email address (@email.com)"], []),
    USERLOGINMENU,
    USERLOGINMENU,
    stateMap,
    cli.DEFAULTSCAPESEQ
)

# User Login UI
userLogin_ui = cli.MultipleInput(
    cli.createMultipleInputFields(
        ["Username", "Password"], []),
    USERMENU,
    USERLOGINMENU,
    stateMap,
    cli.DEFAULTSCAPESEQ)

 #-----------------  USER ACTIONS  -----------------#

userMenu_ui = cli.OptionsMenu(
    "Choose your action",
    ["Display a booking schedule", "View available halls", "Make a new booking", 
    "View your bookings", "Edit a booking", "Cancel a booking", 
    "Search for a booking", "Profile", "Logout"],
    [USERDISPLAYSCHEDULE, USERVIEWHALLS, USERMAKEBOOKING, 
    USERVIEWBOOKINGS, USEREDITBOOKING, USERCANCELBOOKING, 
    USERSEARCHBOOKING, USERSHOWPROFILE, USERLOGINMENU])

userDisplaySchedule_ui = cli.MultipleInput(
    cli.createMultipleInputFields(
        ["hallID", "DDMMYYYY Date (enter TODAY for today's date):"],
        []
    ),
    USERMENU, USERMENU,
    stateMap, cli.DEFAULTSCAPESEQ)

userViewHalls_ui = cli.MultipleInput(
    [], USERMENU, USERMENU, stateMap, cli.NULLSCAPESEQ
)

userMakeBooking_ui = cli.MultipleInput(
     cli.createMultipleInputFields(
          ["Start time", "End time", "hallID", "DDMMYYYY Date"],
          []
     ),
     USERMENU, USERMENU,
     stateMap, cli.DEFAULTSCAPESEQ
)

userViewBookings_ui = cli.MultipleInput(
     cli.createMultipleInputFields([],[]),
     USERMENU, USERMENU,
     stateMap, cli.NULLSCAPESEQ
)

userEditBooking_ui = cli.MultipleInput(
     cli.createMultipleInputFields(
            ["Booking ID", "New Start Time", "New End time"],
            []),
    USERMENU, USERMENU,
    stateMap, cli.DEFAULTSCAPESEQ
)

userCancelBooking_ui = cli.MultipleInput(
     cli.createMultipleInputFields(
        ["Booking ID", util.turnRed("Are you sure? y/n")],
        [cli.EXPECTED_NOCHECK, ["y", "n"]]
     ),
     USERMENU, USERMENU,
     stateMap, cli.DEFAULTSCAPESEQ
)

userSearchBooking_ui = cli.MultipleInput(
    cli.createMultipleInputFields(
        ["BookingID"], []
    ),
    USERMENU, USERMENU,
    stateMap, cli.DEFAULTSCAPESEQ
)

userShowProfile_ui = cli.OptionsMenu(
    "",
    ["Edit profile", "Go back"],
    [USEREDITPROFILE, USERMENU]
)

userEditProfile_ui = cli.MultipleInput(
    cli.createMultipleInputFields(
         ["('PASS' to skip) Username", "('PASS' to skip) Password",
          "('PASS' to skip) First name", "('PASS' to skip) Last name",
          "('PASS' to skip) Date of Birth (format: DDMMYYYY)", "('PASS' to skip) Contact Number (+CC AAA PPPP PPPP)",
          "('PASS' to skip) E-mail (@email.com)"], []
    ),
    USERSHOWPROFILE, USERSHOWPROFILE,
    stateMap, cli.DEFAULTSCAPESEQ
)

#===============================================================#


#=====================  STATE DEFINITIONS ======================#
# Once UIs have been defined, create the States

# MAIN MENUS / LOGIN
endState = cli.CLIstate(endElement, NULLFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
mainMenuState = cli.CLIstate(mainMenu_ui, MAINMENULOGOFUNC, stateFunctionMap, cli.EXECUTEBEFORE, stateMap)
adminLoginState = cli.CLIstate(adminLogin_ui, NULLFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
adminMenuState = cli.CLIstate(adminMenu_ui, ADMINMENUFUNC, stateFunctionMap, cli.EXECUTEBEFORE, stateMap)

# ADMIN HALL MANAGEMENT
adminHallMngState = cli.CLIstate(adminHallMng_ui, NULLFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
adminSetHallState = cli.CLIstate(adminSetHall_ui, SETHALLFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
adminViewHallsState = cli.CLIstate(adminViewHalls_ui, VIEWHALLSFUNC, stateFunctionMap, cli.EXECUTEBEFORE, stateMap)
adminSearchHallState = cli.CLIstate(adminSearchHall_ui, SEARCHHALLFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
adminDeleteBlockHallState = cli.CLIstate(adminDeleteBlockHall_ui, DELETEHALLFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)

# ADMIN BOOKING MANAGEMENT
adminBookingMngState = cli.CLIstate(adminBookingMng_ui, NULLFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
adminAddSetBookingState = cli.CLIstate(adminAddSetBooking_ui, ADMINADDBKNGFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
adminSearchBookingState = cli.CLIstate(adminSearchBooking_ui, SEARCHBOOKINGFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
adminViewBookingsState = cli.CLIstate(adminViewBookings_ui, VIEWBOOKINGSFUNC, stateFunctionMap, cli.EXECUTEBEFORE, stateMap)
adminDeleteBookingState = cli.CLIstate(adminDeleteBooking_ui, DELETEBOOKINGFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)

# ADMIN USER MANAGEMENT
adminUserMngState = cli.CLIstate(adminUserMng_ui, NULLFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
adminViewusersState = cli.CLIstate(adminViewUsers_ui, ADMINVIEWUSERSFUNC, stateFunctionMap, cli.EXECUTEBEFORE, stateMap)
adminSearchUserState = cli.CLIstate(adminSearchUser_ui, ADMINSEARCHUSERFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
adminAddSetUserState = cli.CLIstate(adminAddSetUser_ui, ADMINADDSETUSERFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
adminDeleteUserState = cli.CLIstate(adminDeleteUser_ui, ADMINDELETEUSERFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)

# USER LOGIN/REGISTER 
userLoginMenuState = cli.CLIstate(userLoginMenu_ui, NULLFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
userRegistrationState = cli.CLIstate(userRegistration_ui, USERREGISTERFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
userLoginState = cli.CLIstate(userLogin_ui, USERLOGINFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)

# USER FUNCTIONALITIES
userMenuState = cli.CLIstate(userMenu_ui, USERMENUFUNC, stateFunctionMap, cli.EXECUTEBEFORE, stateMap)
userDisplayScheduleState = cli.CLIstate(userDisplaySchedule_ui, USERSCHEDULEFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
userViewHallsState = cli.CLIstate(userViewHalls_ui, USERVIEWHALLSFUNC, stateFunctionMap, cli.EXECUTEBEFORE, stateMap)
userMakeBookingState = cli.CLIstate(userMakeBooking_ui, USERMAKEBOOKINGFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
userViewBookingsState = cli.CLIstate(userViewBookings_ui, USERVIEWBOOKINGSFUNC, stateFunctionMap, cli.EXECUTEBEFORE, stateMap)
userEditBookingState = cli.CLIstate(userEditBooking_ui,  USEREDITBOOKINGFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
userCancelBookingState = cli.CLIstate(userCancelBooking_ui, USERCANCELBOOKINGFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
userSearchBookingState = cli.CLIstate(userSearchBooking_ui, USERSEARCHBOOKINGFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
userShowProfileState = cli.CLIstate(userShowProfile_ui, USERPROFILEFUNC, stateFunctionMap, cli.EXECUTEBEFORE, stateMap)
userEditProfileState = cli.CLIstate(userEditProfile_ui, USEREDITPROFILEFUNC, stateFunctionMap, cli.EXECUTEAFTER, stateMap)
#===============================================================#

#=====================  STATE MAPPING ======================#
# Map each state to its code
stateMap = {
    ENDCODE : endState,
    MAINMENU : mainMenuState,
    
    # ---- ADMIN STATES ----
    ADMINLOGIN : adminLoginState,
    ADMINMENU : adminMenuState,
    
    # Admin hall management states ...
    ADMINHALLMNG : adminHallMngState,
    ADMINSETHALL : adminSetHallState,
    ADMINVIEWHALLS : adminViewHallsState,
    ADMINSEARCHHALL : adminSearchHallState,
    ADMINDELETEHALL : adminDeleteBlockHallState,

    # Admin booking management states ...
    ADMINBOOKINGMNG : adminBookingMngState,
    ADMINADDSETBKNG : adminAddSetBookingState,
    ADMINVIEWBOOKINGS : adminViewBookingsState,
    ADMINSEARCHBKNG : adminSearchBookingState,
    ADMINDELETEBLOCKBKNG : adminDeleteBookingState,

    # Admin user management states ...
    ADMINUSERMNG : adminUserMngState,
    ADMINVIEWUSER : adminViewusersState,
    ADMINSEARCHUSER : adminSearchUserState,
    ADMINADDSETUSER : adminAddSetUserState,
    ADMINDELETEBLOCKUSER : adminDeleteUserState,

    # User login / register states ...
    USERLOGINMENU : userLoginMenuState,
    USERREGISTER : userRegistrationState,
    USERLOGIN : userLoginState,
    # User session states ... 
    USERMENU : userMenuState,
    USERDISPLAYSCHEDULE : userDisplayScheduleState,
    USERVIEWHALLS : userViewHallsState,
    USERMAKEBOOKING : userMakeBookingState,
    USERVIEWBOOKINGS : userViewBookingsState,
    USEREDITBOOKING : userEditBookingState,
    USERCANCELBOOKING : userCancelBookingState,
    USERSEARCHBOOKING : userSearchBookingState,
    USERSHOWPROFILE : userShowProfileState,
    USEREDITPROFILE : userEditProfileState
}

# Update state map reference
# This is because python does not manage variable
# references / pointers
for value in stateMap.values():
        value.stateMapRef = stateMap

#===============================================================#

# trigger program start
def startInterface():
    cli.updateCLIstate(mainMenuState, MAINMENU, False)