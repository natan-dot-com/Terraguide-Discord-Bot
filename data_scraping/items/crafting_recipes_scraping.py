import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
from bs4 import BeautifulSoup
from item_hash import *
import re
import requests

# Constant values
MAIN_ITEM_FILE_PREFIX = "items_"
MAIN_CRAFTING_STATION_SUFFIX = "/Crafting_stations"
TERRARIA_TABLE_CLASS = "terraria"
SORTABLE_TABLE_CLASS = "sortable"

LOG_EXT = ".log"
DEFAULT_LOG_PATH = "logs/recipes_"
ITEMS_JSON_PATH = GLOBAL_JSON_PATH + MAIN_NAME_FILE + JSON_EXT
RECIPE_JSON_PATH = GLOBAL_JSON_PATH + RECIPE_NAME_FILE + JSON_EXT

TUPLE_TABLE_NAME = 0
TUPLE_TABLE_URL = 1

scrappingData = ["Result", "Ingredients"]
nameSubstitutes = {
    "Any Wood": "Wood",
    "Any Iron Bar": "Iron Bar",
    "Any Pressure Plate": "Brown Pressure Plate",
    "Any Bird": "Bird",
    "Any Butterfly": "Julia Butterfly",
    "Any Bug": "Buggy",
    "Any Duck": "Duck",
    "Any Firefly": "Firefly",
    "Any Scorpion": "Scorpion",
    "Any Snail": "Snail",
    "Any Squirrel": "Squirrel"
}
javascriptTables = ["/Work_Bench", "/Placed_Bottle", "/Alchemy_Table", "/Extractinator"]

# Initialize both hash tables.
def initializeHashTables(itemList):
    tableList = LoadJSONFile(GLOBAL_JSON_PATH + TABLE_NAME_FILE + JSON_EXT)

    itemHash = hashTable(ITEMS_HASH_SIZE, SCRAPING_NAME)
    for itemInstance in itemList:
        itemHash.add(itemInstance[SCRAPING_NAME], itemInstance)

    tableHash = hashTable(TABLES_HASH_SIZE, SCRAPING_NAME)
    for tableInstance in tableList:
        tableHash.add(tableInstance[SCRAPING_NAME], tableInstance)

    return itemHash, tableHash

# Loads HTML content from the table we're looking for.
def getTableContent(urlSuffix, tableClass):
    URL = "https://terraria.gamepedia.com" + urlSuffix
    html = requests.get(URL)
    soup = BeautifulSoup(html.content, 'html.parser')
    table = soup.findAll("table", class_=tableClass)
    return table

def feedWriteStructure(itemList, recipeDict, writeFileStructure):
    itemIndex = int(recipeDict[RECIPE_RESULT])-1
    itemType = itemList[itemIndex][SCRAPING_TYPE]
    if itemType not in writeFileStructure.keys():
        writeFileStructure[itemType] = {}
    if itemIndex+1 not in writeFileStructure[itemType].keys():
        writeFileStructure[itemType][itemIndex+1] = []
    writeFileStructure[itemType][itemIndex+1].append(recipeDict[RECIPE_CRAFT_ID])

# Algorithm to get the recipe's ID and refers it inside each JSON-data file.
def insertRecipeOnJSON(writeFileStructure, itemList, logFile):
    print("\nInitiating writing process...")
    for itemType in writeFileStructure.keys():
        filenameSuffix = itemType.lower().replace(" ", "_")
        filename = GLOBAL_JSON_PATH + MAIN_ITEM_FILE_PREFIX + filenameSuffix + JSON_EXT
        try:
            with open(filename) as outputFile:
                JSONList = LoadJSONFile(filename)
            for itemID_Structure in writeFileStructure[itemType].keys():
                for JSONInstance in JSONList:
                    if int(JSONInstance[SCRAPING_ITEM_ID]) == int(itemID_Structure):
                        for recipeID in writeFileStructure[itemType][itemID_Structure]:
                            if recipeID in JSONInstance[SCRAPING_SOURCE][SOURCE_RECIPES]:
                                print("\tRecipe ID " + recipeID + " is already on file. Not writing.")
                            else:
                                JSONInstance[SCRAPING_SOURCE][SOURCE_RECIPES].append(recipeID)
                        break
            SaveJSONFile(filename, JSONList)
        except IOError:
            print("File '" + filename + "' not found. Aborting proccess.")
            logFile.write("Can't reach '" + filename + "'. No such file or directory.\n\n")

# Scraps every recipe from a table in specified suffix.
def getCraftingRecipes(stationTuple, craftDictList, itemList, itemHash, tableHash, recipesCounter):
    writeFileStructure = {}
    print("Starting processing '" + stationTuple[TUPLE_TABLE_NAME] + "'s page...")
    
    tableList = getTableContent(stationTuple[TUPLE_TABLE_URL], SORTABLE_TABLE_CLASS)
    for tableInstance in tableList:
        if tableInstance.find("caption"):
            table = tableInstance
            break

    rows = table.findAll("tr")
    tableHead = getTableColumns(rows[0], scrappingData)

    logFilePath = DEFAULT_LOG_PATH + stationTuple[TUPLE_TABLE_NAME].lower().replace(" ", "_") + LOG_EXT
    logFile = open(logFilePath, "w+")
    print("Creating new log file for '"+ stationTuple[TUPLE_TABLE_NAME] + "'.")
    logFile.write("Starting log file for '" + stationTuple[TUPLE_TABLE_NAME] + "'.\n")
        
    recipeResult = ""
    recipeQty = ""

    tableID = tableHash.search(stationTuple[TUPLE_TABLE_NAME], SCRAPING_TABLE_ID)
    if tableID == NOT_FOUND:
        print("Table ID for '" + stationTuple[TUPLE_TABLE_NAME] + "' not found. Aborting Process.")
        logFile.write("TABLE ERROR: Table ID not found. Aborted proccess.\n")
        logFile.write("Execution failed returning value 1.\n")
        logFile.close()
        return
    else:
        logFile.write("Table ID (" + tableID + ") found. Starting execution.\n\n")

    for row in rows[1::]:
        recipeDict = {
            RECIPE_CRAFT_ID: "",
            RECIPE_RESULT: "",
            RECIPE_RESULT_QUANTITY: "",
            RECIPE_TABLE: "",
            RECIPE_IDENTITY: []
        } 
        cols = row.findAll("td")
        
        # Getting the informations from 'Result' column.
        
        # If it exists, recipeResult will be updated. The same happens with recipeQty.
        if row.find("td", class_="result"):
            recipeResult = cols[tableHead["Result"]].img['alt']
                
            if cols[tableHead["Result"]].find("span", class_="note-text"):
                recipeQty = re.search("\d+", cols[tableHead["Result"]].find("span", class_="note-text").text).group()
            else:
                recipeQty = "1"
                
        print(str(recipesCounter) + ": Scrapping '" + recipeResult + "' from '" + stationTuple[TUPLE_TABLE_NAME] + "'s page.")
        
        recipeDict[RECIPE_RESULT] =  itemHash.search(recipeResult, SCRAPING_ID)
        if recipeDict[RECIPE_RESULT] == NOT_FOUND:
            print("\tError detected. Please check the log file for more details.")
                
            logFile.write("RECIPE WARNING: Item '" + recipeResult + \
                "' was not found in database. Maybe this item was already removed from/replaced in Terraria.\n")
                
            logFile.write("\tACTION: Recipe dictionary from '" + recipeResult + "' was removed from the list.\n\n")
            continue
            
        recipeDict[RECIPE_CRAFT_ID] = str(recipesCounter)
        recipeDict[RECIPE_RESULT_QUANTITY] = recipeQty
        recipeDict[RECIPE_TABLE] = tableID
        
        # Getting the informations from 'Ingredients' column.
        
        # THE WORST (If there's not 'Result' class, the ingredient column is actually the first one)
        if not row.find("td", class_="result"):
            ingredientRows = cols[0].findAll("li")
        else:
            ingredientRows = cols[tableHead["Ingredients"]].findAll("li")
        
        for ingredientRow in ingredientRows:
            ingredientDict = {
                INGREDIENT_NAME: "",
                INGREDIENT_QUANTITY: ""
            }
            ingredientName = ingredientRow.a['title']
            if ingredientName in nameSubstitutes:
                ingredientName = nameSubstitutes[ingredientName]

            ingredientDict[INGREDIENT_NAME] = itemHash.search(ingredientName, SCRAPING_ID)
            if ingredientDict[INGREDIENT_NAME] == NOT_FOUND:
                print("\tError detected. Please check the log file for more details.")
                logFile.write("INGREDIENT ERROR (" + str(recipesCounter) + "): Ingredient '" + ingredientRow.a['title'] + \
                    "' from '" + recipeResult + "' was not found.\n")
                logFile.write("\tACTION: Ingredient ID replaced with NOT_FOUND value (-1). Need to be fixed outside the algorithm.\n\n")
                
            ingredientQty = ingredientRow.find("span", class_="note-text")
            if ingredientQty:
                ingredientDict[INGREDIENT_QUANTITY] = re.search("\d+", ingredientQty.text).group()
            else:
                ingredientDict[INGREDIENT_QUANTITY] = "1"
            recipeDict[RECIPE_IDENTITY].append(ingredientDict)
        craftDictList.append(recipeDict)
        feedWriteStructure(itemList, recipeDict, writeFileStructure)
        recipesCounter += 1
            
    insertRecipeOnJSON(writeFileStructure, itemList, logFile)
    
    print("Successful operation. Exiting with value 0.\n")
    logFile.write("Successful operation. Exiting with value 0.\n")
    logFile.close()

def getTableLinks():
    stationLinks = []
    craftingStationTables = getTableContent(MAIN_CRAFTING_STATION_SUFFIX, TERRARIA_TABLE_CLASS) 
    for craftingTable in craftingStationTables:
        rows = craftingTable.findAll("tr")
        for row in rows[1::]:
            tableColumn = row.find("td")
            if tableColumn.find("span", class_="i"):
                for tableSpan in tableColumn.findAll("span", class_="i"):
                    # StationTuple = (Table_Name, Table_URL)
                    stationTuple = (tableSpan.a['title'], tableSpan.a['href'])
                    stationLinks.append(stationTuple)
            else:
                stationLinks.append((tableColumn.a['title'], tableColumn.a['href']))
    return stationLinks
            
def main():
    craftDictList = []
    recipeCounter = 1
    itemList = LoadJSONFile(ITEMS_JSON_PATH)
    itemHash, tableHash = initializeHashTables(itemList)
    stationTupleList = getTableLinks()
    for stationTuple in stationTupleList:
        # adm corno
        if stationTuple[TUPLE_TABLE_URL] not in javascriptTables:
            getCraftingRecipes(stationTuple, craftDictList, itemList, itemHash, tableHash, recipeCounter)
            recipeCounter = len(craftDictList)+1
    SaveJSONFile(RECIPE_JSON_PATH, craftDictList)

if __name__ == "__main__":
    main()
