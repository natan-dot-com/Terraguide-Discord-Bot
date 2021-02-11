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

LOG_FILE_PATH = "recipes_log.txt"
RECIPE_JSON_PATH = "../../json/crafting_recipes.json"
ITEMS_JSON_PATH = "../../json/items.json"
TABLES_JSON_PATH = "../../json/tables.json"  

scrappingData = ["Result", "Ingredients"]

# Initialize both hash tables.
def initializeHashTables():
    itemList = LoadJSONFile(ITEMS_JSON_PATH)
    tableList = LoadJSONFile(TABLES_JSON_PATH)

    itemHash = hashTable(8192, SCRAPING_NAME)
    for itemInstance in itemList:
        itemHash.add(itemInstance[SCRAPING_NAME], itemInstance)

    tableHash = hashTable(64, "name")
    for tableInstance in tableList:
        tableHash.add(tableInstance["name"], tableInstance)

    return itemHash, tableHash

# Load HTML content from the table we're looking for.
def getTableContent(urlSuffix):
    URL = "https://terraria.gamepedia.com/" + urlSuffix
    html = requests.get(URL)
    soup = BeautifulSoup(html.content, 'html.parser')
    table = soup.find("table", class_="sortable")
    return table

def main():
    dictList = LoadJSONFile(RECIPE_JSON_PATH)
    itemHash, tableHash = initializeHashTables()
    
    try:
        logFile = open(LOG_FILE_PATH, "a")
        print("Error log file found.")
    except IOError:
        logFile = open(LOG_FILE_PATH, "w+")
        print("Error log file not found. A new one will be created.")
        
    urlSuffix = "By_Hand"

    table = getTableContent(urlSuffix)
    rows = table.findAll("tr")
    tableHead = getTableColumns(rows[0], scrappingData)

    recipeResult = ""
    recipeQty = ""
    recipesCounter = len(dictList)+1

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
                
        print(str(recipesCounter) + ": Scrapping '" + recipeResult + "' from '" + urlSuffix.replace("_", " ") + "'s page.")
        
        recipeDict[RECIPE_RESULT] =  itemHash.search(recipeResult, SCRAPING_ID)
        if recipeDict[RECIPE_RESULT] == NOT_FOUND:
            print("\tError detected. Please check the log file for more details.")
            logFile.write("RECIPE ERROR: Item '" + recipeResult + "' was not found in database. Maybe this item was already removed from/replaced in Terraria.\n")
            logFile.write("\tACTION: Recipe dictionary from '" + recipeResult + "' was removed from the list.\n\n")
            continue
            
        recipeDict[RECIPE_CRAFT_ID] = recipesCounter
        recipeDict[RECIPE_RESULT_QUANTITY] = recipeQty
        recipeDict[RECIPE_TABLE] = tableHash.search(urlSuffix.replace("_", " "), "id")
        
        # Getting the informations from 'Ingredients' column.
        
        # THE WORST (If there's not 'Result' class, the ingredient column is actually the first)
        if not row.find("td", class_="result"):
            ingredientRows = cols[tableHead["Result"]].findAll("li")
        else:
            ingredientRows = cols[tableHead["Ingredients"]].findAll("li")
        
        for ingredientRow in ingredientRows:
            ingredientDict = {
                INGREDIENT_NAME: "",
                INGREDIENT_QUANTITY: ""
            }
            ingredientDict[INGREDIENT_NAME] = itemHash.search(ingredientRow.a['title'], SCRAPING_ID)
            if ingredientDict[INGREDIENT_NAME] == NOT_FOUND:
                print("\tError detected. Please check the log file for more details.")
                logFile.write("INGREDIENT ERROR (" + str(recipesCounter) + "): Ingredient '" + ingredientRow.a['title'] + "' from '" + recipeResult + "' was not found.\n") 
                logFile.write("\tACTION: Ingredient ID replaced with NOT_FOUND value (-1). Need to be fixed outside the algorithm.\n\n")
                
            ingredientQty = ingredientRow.find("span", class_="note-text")
            if ingredientQty:
                ingredientDict[INGREDIENT_QUANTITY] = re.search("\d+", ingredientQty.text).group()
            else:
                ingredientDict[INGREDIENT_QUANTITY] = "1"
            recipeDict[RECIPE_IDENTITY].append(ingredientDict)
        dictList.append(recipeDict)
        recipesCounter += 1
    print("Successful operation. Exiting with value 0.")
    logFile.close()
    SaveJSONFile(RECIPE_JSON_PATH, dictList)

if __name__ == "__main__":
    main()
