import discord
from discord.ext import commands
import json

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
                for recipeInstance in recipeList:
                    if recipeInstance['id'] == itemInstance['recipe1']:
                        message = message + ":hammer_pick: Item " + itemInstance['name'] + " is made by using :hammer_pick:\n"
                        if len(recipeInstance['ingredient1']) > 0:
                            for itemInstance in itemList:
                                if itemInstance['id'] == recipeInstance['ingredient1']:
                                    message = message + recipeInstance['amount1'] + " " + itemInstance['name'] + "\n"
                                    break
                        if len(recipeInstance['ingredient2']) > 0:
                            for itemInstance in itemList:
                                if itemInstance['id'] == recipeInstance['ingredient2']:
                                    message = message + recipeInstance['amount2'] + " " + itemInstance['name'] + "\n"
                                    break
                        break
                await ctx.send(message)
                return
                break
        await ctx.send('Recipe not found')

bot.run('MjQ2NTExOTcxMDY5ODUzNjk3.WCVcKQ.quxR1uO0TUb6UQPhvLYzqoApHBI')
