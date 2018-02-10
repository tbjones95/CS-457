# Import Libraries
import cmd, sys
from GlobalVars import *

class databaseShell(object):

    def parseUserCommands(self, input):

        # Variables

        # Test for correct syntax
        if not input == EXIT and not input.endswith(';'):
            print "-- !Failed: Wrong syntax."
            return None

        # Test for system commands
        if input == EXIT:
            return -1

        # Test for Database commands
        if input.startswith(CREATE_DATABASE)\
            or input.startswith(DELETE_DATABASE)\
            or input.startswith(USE_DATABASE):

            self.__databaseHandler(input)

        # Test for Table commands
        elif input.startswith(CREATE_TABLE)\
            or input.startswith(DROP_TABLE)\
            or input.startswith(ALTER_TABLE)\
            or input.startswith(SELECT):

            self.__tableHandler(input)

        elif input == "":
            return None

        else:
            print "-- !Failed: Incorrect command."
            return None

    def __databaseHandler(self, input):

        # Variables
        database = None
        

        #


        if not os.path.exists(directory):
            os.makedirs(directory)

    #def __tableHandler(self, input):

        # Variables
