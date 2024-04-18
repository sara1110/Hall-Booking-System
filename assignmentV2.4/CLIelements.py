import utility as util

# Global UI Constants 
PROMPT = ">>" 
TITLEBAR = "-------"  

def okPrompt():
    input(util.turnYellow("< OK >"))

# Abstract class 
class CLIelement:
    pass

# Use this for no element at CLI
class endCLIelem(CLIelement):
    pass

# - This class represents a single UI state 
# within the CLI frontend
# - It needs a CLIelement associated to it, and a
# stateFunctionCode that represents its behaviour
# - State to state transition is controlled by the UI components
# - processTiming determines if the state function should be 
# executed before or after the UI display / update
# - process timing can be either EXECUTEBEFORE or EXECUTEAFTER
EXECUTEBEFORE = 0
EXECUTEAFTER = 1
class CLIstate:
    def __init__(self, uiElement : CLIelement, stateFunctionCode: int, stateFunctionMap: dict, functionTiming: int, stateMapRef: dict) -> None:
        # Check that uiElement is a subclass of CLIstate
        if(type(type(uiElement)) == CLIstate):
            print(util.turnRed("CLIstate error: CLI element provided cannot be abstract (class CLIelement)"))
            print(util.turnRed("CLIstate error: Only provide subclasses of CLIelement"))
        else:
            # self.stateMap = stateMap
            self.uiElement = uiElement
            self.stateFunctionCode = stateFunctionCode
            self.stateFunctionMap = stateFunctionMap
            self.functionTiming = functionTiming
            self.stateMapRef = stateMapRef 

# These are optional codes which can
# be returned by state functions, in order to communicate 
# with updateCLIstate (And avoiding circular references)
STATEFUNCTIONSUCESS = 0
STATEFUNCTIONFAIL = -1

def updateCLIstate(state : CLIstate, stateCode: int, invalidLastInput : bool):

    # Execute UI process
    if(type(state.uiElement) == OptionsMenu):
        util.clearScr()
        if(state.functionTiming == EXECUTEBEFORE):
            # Call the state function making a lookup in the stateFunctionMap
            state.stateFunctionMap[state.stateFunctionCode]([])

        displayOptionsMenu(state.uiElement, invalidLastInput)
        
        updateOutput = updateOptionsMenu(stateCode, state.stateMapRef)
        invalidLastInput = updateOutput[0]
        nextStateCode = updateOutput[1]

        if(invalidLastInput):
            updateCLIstate(state, stateCode, True)  
            return 
               
        if(state.functionTiming == EXECUTEAFTER):
            # Call the state function making a lookup in the stateFunctionMap
            state.stateFunctionMap[state.stateFunctionCode]([])
        
        #print("State transition!")
        updateCLIstate(state.stateMapRef[nextStateCode], nextStateCode, False)
        return
    
    elif(type(state.uiElement) == MultipleInput):
        util.clearScr()

        if(state.functionTiming == EXECUTEBEFORE):
            # Call the state function making a lookup in the stateFunctionMap
            state.stateFunctionMap[state.stateFunctionCode]([])

        uiInput = updateMultipleInput(state.uiElement)
        nextStateCode = uiInput[0]
        prevStateCode = state.uiElement.prevStateCode
        args = uiInput[1]
        
        if(state.functionTiming == EXECUTEAFTER):
            # Call the state function making a lookup in the stateFunctionMap
            sucess = state.stateFunctionMap[state.stateFunctionCode](args)
            if sucess == STATEFUNCTIONSUCESS or sucess == None:
                updateCLIstate(state.stateMapRef[nextStateCode], nextStateCode, False)
            elif sucess == STATEFUNCTIONFAIL: 
                updateCLIstate(state.stateMapRef[prevStateCode], prevStateCode, False)
        else:
            updateCLIstate(state.stateMapRef[nextStateCode], nextStateCode, False)
        return
   
    # If state is "finish", return and exit state machine
    elif(type(state.uiElement) == endCLIelem):
        return    

    util.clearScr()

# Class used to represent a simple Menu with multiple options,
# along with its background process function mapped to 'processCode', 
# and a 'trigger' linked to each option. Each 'trigger' represents a state code
# towards which the state machine will go when the option is selected
class OptionsMenu(CLIelement):
    def __init__(self, title:str, options:list, triggers:list) -> None:
        # options and optionTriggers must logically
        # have the same size
        if(len(options) != len(triggers)):
            print("Menu creation error: options and optionTriggers dont have the same length!")
        else:
            # TYPE CHECKING
            # options must have all of its items of str type
            # optionTriggers must only have Menu items
            optionTypeErr = False
            optionTrgTypeErr = False
            
            if not util.isListType(options, str): 
                optionTypeErr = True

            if not util.isListType(triggers, int): 
                optionTrgTypeErr = True

            if(optionTypeErr):  
                print("Menu creation error: options has an item of invalid type")
            if(optionTrgTypeErr):
                print("Menu creation error: optionTriggers has an item of invalid type")

            # If no errors, proceed to assigning each property
            if(not (optionTypeErr or optionTrgTypeErr)):
                self.title=title
                self.options=options
                self.triggers=triggers
                # This is used in case to output the 'invalid input' message
                self.invalidLastInput = False  

def displayOptionsMenu(menu : OptionsMenu, invalidLastInput: bool):
    counter=1
    print(util.turnYellow(menu.title))
    print(TITLEBAR)
    
    if(invalidLastInput):
        print(util.turnRed("Invalid input, please try again"))

    for option in menu.options:
        print(util.turnYellow(str(counter)) + ". " + option)
        counter+=1 

# Returns a list with validChoice at i=0
# and nextMenuCode at i=1
def updateOptionsMenu(menuCode: int, stateMap: dict) -> list:
    choice = input(util.turnYellow(PROMPT))
    validChoice = False

    # Avoid str to int conversion error     
    if (len(util.trimStr(choice))) > 1 or (len(choice) == 0) or (not choice.isdecimal()):
        return [True, menuCode]        

    choice = int(choice)

    for i in range(0, len(stateMap[menuCode].uiElement.options)):
        if choice-1 == i:
            validChoice = True

    if validChoice:
        nextMenuCode = stateMap[menuCode].uiElement.triggers[choice-1]

        # Two outputs are required, this is why
        # an Array is returned    
        return [False, nextMenuCode]    
    else:
        return [True, menuCode]

# Used for MultipleInput
# - expectedInput can either be a single string, 
# a list of strings (more than one corrent input possible),
# or EXPECTED_NOCHECK in case the field does not need checking (value only stored)
EXPECTED_NOCHECK = -1
class MultipleInputField:
    def __init__(self, fieldName: str, expectedInput : list | str | int) -> None:
        
        listTypeErr = False
        nocheckErr = False        

        # Check that the list only contains strings 
        if(type(expectedInput) == list):
            if not util.isListType(expectedInput, str):
                listTypeErr = True
        elif(type(expectedInput) == int):    
            if expectedInput != EXPECTED_NOCHECK:
                nocheckErr = True

        if(listTypeErr):
            print(util.turnRed("MultipleInputField error: expectedInput needs to have only str items"))
        if(nocheckErr):         
            print(util.turnRed("MultipleInputField error: expectedInput can only be provided as EXPECTED_NOCHECK if it is not str or list")) 

        # If no errors, successfully create the object  
        if(not (listTypeErr or nocheckErr)):              
            self.fieldName=fieldName
            self.expectedInput = expectedInput        

# This function automatically creates and returns a
# list of MultipleInputFields from the given parameters
# - fieldNames refers to each input name (redundant)
# - expected Inputs contain the expected input for each prompt.
# In case there is no checking needed, an empty list can be provided
def createMultipleInputFields(fieldNames:list, expectedInputs:list) -> list:
    
    # Initialize the output prompt list
    registrationPrompts = []
    noCheckAll = False

    diffSizeErr = False
    typeErr = False

    if(len(expectedInputs) == 0):
        noCheckAll = True
        pass
    else:
        # error
        if(len(fieldNames) != len(expectedInputs)):
            print(util.turnRed("createMultipleInputFields() error: fieldNames has different size from expectedInputs!"))
            diffSizeErr = True

    if not util.isListType(fieldNames, str):
        print("createMultipleInputFields() error: fieldNames must only contain strings!")    
        typeErr = True

    if not (diffSizeErr or typeErr):
        for i in range(0, len(fieldNames)):
            if(noCheckAll):
                registrationPrompts.append(MultipleInputField(fieldNames[i], EXPECTED_NOCHECK))
            else:
                registrationPrompts.append(MultipleInputField(fieldNames[i], expectedInputs[i]))
    
    return registrationPrompts

# Prompts the user to enter data in a specific field
# Performs error checking and outputs the input data
# This works as both a display and update function
def promptMultipleInputField(field : MultipleInputField, invalidInput : bool, scapeSequence: str) -> str:
    if invalidInput:
        print(util.turnRed("Invalid input, please try again"))
    fieldInput = input(field.fieldName + " " + PROMPT + " ")

    if(len(fieldInput) == 0):
        promptMultipleInputField(field, False, scapeSequence)
        return
    
    # Remove whitespace at start and end
    fieldInput = util.trimEdges(fieldInput)
    
    # If it is a scape sequence then exit the prompt
    if(fieldInput == scapeSequence and scapeSequence != NULLSCAPESEQ):
        return fieldInput

    if(type(field.expectedInput) == str):
        if(fieldInput != field.expectedInput):
            promptMultipleInputField(field, True, scapeSequence)
            return 
    
    elif(type(field.expectedInput) == list):
        invalidInput = True 

        for exp in field.expectedInput :    
            if(fieldInput == exp):
                invalidInput = False
                break

        if(invalidInput):
            promptMultipleInputField(field, True, scapeSequence)
            return

    return fieldInput

# Class used to represent a multiple input
# interface such as those used for entering credentials
# -> scapeSequence is the char or str that will cause the 
# program to  exit this state
class MultipleInput(CLIelement):
    def __init__(self, fields : list, nextStateCode:int, prevStateCode:int, stateMap:dict, scapeSequence: str) -> None:
        
        # Error checking
        if not util.isListType(fields, MultipleInputField):
            print(util.turnRed("MultipleInput error: fields can only have items of MultipleInputField type"))
        else:  
            self.fields = fields
            self.nextStateCode = nextStateCode
            self.prevStateCode = prevStateCode
            self.stateMap = stateMap
            self.scapeSequence = scapeSequence

DEFAULTSCAPESEQ = "q"
NULLSCAPESEQ = "" 

# Returns an array with nextStateCode at position 0,
# and inputArr at position 1
def updateMultipleInput(minput : MultipleInput) -> list:
    invalidInput = False
    inputArr = []
    cancelTrigger = False

    if(minput.scapeSequence != NULLSCAPESEQ):
        print("(Input " + util.turnRed(minput.scapeSequence) + " to cancel)")
    
    for field in minput.fields:
        fieldValue = promptMultipleInputField(field, invalidInput, minput.scapeSequence) 
        if(fieldValue == minput.scapeSequence 
           and minput.scapeSequence != NULLSCAPESEQ):
            cancelTrigger = True
            break
        else:
            if(util.trimStr(str(fieldValue)) != "" 
               and type(fieldValue) != None):
                inputArr.append(fieldValue)

    if cancelTrigger:
        return [minput.prevStateCode, []]
    else:
        input(util.turnYellow("< OK >"))
        return [minput.nextStateCode, inputArr] 
