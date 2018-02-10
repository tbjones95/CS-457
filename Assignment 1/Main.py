# Import Libraries
import atexit
import json
from Database import databaseShell

# Functions
def main():

    # Variables
    dbCommand = None
    result = None
    database = databaseShell()

    # Loop until user wants to quit
    while True:

        # Get users command
        dbCommand = raw_input(":>")

        # Parse user commands
        if not dbCommand == "":
            result = database.parseUserCommands(dbCommand)

        if result == -1:
            break

if __name__ == "__main__":
    main()
