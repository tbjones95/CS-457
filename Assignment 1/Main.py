# Authors: Amir Behmaram and Tanner Jones
# Date: 2/22/2018
# Version: 1.0

# Import Libraries
import atexit, json, sys
from Database import databaseShell

# Functions
def main():

    # Variables
    database = databaseShell()

    # If something has been passed via standard input
    if not sys.stdin.isatty():
        for line in sys.stdin:
            stripped = line.strip()

            if not stripped:
                break
            if stripped.startswith('--'):
                continue
            if stripped == '.EXIT':
                print "Program ending"
                break

            database.onecmd(stripped)
    else:
        # Call shell
        database.cmdloop()

if __name__ == "__main__":
    main()
