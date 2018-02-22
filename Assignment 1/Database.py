# Import Libraries
import sys, os, shutil, json
from cmd import Cmd
from time import gmtime, strftime
from GlobalVars import *
from pprint import pprint

# Globals
DATABASE_DIR = os.getcwd() + r"\Databases"
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

            self.__createTable(arg)

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
        testPath = CURRENT_DB_DIR + "\\" + arg[:-1]

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
        tableFile = CURRENT_DB_DIR + "\\" + tableName + ".json"

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
                json.dump(data, dataFile, indent = 4, sort_keys = True)

        elif query[2] == DROP and query[3] == COLUMN:
            with open(tableFile, "r") as dataFile:
                data = json.load(dataFile)

            colName = query[4].replace(";", "")
            if colName in data:
                del data[colName]

                with open(tableFile, "w") as dataFile:
                    json.dump(data, dataFile, indent = 4, sort_keys = True)
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
                    json.dump(data, dataFile, indent = 4, sort_keys = True)
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
        tableFile = CURRENT_DB_DIR + "\\" + tableName + ".json"

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
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        databaseInfo = None
        databaseDir = None
        database = None

        # Test for the correct syntax
        if not len(dbName) == 2 or dbName[1] == '':
            print "--!Failed: Incorrect Database Name"
            return

        # Place assign database
        dbName = dbName[1]
        databasePath = DATABASE_DIR + "\\" + dbName + "\\"

        # Check for a database folder
        if os.path.exists(databasePath):
            print "-- !Failed: Database " + dbName + " already exists."
            return

        # Create a database folder
        os.makedirs(os.path.dirname(databasePath))

        # Pull database information
        databaseInfo = {
                        "Database Name" : dbName,
                        "Date" : date,
                        "Tables" : []
                        }

        # Dump database information into json file
        with open(databasePath + dbName + ".json", 'w') as outfile:
            json.dump(databaseInfo, outfile, indent = 4, sort_keys = True)

    def __dropDatabase(self, arg):

        # Variables
        dbName = arg[:-1].split(" ")

        # Test for the correct syntax
        if not len(dbName) == 2 or dbName[1] == '':
            print "--!Failed: Incorrect Database Name"
            return

        # Place assign database
        dbName = dbName[1]

        # Check for a database folder
        if not os.path.exists(dbName):
            print "-- !Failed: Database " + dbName + " doesn't exist."
            return

        shutil.rmtree(dbName)
        print "--!Succussful: Database " + dbName + " dropped."

    def __createTable(self, arg):

        # Variables
        databaseFile = CURRENT_DB_DIR + "\\" + os.path.basename(CURRENT_DB_DIR) + ".json"
        databaseInfo = None
        tablePath = None
        columnList = None
        columns = []
        count = None
        tableInfo = {}

        # Split the arguments
        arg = arg[:-1].split(' ', 2)

        # Test for correct syntax
        if not len(arg) == 3 or arg[1] == '' or arg[2] == '':
            print "--!Failed: Incorrect Table Name"
            return

        if not arg[2].startswith('(') or not arg[2].endswith(')'):
            print "--!Failed: Incorrect Column Configurations"
            return

        # Check if database has been selected
        if CURRENT_DB_DIR == DATABASE_DIR:
            print "-- Error: No Database is being used"
            return

        # Assign column list and table name
        tablePath = CURRENT_DB_DIR + "\\" + arg[1] + ".json"
        columnList = arg[2][1:-1]
        columnList = columnList.split(', ')

        # Test if table already exist
        if os.path.exists(tablePath):
            print "-- !Failed: Table " + arg[1] + " already exists."
            return

        # Loop through each columns
        for count in range(len(columnList)):

            columns = columnList[count].split(' ')

            # Check for correct datatype
            if not columns[1] in DATATYPES:
                print  "-- !Failed: Datatype '" + columns[1] + "' incorrect type."
                return

            # TODO: Check for equal amount of ()

            tableInfo.update({
                                columns[0] : {
                                    "Datatype" : columns[1],
                                    "Data" : []
                                }
                            })

        # Dump table information into json file
        with open(tablePath, 'w') as outfile:
            json.dump(tableInfo, outfile, indent = 4, sort_keys = True)

        # Add table to database file
        with open(databaseFile, 'r') as outfile:
            databaseInfo = json.load(outfile)

        databaseInfo["Tables"].append(arg[1])

        with open(databaseFile, 'w') as outfile:
            json.dump(databaseInfo, outfile, indent = 4, sort_keys = True)
