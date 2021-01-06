import json
from math import floor

NOT_FOUND = -1

recipeKeyList = ['recipe1', 'recipe2', 'recipe3', 'recipe4', 'recipe5', 'recipe6']
ingredientKeyList = ['ingredient1', 'ingredient2', 'ingredient3', 'ingredient4', 'ingredient5', 'ingredient6']
amountKeyList = ['amount1', 'amount2', 'amount3', 'amount4', 'amount5', 'amount6']

def binarySearch(JSONData, low, high, ID):
    if high >= low:
        mid = floor((high+low) // 2)
        if int(JSONData[mid]['id']) == ID:
            return JSONData[mid]
        elif int(JSONData[mid]['id']) > ID:
            return binarySearch(JSONData, low, mid-1, ID)
        elif int(JSONData[mid]['id']) < ID:
            return binarySearch(JSONData, mid+1, high, ID)
    return NOT_FOUND

def searchForItemRecipes(itemData, itemName):
    for itemIdentity in itemData:
        if itemIdentity['name'] == itemName:
            recipeIDList = []
            for recipeName in recipeKeyList:
                if len(itemIdentity[recipeName] > 0):
                    recipeIDList.append(itemIdentity[recipeName])
                else:
                    break
            return recipeIDList

def showCraftingTable(tableData, tableID):
    for tableIdentity in tableData:
        if tableIdentity['id'] == tableID:
            if len(tableIdentity['alternative_name'] > 0):
                return tableIdentity['name'], tableIdentity['alternative_name']
            else:
                return tableIdentity['name']
                
