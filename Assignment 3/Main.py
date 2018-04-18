# Authors: Amir Behmaram and Tanner Jones
# Date: 3/27/2018
# Version: 2.0

# Import Libraries
import atexit, json, sys
from Database import databaseShell
from GlobalVars import *

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

            # Call convert to lower to go through string and cast every reserved variable to lower
            cleanedString = convertToLower(stripped)

            if cleanedString.startswith('--') or not cleanedString:
                # This is either a comment line in the sql file or an empty line, ignore it
                query = empty
                continue

            elif cleanedString.endswith(';'):
                query = query + ' ' + cleanedString

                # Get rid of space in the front of the query
                query = query[1:]
                database.onecmd(query)
                query = empty

            elif stripped == '.EXIT':
                print "Program ending"
                break

            else:
                query = query + ' ' + stripped

    else:
        print "Welcome to Assignment 3!"
        flag = True

        while flag:
            line = raw_input(":> ")

            if line == '.EXIT' or line == '.exit':
                flag = False

            elif line.endswith(';'):
                query = query + ' ' + line

                # Get rid of space in the front of the query
                print query
                query = query[1:]
                database.onecmd(query)

                # Clear query string
                query = empty

            else:
                query = query + ' ' + line

def convertToLower(var):
    # Variables

    splitString = var.split(" ")
    newString = ""

    for word in splitString:
        splitFlag = False
        testStr = word

        # Try to split on '('
        tempStr = word.split("(")

        # If the split was successful, take the first value and use that as the testStr
        if len(tempStr) > 1:
            testStr = tempStr[0]
            splitFlag = True

        if testStr.isupper():
            if isReserved(testStr):
                testStr = testStr.lower()

        if(splitFlag):
            testStr = testStr + '(' + tempStr[1]

        newString = newString + " " + testStr

    # Get rid of space in the front of the string
    newString = newString[1:]

    return newString

def isReserved(var):
    # Variables
    reservedWords = ["CREATE", "USE", "DATABASE", "TABLE", "ALTER", "ADD", "DROP", "COLUMN",
                     "SELECT", "FROM", "INSERT", "INTO", "VALUES", "STAR", "EQUAL", "NOT_EQUAL", "GREATER",
                     "LESS", "GREATER_EQUAL", "LESS_EQUAL", "INNER", "JOIN", "LEFT", "OUTER"]
    flag = False

    for word in reservedWords:
        if var == word:
            flag = True
        else:
            pass

    return flag

if __name__ == "__main__":
    main()
