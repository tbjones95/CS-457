# Authors: Amir Behmaram and Tanner Jones
# Date: 2/22/2018
# Version: 1.0

# Import Libraries
import sys, os, shutil, json, re
from cmd import Cmd
from time import gmtime, strftime
from GlobalVars import *
from pprint import pprint
from collections import OrderedDict

# Globals
DATABASE_DIR = os.getcwd() + "/Databases"
CURRENT_DB_DIR = DATABASE_DIR
DB_NAME = ""
QUERY_STRING = ""

class databaseShell(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = ":> "
        self.intro  = "Welcome to Assignment 2!"

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

        # If we are adding a column
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

        # If we are dropping a column
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

        # If we are altering a columns contents
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

        # Otherwise it is a bad alter command, throw error then exit
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

    def do_insert(self, arg):
        # Variables

        # Check syntax
        if not self.__checkSyntax(arg):
            return

        # If DB = DB DIR throw error No DB in use
        if CURRENT_DB_DIR == DATABASE_DIR:
            print "-- !Failed: No Database is being used"
            return

        # The following three steps are to clear out any unwanted characters
        # from the insert command. This will wipe out any tabs, new lines, etc.
        # It does maintain spaces however, since the JSON .dump wipes out spaces
        # before inserting them.

        # First replace all spaces with a temporary character &
        tempStr = arg.replace(' ', '&')

        # Second strip all tabs, spaces, endlines etc
        tempStrTwo = "".join(tempStr.split())

        # Third replace all special characters with spaces
        tempStrThree = tempStrTwo.replace('&', ' ')

        # Finally, split on spaces
        query = tempStrThree.split(' ')

        tableName = query[1]
        tableFile = CURRENT_DB_DIR + "/" + tableName + ".json"

        # If into isnt immediately after throw error and exit, not a valid command.
        if query[0] != INTO:
            print "-- Failed: Incorrect INSERT statement, missing INTO"
            return

        # If the table doesnt exist throw an error then exit
        if not os.path.isfile(tableFile):
            print "-- !Failed: Table doesn't exist"
            return

        # If the command following the table name is Values, continue
        if query[2].startswith(VALUES):

            # Get just the values by splitting the string on the (
            temp = tempStrThree.split('(')

            # Split the values up
            values = temp[1].split(',')

            # Before we do anything else, clean up the last value by removing the
            # trailing );
            values[len(values) - 1] = values[len(values) - 1][:-2]
            valIndex = 0

            # Open the table and get the data
            with open(tableFile, "r") as dataFile:
                data = json.load(dataFile, object_pairs_hook=OrderedDict)

                # Loop through the table and insert the new information to each column
                for key, value in data.items():

                    # Clean up variable before adding
                    cleanVar = self.__cleanVariable(values[valIndex])

                    # Convert to the proper datatype based on the type
                    newVal = self.__convertInputValue(cleanVar, value['Datatype'])

                    # Append to table
                    value['Data'].append(newVal)
                    valIndex += 1

            # Dump information back into the table file
            with open(tableFile, "w") as dataFile:
                json.dump(data, dataFile, indent = 4)
                print "-- Success: 1 new record inserted"

        else:
            print "-- Failed: Missing VALUES from INSERT command"
            return

    def do_select(self, arg):

        # Variables
        columnList = None
        tableName = None
        tablePath = None
        condition = None
        data = None
        count = None
        tableHeader = None
        rowList = None

        # Check if database has been selected
        if CURRENT_DB_DIR == DATABASE_DIR:
            print "-- !Failed: No Database is being used"
            return

        # Strip what columns the user wants
        arg = arg[:-1].split(" from ")

        # Test for the correct syntax
        if not len(arg) == 2:
            print "-- !Failed: Incorrect select syntax"
            return

        # Strip column list
        columnList = arg[0].split(", ")

        # Strip the where statement
        arg = arg[1].split(" where ")

        if len(arg) == 2:
            condition = arg[1]

        # Assign table name
        tableName = arg[0]
        tablePath = CURRENT_DB_DIR + "/" + tableName + ".json"

        # Test to see if the table exist
        if not os.path.exists(tablePath):
            print "-- !Failed: No Table with name " + tableName + " exists"
            return

        # Gather table data
        with open(tablePath, 'r') as table:
            data = json.load(table, object_pairs_hook=OrderedDict)

        # Gather column list for *
        if columnList[0].startswith(STAR):

            columnList = []

            # Create table header and get column lists
            for column, datatype in data.iteritems():

                columnList.append(column)

        # Gather table results
        tableHeader, rowList = self.__gatherTableData(columnList, data, condition)

        # Print results
        print "-- " + tableHeader

        for count in range(len(rowList)):

            print "-- " + rowList[count]

    def do_update(self, arg):

        # Variables
        tableName = None
        tablePath = None
        data = None
        startingValue = None
        endingValue = None
        recordsChanged = None

        # Check if database has been selected
        if CURRENT_DB_DIR == DATABASE_DIR:
            print "-- !Failed: No Database is being used"
            return

        # Strip what columns the user wants
        arg = arg[:-1].split(" set ")

        # Test for the correct syntax
        if not len(arg) == 2:
            print "-- !Failed: Incorrect select syntax"
            return

        # Get table name and build the path to the table
        tableName = arg[0]
        tablePath = CURRENT_DB_DIR + "/" + tableName + ".json"

        # Test to see if the table exist
        if not os.path.exists(tablePath):
            print "-- !Failed: No Table with name " + tableName + " exists"
            return

        # Strip the where statement
        arg = arg[1].split(" where ")

        # Test for the correct syntax
        if not len(arg) == 2:
            print "-- !Failed: Incorrect select syntax"
            return

        startingValue = arg[0]
        endingValue = arg[1]

        # Gather table data
        with open(tablePath, 'r') as table:
            data = json.load(table, object_pairs_hook=OrderedDict)

        recordsChanged = self.__UpdateTable(data, startingValue, endingValue)

        # Update table data
        with open(tablePath, 'w') as table:
            json.dump(data, table, indent = 4, sort_keys = True)

        # Print results
        print "-- " + str(recordsChanged) + " record modified."

    def do_delete(self, arg):

        # Variables
        tableName = None
        tablePath = None
        condition = None
        data = None
        columnList = None
        recordsChanged = None

        # Check if database has been selected
        if CURRENT_DB_DIR == DATABASE_DIR:
            print "-- !Failed: No Database is being used"
            return

        # Start striping away the command
        arg = arg[:-1].split("from ")

        # Test for the correct syntax
        if not len(arg) == 2:
            print "-- !Failed: Incorrect select syntax"
            return

        # Strip the tables name and condition
        arg = arg[1].split(" where ")

        # Test for the correct syntax
        if not len(arg) == 2:
            print "-- !Failed: Incorrect select syntax"
            return

        # Assign the table name and table path
        tableName = arg[0]
        tablePath = CURRENT_DB_DIR + "/" + tableName + ".json"

        # Test to see if the table exist
        if not os.path.exists(tablePath):
            print "-- !Failed: No Table with name " + tableName + " exists"
            return

        # Assign the condition of deleting
        condition = arg[1]

        # Gather table data
        with open(tablePath, 'r') as table:
            data = json.load(table, object_pairs_hook=OrderedDict)

        columnList = []

        # Gather all columns within the table
        for column, datatype in data.iteritems():

            columnList.append(column)

        recordsChanged = self.__deleteData(data, condition, columnList)

        # Update table data
        with open(tablePath, 'w') as table:
            json.dump(data, table, indent = 4, sort_keys = True)

        # Print results
        print "-- " + str(recordsChanged) + " records deleted."

    def do_EXIT(self, arg):

        # Variables
        # This is depracated since we got rid of the command shell, leaving it in in case we go back to it
        return -1

    def emptyline(self):

        # Variables

        pass

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
        tableInfo = OrderedDict()

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
            json.dump(tableInfo, outfile, indent = 4)

        # Add table to database file
        with open(databaseFile, 'r') as outfile:
            databaseInfo = json.load(outfile)

        databaseInfo["Tables"].append(arg[1])

        with open(databaseFile, 'w') as outfile:
            json.dump(databaseInfo, outfile, indent = 4, sort_keys = True)

        print "-- Success: Table " + tableName + " created"

    # This function tests whether any create commadn has the correect syntax.
    # If it doesn't it will return false and the create function will be terminated
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

    def __gatherTableData(self, columnList, data, condition):

        # Variables
        count = None
        dataSize = None
        tableHeader = ""
        rowStatement = None
        rowList = []
        column = None
        operator = None
        value = None

        # Create table header and get column lists
        for count in range(len(columnList)):

            dataSize = len(data[columnList[count]]["Data"])

            tableHeader += columnList[count] + " (" + data[columnList[count]]["Datatype"] + ") | "

        # Parse condition statement
        if not condition == None:
            column, operator, value = self.__parseWhereStatements(condition)

            value = self.__convertInputValue(value, data[column]["Datatype"])

        # Gather data from each column
        for count in range(dataSize):

            rowStatement = ""

            if not condition == None:

                if operator == EQUAL:

                    if not data[column]["Data"][count] == value:
                        continue

                if operator == NOT_EQUAL:

                    if not data[column]["Data"][count] != value:
                        continue

                if operator == GREATER:

                    if not data[column]["Data"][count] > value:
                        continue

                if operator == LESS:

                    if not data[column]["Data"][count] < value:
                        continue

                if operator == GREATER_EQUAL:

                    if not data[column]["Data"][count] >= value:
                        continue

                if operator == LESS_EQUAL:

                    if not data[column]["Data"][count] <= value:
                        continue

            for dataIndex in range(len(columnList)):

                rowStatement += str(data[columnList[dataIndex]]["Data"][count]) + " | "

            rowList.append(rowStatement[:-2])

        return tableHeader[:-2], rowList

    def __UpdateTable(self, data, startingValue, endingValue):

        # Variables
        setColumn = None
        setOperator = None
        setValue = None
        conditionColumn = None
        conditionOperator = None
        conditionValue = None
        dataSize = None
        count = None
        recordsChanged = 0

        # Parse both set and condition statements
        setColumn, setOperator, setValue = self.__parseWhereStatements(startingValue)
        conditionColumn, conditionOperator, conditionValue = self.__parseWhereStatements(endingValue)

        # Remove quotes from both values
        setValue = setValue.replace("'", "")
        setValue = self.__convertInputValue(setValue, data[setColumn]["Datatype"])
        conditionValue = conditionValue.replace("'", "")
        conditionValue = self.__convertInputValue(conditionValue, data[conditionColumn]["Datatype"])

        # Get data size
        dataSize = len(data[conditionColumn]["Data"])

        # Loop through column which is being tested
        for count in range(dataSize):

            if data[conditionColumn]["Data"][count] == conditionValue:
                data[setColumn]["Data"][count] = setValue
                recordsChanged += 1

        # Return results
        return recordsChanged

    def __deleteData(self, data, condition, columnList):

        # Variables
        column = None
        operator = None
        value = None
        dataSize = None
        count = 0
        recordsChanged = 0

        # Parse the conditional statement
        column, operator, value = self.__parseWhereStatements(condition)

        # Remove quotes from both values
        value = value.replace("'", "")
        value = self.__convertInputValue(value, data[column]["Datatype"])

        # Get data size
        dataSize = len(data[column]["Data"])

        # Gather data from each column
        while count < dataSize:

            if operator == EQUAL:

                if not data[column]["Data"][count] == value:
                    count += 1
                    continue

            elif operator == NOT_EQUAL:

                if not data[column]["Data"][count] != value:
                    count += 1
                    continue

            elif operator == GREATER:

                if not data[column]["Data"][count] > value:
                    count += 1
                    continue

            elif operator == LESS:

                if not data[column]["Data"][count] < value:
                    count += 1
                    continue

            elif operator == GREATER_EQUAL:

                if not data[column]["Data"][count] >= value:
                    count += 1
                    continue

            elif operator == LESS_EQUAL:

                if not data[column]["Data"][count] <= value:
                    count += 1
                    continue


            for dataIndex in range(len(columnList)):

                data[columnList[dataIndex]]["Data"].pop(count)

            dataSize -= 1
            recordsChanged += 1

        return recordsChanged

    def __parseWhereStatements(self, condition):

        # Variables
        column = None
        operator = None
        value = None

        condition = condition.split(" ")

        column = condition[0]
        operator = condition[1]
        value = condition[2]

        return column, operator, value

    def __convertInputValue(self, value, datatype):

        # Variables

        # Test for the correct datatype
        if datatype.startswith("varchar"):
            return str(value)

        elif datatype.startswith("int"):
            return int(value)

        elif datatype.startswith("float"):
            return float(value)

    def __cleanVariable(self,arg):

        # Variables

        # The arg given will be any variable, remove any unneeded characters, spaces, and tabs
        cleanVar = "".join(arg.split())

        cleanVar = cleanVar.replace("'", "")

        return cleanVar
