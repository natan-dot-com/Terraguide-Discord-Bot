import discord
import json
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
    
    await ctx.send('```Command List:\n$fr "ItemName" -> Search for the recipe of an item```')

@bot.command()
async def craft(ctx, arg):

    if ctx.author == bot.user or not arg:
        return

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
                await ctx.send("This item doesn't have any recipe")
            break

        #reset the output variable for the next possible recipe
        message = ""

        recipeInstance = searchByID(recipeList, 0, len(recipeList), int(itemInstance[recipeName]))
        if not recipeInstance:
            return ERROR  

        tableInstance = searchByID(tableList, 0, len(tableList), int(recipeInstance['table']))
        if not tableInstance:
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

            ingredientInstance = searchByID(itemList, 0, len(itemList), int(recipeInstance[ingredientName]))
            if not ingredientInstance:
                return ERROR

            message += recipeInstance[amountName] + " " + ingredientInstance['name'] + "\n"
        
        #Send the message to UI discord after all the ingredients were put into the ouput message variable
        await ctx.send(message)               

bot.run('Nzk2MDY1OTI0NzU1MDk1NTg0.X_SgKg.8UNAsVGPDnbS2nMc40LrpuoepTI')
