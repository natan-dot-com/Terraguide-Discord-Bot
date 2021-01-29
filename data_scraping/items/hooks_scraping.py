import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
from bs4 import BeautifulSoup
import re
import requests

ITEM_ID_COLUMN = 1
SOURCE_COLUMN = 2
REACH_COLUMN = 3
VELOCITY_COLUMN = 4
HOOKS_COLUMN = 5
LATCHING_COLUMN = 6
RARITY_COLUMN = 8

JSON_PATH = "items_hooks.json"
hooksDictList = []

URL = "https://terraria.gamepedia.com/Hooks"
html = requests.get(URL)
soup = BeautifulSoup(html.content, 'html.parser')
tables = []
tables.append(soup.find("table", { "id" : "Hooks-Pre-Hardmode-table" }))
tables.append(soup.find("table", { "id" : "Hooks-Hardmode-table" }))
for table in tables:
    rows = table.findAll("tr")
    for row in rows[1::]:
        hooksDict = {
            SCRAPING_ITEM_ID: "",
            SCRAPING_REACH: "",
            SCRAPING_VELOCITY: "",
            SCRAPING_HOOKS: "",
            SCRAPING_LATCHING: "",
            SCRAPING_RARITY: "",
            SCRAPING_SOURCE: ""
        }
        cols = row.findAll("td")
        
        # Scraping all the trivial information
        hooksDict[SCRAPING_ITEM_ID] = (re.search("\d+", cols[ITEM_ID_COLUMN].find("div", class_="id").text)).group()
        hooksDict[SCRAPING_REACH] = cols[REACH_COLUMN].text.replace("\n", "")
        hooksDict[SCRAPING_VELOCITY] = cols[VELOCITY_COLUMN].text.replace("\n", "")
        hooksDict[SCRAPING_HOOKS] = cols[HOOKS_COLUMN].text.replace("\n", "")
        hooksDict[SCRAPING_LATCHING] = cols[LATCHING_COLUMN].text.replace("\n", "")
        hooksDict[SCRAPING_RARITY] = (re.search("\d+", cols[RARITY_COLUMN].span.a['title'])).group()
        
        sourceDict = {
            "Drop" : "",
            "NPC" : "",
            "Recipe" : "",
            "Other" : ""
        }
        
        # Splitting string to prevent inconsistences
        stringsList = re.split(" or |\n", cols[SOURCE_COLUMN].text)
        print(stringsList)
        for instance in stringsList:
            
            # Check to prevent breakline madness
            if instance:
                
                # If the source is a drop, it will be done together with its specified json (therefore there's no need to do it here)
                # The drop's ID will be put in the 'Drop' dict key later on.
                if (re.search("%", instance)):
                    continue
                
                # If the source is a crafting recipe, it's needed to put it in the recipes json and get its reference ID
                if (re.search("^Crafted:", instance)):
                    quantityList = re.search("(?<=Crafted:).*$", instance).group().replace(" ", "").split("+")
                    imageList = cols[SOURCE_COLUMN].findAll('img')

                    ingredientList = []
                    for imageInstance in imageList:
                        ingredientList.append(imageInstance['alt'])

                    recipeList = []
                    for ingredient, quantity in zip(ingredientList, quantityList):
                        recipeDict = {
                            "Ingredient": "", 
                            "Quantity": ""
                        }
                        recipeDict['Ingredient'] = ingredient
                        if not quantity:
                            quantity = "1"
                        recipeDict['Quantity'] = quantity
                        recipeList.append(recipeDict)
                    # PLACEHOLDER: RecipeList will eventually be on the crafting recipe json
                    # The recipe's ID will be put in the 'Recipe' dict key later on.
                    sourceDict['Recipe'] = recipeList
                    
                # If the source is an NPC, it's needed to get its respective ID.
                elif (re.search("\(", instance)):
                    # PLACEHOLDER: NPC's name will be in the dictionary while the NPC json isn't done
                    sourceDict['NPC'] = re.search(".+?(?=\()", instance).group().rstrip().replace("\n", "")
                    
                # If it's none of the above, we can just put it directly in the 'Other' dict key as open-text.
                else:
                    sourceDict['Other'] = instance.rstrip().replace("\n", "")
            
        hooksDict[SCRAPING_SOURCE] = sourceDict
        hooksDictList.append(hooksDict)

SaveJSONFile(JSON_PATH, sorted(hooksDictList, key = lambda i: int(i['Item ID'])))
