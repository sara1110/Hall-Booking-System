import utility as util
import time

cubeAnimation1 = [
[
"      .+------+",     
"    .' |      |",    
"   +   |      |",   
"   |   |      |",  
"   |  .+------+",   
"   |.'      .' ",   
"   +------+    ",
],      
[
"     +------+",
"    /|      |",
"   + |      |",
"   | |      |",
"   | +------+",
"   |/      / ",
"   +------+  ",
],
[
"    +------+",
"    |      |",
"    +      +",
"    |      |",
"    +------+",
"    |      |",
"    +------+",
],
[
"   +------+",
"   |      |\ ",
"   |      | +",
"   |      | |",
"   +------+ |",
"    \      \|",
"     +------+",
],
[
"  +------+.",
"  |      | `.",
"  |      |   +",
"  |      |   |",
"  +------+.  |",
"   `.      `.|",
"     `+------+",
]
]

cubeAnimation2 = [
[
"      .+------+",     
"    .' |      |",    
"   +   |      |",   
"   |   |      |",  
"   |  .+------+",   
"   |.'      .' ",   
"   +------+    ",
"HALL SYMPHONY"
],
[
"      .+------+",     
"    .' |      |",    
"   +   |      |",   
"   |   |      |",  
"   |  .+------+",   
"   |.'      .' ",   
"   +------+    ",
"HALL SYMPHONY"
],
[
"      .+------+",     
"    .' |      |",    
"   +   |      |",   
"   |   |      |",  
"   |  .+------+",   
"   |.'      .' ",   
"   +------+    ",
"HALL SYMPHONY"
],
[
"      .+------+",     
"    .' |      |",    
"   +   |      |",   
"   |   |      |",  
"   |  .+------+",   
"   |.'      .' ",   
"   +------+    ",
util.turnYellow("HALL SYMPHONY")
],
[
"      .+------+",     
"    .' |      |",    
"   +   |      |",   
"   |   |      |",  
"   |  .+------+",   
"   |.'      .' ",   
"   +------+    ",
util.turnYellow(" HALL SYMPHONY")
],
[
"      .+------+",     
"    .' |      |",    
"   +   |      |",   
"   |   |      |",  
"   |  .+------+",   
"   |.'      .' ",   
"   +------+    ",
util.turnYellow("to HALL SYMPHONY")
],
[
"      .+------+",     
"    .' |      |",    
"   +   |      |",   
"   |   |      |",  
"   |  .+------+",   
"   |.'      .' ",   
"   +------+    ",
util.turnYellow("e to HALL SYMPHONY")
],
[
"      .+------+",     
"    .' |      |",    
"   +   |      |",   
"   |   |      |",  
"   |  .+------+",   
"   |.'      .' ",   
"   +------+    ",
util.turnYellow("ome to HALL SYMPHONY")
],
[
"      .+------+",     
"    .' |      |",    
"   +   |      |",   
"   |   |      |",  
"   |  .+------+",   
"   |.'      .' ",   
"   +------+    ",
util.turnYellow("lcome to HALL SYMPHONY")
],
[
"      .+------+",     
"    .' |      |",    
"   +   |      |",   
"   |   |      |",  
"   |  .+------+",   
"   |.'      .' ",   
"   +------+    ",
util.turnYellow("Welcome to HALL SYMPHONY")
],    
]

localadminLogo = [
"   ___________  ",
"  |.---------.| ",
"  ||         || ",
"  ||         || ",
"  ||         || ",
"  |'---------'| ",
"   `)__ ____('  ",
"   [=== -- o ]  ",
" __'---------'__  ",
"[::::::::::: :::] ",
' `"""""""""""""`  ',
]

userLogo = [
"      .---.       ",
"     |     |      ",
"      \___/       ",
"   ___/   \___    ",
" /           \ \  ",
" | |         | |  ",
" | |\       /| | \n",
]

auditorium = [
"   .+---------------+",
" .' |               |",
"+   |   ║▒▒▒▒▒║     |",
"|   |   ║▒▒▒▒▒║     |",
"|  .+--▄▄▄▄▄▄▄------+",
"|.'               .'",
"+----------------+",
]

banquetHall = [
"   .+-------------+",
" .' |             |",
"+   |             |",
"|  .+-------------+",
"|.' ╔═════════╗ .'",
"+--------------+",
]

meetingHall = [
"        .+--------+",
"      .' |        |",
"     +   |  ▓▓▓   |",
"     |  .+--------+",
"     |.' ┌┐  ┌┐ .'",
"     +---------+", 
]

def printFrame(frame):
    for line in frame:
        print(line)

def playAnimation(animationFrames):
    for frame in animationFrames:
        util.clearScr()
        printFrame(frame)
        time.sleep(0.1)

def playAnimationReverse(animationFrames):
    counter = len(animationFrames) - 1
    while counter >= 0:
        util.clearScr()
        printFrame(animationFrames[counter])
        time.sleep(0.1)
        counter -= 1 
    pass

def playStartupAnimation():
    playAnimation(cubeAnimation1)
    playAnimationReverse(cubeAnimation1)
    playAnimation(cubeAnimation2)

def printCubeLogo(args):
    printFrame(cubeAnimation1[0])

def printlocaladminLogo():
    printFrame(localadminLogo)                

def printUserLogo():
    printFrame(userLogo)

def printAuditorium():
    printFrame(auditorium)

def printBanquetHall():
    printFrame(banquetHall)

def printMeetingHall():
    printFrame(meetingHall)