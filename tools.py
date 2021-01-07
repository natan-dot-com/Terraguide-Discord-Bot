from math import floor

recipeNameList = ['recipe1', 'recipe2', 'recipe3', 'recipe4', 'recipe5', 'recipe6']
ingredientNameList = ['ingredient1', 'ingredient2', 'ingredient3', 'ingredient4', 'ingredient5', 'ingredient6']
amountNameList = ['amount1', 'amount2', 'amount3', 'amount4', 'amount5', 'amount6']

NOT_FOUND = 0
ERROR = -1

description = 'A terraria bot.'

#Binary Search by ID
def searchByID(JSONData, low, high, ID):
    if high >= low:
        mid = floor((high + low) // 2)
        if int(JSONData[mid]['id']) == ID:
            return JSONData[mid]
        elif int(JSONData[mid]['id']) > ID:
            return searchByID(JSONData, low, mid-1, ID)
        elif int(JSONData[mid]['id']) < ID:
            return searchByID(JSONData, mid+1, high, ID)
    return

#Linear Search by Name
def searchByName(JSONData, name):
    for JSONInstance in JSONData:
        if JSONInstance['name'].lower() == name.lower():
            return JSONInstance
    return
