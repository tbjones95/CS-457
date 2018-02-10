# Import Libraries
import atexit
import json
from Database import databaseShell

# Functions
def main():

    # Variables
    database = databaseShell()

    # Call shell
    database.cmdloop()
    
if __name__ == "__main__":
    main()
