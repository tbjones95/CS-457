# Import Libraries
import cmd, sys
from cmd import Cmd
from GlobalVars import *

class databaseShell(Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = ":> "
        self.intro  = "Welcome to Assignment 1!"

    def preloop(self):

        # Variables
        self._hist    = []
        self._locals  = {}
        self._globals = {}

        # Sets up command completion
        cmd.Cmd.preloop(self)

    def do_CREATE(self, arg):

        # Variables
        if not os.path.exists(directory):
            os.makedirs(directory)

    def do_DROP(self, arg):

        # Variables
        print "Drop"

    def do_USE(self, arg):

        # Variables
        print "USE"

    def do_ALTER(self, arg):

        # Variables
        print "ALTER"

    def do_SELECT(self, arg):

        # Variables
        print "SELECT"

    def emptyline(self):
        # Variables

        pass

    def do_EXIT(self, arg):

        # Variables

        return -1

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
