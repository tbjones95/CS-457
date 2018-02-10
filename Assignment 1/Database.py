# Import Libraries
import sys, os
from cmd import Cmd
from GlobalVars import *

class databaseShell(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = ":> "
        self.intro  = "Welcome to Assignment 1!"

    def preloop(self):

        # Variables
        self._hist    = []
        self._locals  = {}
        self._globals = {}

        # Sets up command completion
        Cmd.preloop(self)

    def default(self, arg):

        # Variables

        print "-- !Failed: Incorrect command."

    def do_CREATE(self, arg):

        # Variables

        # Check syntax
        if not self.__checkSyntax(arg):
            return

        # Test to create database
        if arg.startswith(DATABASE):

            self.__createDatabase(arg)

        elif arg.startswith(TABLE):

            self.__createTable

    def do_DROP(self, arg):

        # Variables
        print "Drop"

        # Check syntax
        if not self.__checkSyntax(arg):
            return

    def do_USE(self, arg):

        # Variables
        print "USE"

        # Check syntax
        if not self.__checkSyntax(arg):
            return

    def do_ALTER(self, arg):

        # Variables
        print "ALTER"

        # Check syntax
        if not self.__checkSyntax(arg):
            return

    def do_SELECT(self, arg):

        # Variables
        print "SELECT"

        # Check syntax
        if not self.__checkSyntax(arg):
            return

    def emptyline(self):
        # Variables

        pass

    def do_EXIT(self, arg):

        # Variables

        return -1

    def __checkSyntax(self, arg):

        # Variables

        if not arg.endswith(';'):

            print "-- !Failed: Wrong syntax."
            return False

        return True

    def __createDatabase(self, arg):

        # Variables
        dbName = arg[:-1].split(" ")

        # Test for the correct syntax
        if not len(dbName) == 2 or dbName[1] == '':
            print "--!Failed: Incorrect Database Name"
            return

        # Place assign database
        dbName = dbName[1]

        # Create database folder
        if not os.path.exists(dbName):
            os.makedirs(dbName)
            print "--!Succussful: Database " + dbName + " created."

        else:
            print "-- !Failed: Database " + dbName + " already exists."
