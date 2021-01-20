from math import floor

recipeNameList = ['recipe1', 'recipe2', 'recipe3', 'recipe4', 'recipe5', 'recipe6']
ingredientNameList = ['ingredient1', 'ingredient2', 'ingredient3', 'ingredient4', 'ingredient5', 'ingredient6']
amountNameList = ['amount1', 'amount2', 'amount3', 'amount4', 'amount5', 'amount6']

NOT_FOUND = 0
ERROR = -1

botDescription = 'A terraria bot.'
botPrefix = 't.'

#Thumbnail for UI output commands
craftThumbNail = 'https://art.pixilart.com/7b7bd37bb742cd4.png'
listThumbNail = 'https://cdn2.iconfinder.com/data/icons/font-awesome/1792/search-512.png'
helpThumbNail = 'https://img2.gratispng.com/20180326/ytq/kisspng-question-mark-clip-art-competition-5ab8be3d0288c7.3002224515220567650104.jpg'

#Color for UI output commands
craftColor = 0x0a850e
listColor = 0xe40101
helpColor = 0x000000

#Output for help command
helpCommand = "Show this dialog"
craftCommand = "Show all recipes for an item"
listCommand  = "Find all items that contains the input word"

#Output Messages format
tableMessage = ":hammer_pick: **{}** is made on the following tables :hammer_pick:" 
craftMessage = ":gear: **{}** uses the following ingredients :gear:"
notFoundMessage = "Item {} doesn't have any recipe"
userRequestMessage = "User {} has requested a craft recipe for {}."

pageSize = 12

#Linear Search by Name
def searchByName(JSONData, name):
    for JSONInstance in JSONData:
        if JSONInstance['name'].lower() == name.lower():
            return JSONInstance
    return
