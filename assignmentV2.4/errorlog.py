#import utility as util
import json

ERRORLOG_FILEPATH = "files/errorlog.txt"

def logError(error: str):
    with open(ERRORLOG_FILEPATH, "a") as file:
        json.dump(error, file)
        file.write("\n")
