import discord
import json
import re
from discord.ext import commands
from tools import *
from json_manager import *

bot = commands.Bot(command_prefix='$', description=description, help_command=None)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def help(ctx):
    
    if ctx.author == bot.user:
        return
    
    await ctx.send('```Command List:\n$craft "ItemName" -> Search for the recipe of an item```')

# Shows a list of  every item which starts with 'arg'
@bot.command()
async def list(ctx, arg):

    if ctx.author == bot.user or not arg:
        return

    print(str(ctx.author) + ' has requested a list of items for ' + arg + '.')

    message = ""
    matchCounter = 0
    itemList = LoadJSONFile(ITEM_FILE_PATH)

    #Regex usage to find every match of the input
    for itemInstance in itemList:
        if re.search("^" + arg + "*", itemInstance['name'], re.IGNORECASE): 
            message += itemInstance['name'] + "\n"
            matchCounter += 1
    
    await ctx.send(str(matchCounter) + " occurrencies found:\n" + message)

# Shows crafting information about 'arg'
@bot.command()
async def craft(ctx, arg):

    if ctx.author == bot.user or not arg:
        return

    print(str(ctx.author) + ' has requested a craft recipe for ' + arg + '.')

    message = ""
    itemList = LoadJSONFile(ITEM_FILE_PATH)
    recipeList = LoadJSONFile(RECIPE_FILE_PATH)
    tableList = LoadJSONFile(TABLE_FILE_PATH)

    #Search for the given item name
    itemInstance = searchByName(itemList, arg)
    if not itemInstance:
        await ctx.send('Item not found. Be sure to spell the item name correctly in quotes')
        return NOT_FOUND
    
    #Check each of the recipes
    for recipeName in recipeNameList:

        #if the JSON doesn't have any recipes left then break
        if not itemInstance[recipeName]:
            if not message:
                await ctx.send("item " + itemInstance['name'] + " doesn't have any recipe")
            break

        #reset the output variable for the next possible recipe
        message = ""

        recipeInstance = recipeList[int(itemInstance[recipeName]) - 1]
        if not recipeInstance:
            print('(ERROR) recipeInstance is an empty variable.\n')
            return ERROR  

        tableInstance = tableList[int(recipeInstance['table']) - 1]
        if not tableInstance:
            print('(ERROR) tableInstance is an empty variable.\n')
            return ERROR

        message += ":hammer_pick: Item " + itemInstance['name'] + " is made on :hammer_pick:\n" + tableInstance['name'] + "\n"
        if tableInstance['alternate_name']:
            message += tableInstance['alternate_name'] + "\n"
        message += ":gear: and uses the following ingredients :gear:\n"             

        #Search for each of the ingredients
        for ingredientName, amountName in zip(ingredientNameList, amountNameList):

            #if the JSON doesn't have any ingredients left then break
            if not recipeInstance[ingredientName]:
                break

            ingredientInstance = itemList[int(recipeInstance[ingredientName]) - 1]
            if not ingredientInstance:
                print('(ERROR) ingredientInstance is an empty variable.\n')
                return ERROR

            message += recipeInstance[amountName] + " " + ingredientInstance['name'] + "\n"
        
        #Send the message to UI discord after all the ingredients were put into the ouput message variable
        await ctx.send(message)               

bot.run('MjQ2NTExOTcxMDY5ODUzNjk3.WCVcKQ.quxR1uO0TUb6UQPhvLYzqoApHBI')