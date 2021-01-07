import discord
from discord.ext import commands
import json
from tools import *

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
async def fr(ctx, arg):

    if ctx.author == bot.user or not arg:
        return

    message = ""

    with open('json/items.json') as items:
        itemList = json.load(items)        

    #Search for the given item name
    itemInstance = search_by_name(itemList, arg)
    if not itemInstance:
        await ctx.send('Item not found. Be sure to spell the item name correctly in quotes')
        return NOT_FOUND
    
    with open('json/recipes.json') as recipes:
        recipeList = json.load(recipes)

    #Check each of the recipes
    for recipeName in recipeNameList:

        #if the JSON doesn't have any recipes left then break
        if not itemInstance[recipeName]:
            if not message:
                await ctx.send("This item doesn't have any recipe")
            break

        #reset the output variable for the next possible recipe
        message = ""

        recipeInstance = search_by_id(recipeList, 0, len(recipeList), int(itemInstance[recipeName]))

        if not recipeInstance:
            return ERROR  

        with open('json/tables.json') as tables:
            tableList = json.load(tables)
            
        tableInstance = search_by_id(tableList, 0, len(tableList), int(recipeInstance['table']))

        message = message + ":hammer_pick: Item " + itemInstance['name'] + " is made on :hammer_pick:\n" + tableInstance['name'] + "\n"
        
        if tableInstance['alternate_name']:
            message = message + tableInstance['alternate_name'] + "\n"

        message = message + ":gear: and uses the following ingredients :gear:\n"             

        #Search for each of the ingredients
        for ingredientName, amountName in zip(ingredientNameList, amountNameList):

            #if the JSON doesn't have any ingredients left then break
            if not recipeInstance[ingredientName]:
                break

            ingredientInstance = search_by_id(itemList, 0, len(itemList), int(recipeInstance[ingredientName]))
            
            if not ingredientInstance:
                return ERROR

            message = message + recipeInstance[amountName] + " " + ingredientInstance['name'] + "\n"
        
        #Send the message to UI discord after all the ingredients were put into the ouput message variable
        await ctx.send(message)               

bot.run('Nzk2MDY1OTI0NzU1MDk1NTg0.X_SgKg.8UNAsVGPDnbS2nMc40LrpuoepTI')
