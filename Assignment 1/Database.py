# Import Libraries
import sys, os, shutil, json
from cmd import Cmd
from time import gmtime, strftime
from GlobalVars import *
from pprint import pprint

# Globals
DATABASE_DIR = os.getcwd() + "/Databases"
CURRENT_DB_DIR = DATABASE_DIR
DB_NAME = ""

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
        if not self.__testCreateSyntax(arg):
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

            self.__dropTable(arg)

    def do_USE(self, arg):

        # Variables
        global CURRENT_DB_DIR
        dbName = arg[:-1]
        global DB_NAME
        DB_NAME = dbName

        # Check syntax
        if not self.__checkSyntax(arg):
            return

        # If we aren't in the Database Directory, that means we are in
        # some other db, go back to home
        if CURRENT_DB_DIR != DATABASE_DIR:
                CURRENT_DB_DIR = DATABASE_DIR

        # Check for existence of DB user is trying to use already
        testPath = CURRENT_DB_DIR + "/" + dbName

        if os.path.exists(testPath):
            CURRENT_DB_DIR = testPath
            print "-- Success: Database " + dbName + " is in use"
        else:
            print "-- !Failed: No db with name " + dbName + " exists"

    # ALTER TABLE tab_1 ADD colName datatype, ALTER TABLE tab_1 DROP COLUMN colName, ALTER TABLE tab_1 ALTER COLUMN colName datatype
    def do_ALTER(self, arg):

        # Variables

        # Check syntax
        if not self.__checkSyntax(arg):
            return

        # If DB = DB DIR throw error No DB in use
        if CURRENT_DB_DIR == DATABASE_DIR:
            print "-- !Failed: No Database is being used"
            return

        # Get table name from current DB
        query = arg.split(" ")
        tableName = query[1]
        tableFile = CURRENT_DB_DIR + "/" + tableName + ".json"

        if not os.path.isfile(tableFile):
            print "-- !Failed: Table doesn't exist"
            return

        if query[2] == ADD:
            with open(tableFile, "r") as dataFile:
                data = json.load(dataFile)

            colName = query[3]
            val = query[4].replace(";", "")

            if colName in data:
                print "-- !Failed: Column already exists"
                return

            data[colName] = {"type": val, "data": []}

            with open(tableFile, "w") as dataFile:
                json.dump(data, dataFile, indent = 4, sort_keys = True)
                print "-- Success: Column " + colName + " " + val + " added to table"

        elif query[2] == DROP and query[3] == COLUMN:
            with open(tableFile, "r") as dataFile:
                data = json.load(dataFile)

            colName = query[4].replace(";", "")
            if colName in data:
                del data[colName]

                with open(tableFile, "w") as dataFile:
                    json.dump(data, dataFile, indent = 4, sort_keys = True)
                    print "-- Success: Column " + colName + " " + val + " dropped from table"
            else:
                print "-- !Failed: No column with the name " + query[4] + " exists in the table"

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
                    print "-- Success: Column " + colName + " altered to " + val
            else:
                print "-- !Failed: No column with the name " + query[4] + " exists in the table"

        else:
            print "-- !Failed: Not a valid ALTER command"
            return

    def do_SELECT(self, arg):

        # Variables

        # If DB = DB DIR throw error No DB in use
        if CURRENT_DB_DIR == DATABASE_DIR:
            print "-- !Failed: No Database is being used"
            return

        # Get table name from current DB
        query = arg.split(" ")
        tableName = query[2].replace(";", "")
        tableFile = CURRENT_DB_DIR + "/" + tableName + ".json"

        if not os.path.isfile(tableFile):
            print "-- !Failed: Table doesn't exist"
            return

        # SLECT * FROM - Other variations that select specific columsn will be handled later
        if query[0] == "*" and query[1] == FROM:
            with open(tableFile, "r") as dataFile:
                data = json.load(dataFile)

            print "-- Success:"
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

        # Place assign database
        dbName = dbName[1]
        databasePath = DATABASE_DIR + "/" + dbName + "/"

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

        print "-- Success: Database " + dbName + " created"

    def __dropDatabase(self, arg):

        # Variables
        dbName = arg[:-1].split(" ")

        # Test for the correct syntax
        if not len(dbName) == 2 or dbName[1] == '':
            print "-- !Failed: Incorrect Database Name"
            return

        # Place assign database
        dbPath = DATABASE_DIR + "/" + dbName[1]

        # Check for a database folder
        if not os.path.exists(dbPath):
            print "-- !Failed: Database " + dbName[1] + " doesn't exist."
            return

        shutil.rmtree(dbPath)
        print "-- Succuss: Database " + dbName[1] + " dropped."

    def __createTable(self, arg):

        # Variables
        databaseFile = CURRENT_DB_DIR + "/" + os.path.basename(CURRENT_DB_DIR) + ".json"
        databaseInfo = None
        tablePath = None
        columnList = None
        column = []
        count = None
        tableInfo = {}

        # Split the arguments
        arg = arg[:-1].split(' ', 2)
        tableName = arg[1]

        # Test for correct syntax
        if not len(arg) == 3 or arg[1] == '' or arg[2] == '':
            print "-- !Failed: Incorrect Table Name"
            return

        if not arg[2].startswith('(') or not arg[2].endswith(')'):
            print "-- !Failed: Incorrect Column Configurations"
            return

        # Check if database has been selected
        if CURRENT_DB_DIR == DATABASE_DIR:
            print "-- !Failed: No Database is being used"
            return

        # Assign column list and table name
        tablePath = CURRENT_DB_DIR + "/" + tableName + ".json"
        columnList = arg[2][1:-1]
        columnList = columnList.split(', ')

        # Test if table already exist
        if os.path.exists(tablePath):
            print "-- !Failed: Table " + tableName + " already exists."
            return

        # Loop through each columns
        for count in range(len(columnList)):

            column = columnList[count].split(' ')

            if column[0] == "" or column[0] == " ":
                print "-- !Failed: Incorrect syntax."
                return False

            if not self.__testDataTypes(column[1]):
                return

            tableInfo.update({
                                column[0] : {
                                    "Datatype" : column[1],
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

        print "-- Success: Table " + tableName + " created"

    def __testCreateSyntax(self, command):

        # Variables
        cmdCompents = None

        if not command.endswith(';'):
            print "-- !Failed: Incorrect syntax."
            return False

        # Break command down into different pieces
        cmdCompents = command[:-1].split(' ', 2)

        # Test for either Database or Table
        if cmdCompents[0] == "TABLE":

            if not len(cmdCompents) == 3:
                print "-- !Failed: Incorrect syntax."
                return False

            if cmdCompents[1] == " " or cmdCompents[2] == " ":
                print "-- !Failed: Incorrect syntax."
                return False

            if not cmdCompents[2].startswith('(') or not cmdCompents[2].endswith(')'):
                print "-- !Failed: Incorrect syntax."
                return False

            return True

        if cmdCompents[0] == "DATABASE":

            # Test for the correct syntax
            if not len(cmdCompents) == 2:
                print "-- !Failed: Incorrect syntax."
                return False

            if cmdCompents[1] == " ":
                print "-- !Failed: Incorrect syntax."
                return False

            return True

        print "-- !Failed: Unknown command '" + cmdCompents[0] + "'."
        return False

    def __testDataTypes(self, datatype):

        # Variables
        size = None

        # Test for INT and FLOAT
        if datatype == "int" or datatype == "float":
            return True

        # Test for VARCHAR and CHAR
        if ((datatype.startswith("varchar(") or datatype.startswith("char(")) and datatype.endswith(")")):

            size = datatype[:-1].split("(")[1]

            try:
                val = int(size)
            except ValueError:
                print "-- !Failed: Incorrect datatype size."
                return False

            return True

        # Incorrect datatype was used
        print "-- !Failed: Incorrect datatype used."
        return False

    def __dropTable(self, arg):

        # Variables
        arg = arg[:-1].split(' ', 2)
        tableName = arg[1]
        tablePath = CURRENT_DB_DIR + "/" + tableName + ".json"
        dbTablePath = CURRENT_DB_DIR + "/" + DB_NAME + ".json"

        # Check if table exists in current DB and remove from the folder
        if os.path.exists(tablePath):
            os.remove(tablePath)

            # Delete the table from the databases file as well
            with open(dbTablePath, "r") as tableFile:
                data = json.load(tableFile)

                if tableName in data["Tables"]:
                    data["Tables"].remove(tableName)
                else:
                    print "-- !Failed: table doesn't exist in database file"

            with open(dbTablePath, 'w') as tableFile:
                json.dump(data, tableFile, indent = 4, sort_keys = True)

            # Report success
            print "-- Success: Table " + tableName + " dropped"

        # If table does exist, delete the Failed
        else:
            print "-- !Failed: Table " + tableName + " doesn't exist"
