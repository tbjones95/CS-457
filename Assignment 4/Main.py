# Authors: Amir Behmaram and Tanner Jones
# Date: 3/27/2018
# Version: 2.0

# Import Libraries
import atexit, json, sys
from Database import databaseShell

# Globals
empty = ''
query = ''

# Functions
def main():

    # Variables
    database = databaseShell()

    # If something has been passed via standard input
    if not sys.stdin.isatty():
        global query
        for line in sys.stdin:
            stripped = line.strip()

            if stripped.startswith('--') or not stripped:
                # This is either a comment line in the sql file or an empty line, ignore it
                query = empty
                continue

            elif stripped.endswith(';'):
                query = query + ' ' + stripped

                # Get rid of space in the front of the query
                query= query[1:]
                database.onecmd(query)
                query = empty

            elif stripped == '.EXIT':
                print "Program ending"
                break

            else:
                query = query + ' ' + stripped

    else:
        print "Welcome to Assignment 2!"
        flag = True

        while flag:
            line = raw_input(":> ")

            if line == '.EXIT' or line == '.exit':
                flag = False

            elif line.endswith(';'):
                query = query + ' ' + line

                # Get rid of space in the front of the query
                query= query[1:]
                database.onecmd(query)

                # Clear query string
                query = empty

            else:
                query = query + ' ' + line

if __name__ == "__main__":
    main()
