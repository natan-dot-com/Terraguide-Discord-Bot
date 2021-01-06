import discord
from discord.ext import commands
import json
from search import binary_search

recipeNameList = ['recipe1', 'recipe2', 'recipe3', 'recipe4', 'recipe5', 'recipe6']
ingredientNameList = ['ingredient1', 'ingredient2', 'ingredient3', 'ingredient4', 'ingredient5', 'ingredient6']
amountNameList = ['amount1', 'amount2', 'amount3', 'amount4', 'amount5', 'amount6']

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def fr(ctx, arg):

    if ctx.author == bot.user or not arg:
        return

    message = ""

    with open('json/items.json') as items:
        itemList = json.load(items)        

        for itemInstance in itemList:
            
            if itemInstance['name'] == arg:
                with open('json/recipes.json') as recipes:
                    recipeList = json.load(recipes)

                for recipeName in recipeNameList:
                    if itemInstance[recipeName]:
                        recipeInstance = binary_search(recipeList, 0, len(recipeList), int(itemInstance[recipeName]))
                
                        if recipeInstance:
                            message = message + ":hammer_pick: Item " + itemInstance['name'] + " is made by using :hammer_pick:\n"
                        else:
                            break   

                        for ingredientName, amountName in zip(ingredientNameList, amountNameList):
                            if recipeInstance[ingredientName]:
                                ingredientInstance = binary_search(itemList, 0, len(itemList), int(recipeInstance[ingredientName]))
                                if ingredientInstance:
                                    message = message + recipeInstance[amountName] + " " + ingredientInstance['name'] + "\n"
                                else:
                                    break
                        
                        await ctx.send(message)
                    
                    else:
                        break

                    message = ""
                return
        
        await ctx.send('Recipe not found')
        
        '''for recipeInstance in recipeList:
                    #Search for recipe
                    if recipeInstance['id'] == itemInstance['recipe1']:
                        message = message + ":hammer_pick: Item " + itemInstance['name'] + " is made by using :hammer_pick:\n"
                        if len(recipeInstance['ingredient1']) > 0:

                            for itemInstance in itemList:
                                #Search for ingredient 1
                                if itemInstance['id'] == recipeInstance['ingredient1']:
                                    message = message + recipeInstance['amount1'] + " " + itemInstance['name'] + "\n"
                                    break
                        if len(recipeInstance['ingredient2']) > 0:

                            for itemInstance in itemList:
                                #Search for ingredient 2
                                if itemInstance['id'] == recipeInstance['ingredient2']:
                                    message = message + recipeInstance['amount2'] + " " + itemInstance['name'] + "\n"
                                    break
                        break
                await ctx.send(message)
                return
                break
        await ctx.send('Recipe not found')'''

bot.run('MjQ2NTExOTcxMDY5ODUzNjk3.WCVcKQ.quxR1uO0TUb6UQPhvLYzqoApHBI')
