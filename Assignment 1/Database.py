# Import Libraries
import sys, os, shutil, json
from cmd import Cmd
from GlobalVars import *
from pprint import pprint

# Globals
DATABASE_DIR = os.getcwd() + "/Databases"
CURRENT_DB_DIR = DATABASE_DIR

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

        # Check syntax
        if not self.__checkSyntax(arg):
            return

        # Test to create database
        if arg.startswith(DATABASE):

            self.__dropDatabase(arg)

        elif arg.startswith(TABLE):

            #self.__dropTable(arg)
            print "hi"


    def do_USE(self, arg):

        # Variables
        global CURRENT_DB_DIR

        # Check syntax
        if not self.__checkSyntax(arg):
            return

        # If we aren't in the Database Directory, that means we are in
        # some other db, go back to home
        if CURRENT_DB_DIR != DATABASE_DIR:
                CURRENT_DB_DIR = DATABASE_DIR

        # Check for existence of DB user is trying to use already
        testPath = CURRENT_DB_DIR + "/" + arg[:-1]

        if os.path.exists(testPath):
            CURRENT_DB_DIR = testPath
        else:
            print "-- Error: No db with name " + arg[:-1] + " exists"

    # ALTER TABLE tab_1 ADD colName datatype, ALTER TABLE tab_1 DROP COLUMN colName, ALTER TABLE tab_1 ALTER COLUMN colName datatype
    def do_ALTER(self, arg):

        # Variables

        # Check syntax
        if not self.__checkSyntax(arg):
            return

        # If DB = DB DIR throw error No DB in use
        if CURRENT_DB_DIR == DATABASE_DIR:
            print "-- Error: No Database is being used"
            return

        # Get table name from current DB
        query = arg.split(" ")
        tableName = query[1]
        tableFile = CURRENT_DB_DIR + "/" + tableName + ".json"

        if not os.path.isfile(tableFile):
            print "-- Error: Table doesn't exist"
            return

        if query[2] == ADD:
            with open(tableFile, "r") as dataFile:
                data = json.load(dataFile)

            colName = query[3]
            val = query[4].replace(";", "")

            if colName in data:
                print "-- Error: Column already exists"
                return

            data[colName] = {"type": val, "data": []}

            with open(tableFile, "w") as dataFile:
                json.dump(data, dataFile)

        elif query[2] == DROP and query[3] == COLUMN:
            with open(tableFile, "r") as dataFile:
                data = json.load(dataFile)

            colName = query[4].replace(";", "")
            if colName in data:
                del data[colName]

                with open(tableFile, "w") as dataFile:
                    json.dump(data, dataFile)
            else:
                print "-- Error: No column with the name " + query[4] + " exists in the table"

        elif query[2] == ALTER and query[3] == COLUMN:
            with open(tableFile, "r") as dataFile:
                data = json.load(dataFile)

            colName = query[4]
            val = query[5].replace(";", "")
            colData = data.get("data")

            if colName in data:
                data[colName] = {"type": val, "data": [colData]}

                with open(tableFile, "w") as dataFile:
                    json.dump(data, dataFile)
            else:
                print "-- Error: No column with the name " + query[4] + " exists in the table"

        else:
            print "-- Error: Not a valid ALTER command"
            return

    def do_SELECT(self, arg):

        # Variables

        # If DB = DB DIR throw error No DB in use
        if CURRENT_DB_DIR == DATABASE_DIR:
            print "-- Error: No Database is being used"
            return

        # Get table name from current DB
        query = arg.split(" ")
        tableName = query[2].replace(";", "")
        tableFile = CURRENT_DB_DIR + "/" + tableName + ".json"

        if not os.path.isfile(tableFile):
            print "-- Error: Table doesn't exist"
            return

        # SLECT * FROM - Other variations that select specific columsn will be handled later
        if query[0] == "*" and query[1] == FROM:
            with open(tableFile, "r") as dataFile:
                data = json.load(dataFile)

            pprint(data)

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

    def __dropDatabase(self, arg):

        # Variables
        dbName = arg[:-1].split(" ")

        # Test for the correct syntax
        if not len(dbName) == 2 or dbName[1] == '':
            print "--!Failed: Incorrect Database Name"
            return

        # Place assign database
        dbName = dbName[1]

        # Create database folder
        if os.path.exists(dbName):
            shutil.rmtree(dbName)
            print "--!Succussful: Database " + dbName + " dropped."

        else:
            print "-- !Failed: Database " + dbName + " doesn't exist."
