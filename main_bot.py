import discord
import json
import re
from discord.ext import commands
from tools import *
from json_manager import *

bot = commands.Bot(command_prefix='.', description=botDescription, help_command=None)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def help(ctx):
    
    if ctx.author == bot.user:
        return

    embed = discord.Embed(color=helpColor, title="Command List")
    embed.set_thumbnail(url=helpThumbNail)
    embed.add_field(name="$help", value=helpCommand, inline=False)
    embed.add_field(name="$craft \"Item Name\"", value=craftCommand, inline=False)
    embed.add_field(name="$list  \"Something to Search\"", value=listCommand, inline=False)
    
    await ctx.send(embed=embed)

# Shows a list of  every item which starts with 'arg'
@bot.command()
async def list(ctx, arg):

    if ctx.author == bot.user or not arg:
        return

    print('User ' + str(ctx.author) + ' has requested a list of items for ' + arg + '.')

    matchCounter = 0
    matchList = [[]]
    itemList = LoadJSONFile(ITEM_FILE_PATH)

    #Regex usage to find every match of the input
    for itemInstance in itemList:
        if re.search("^" + arg + "*", itemInstance['name'], re.IGNORECASE): 
            if len(matchList[len(matchList)-1]) >= 12:
                matchList.append([])
            matchList[len(matchList)-1].append(itemInstance['name'])
    
    for matchInstance in matchList:
        matchCounter += len(matchInstance)
    if matchCounter == 0:
        await ctx.send("No items were found containing " + arg)
        return NOT_FOUND

    description = str(matchCounter) + " occurrencies found:\n"

    # Pages creation with 12 lines each
    pageList = []
    for matchInstance in matchList:
        message = ""
        for subInstance in matchInstance:
            message += subInstance + "\n"
            
        newPage = discord.Embed (
            title = "Search Info about " + arg,
            colour = discord.Colour.green(),
        )
        newPage.add_field(name=description, value=message, inline=False)
        newPage.set_footer(text="page " + str(matchList.index(matchInstance) + 1) + "/" + str(len(matchList)))
        pageList.append(newPage)

    # Changing page system via Discord reactions
    pageNumber = 0
    botMessage = await ctx.send(embed = pageList[pageNumber])
    await botMessage.add_reaction('◀')
    await botMessage.add_reaction('▶')

    def check(reaction, user):
        return user == ctx.author

    reaction = None
    while True:
        if str(reaction) == '◀':
            if pageNumber > 0:
                pageNumber -= 1
                await botMessage.edit(embed = pageList[pageNumber])
            elif pageNumber == 0:
                pageNumber = len(pageList) - 1
                await botMessage.edit(embed = pageList[pageNumber])
        elif str(reaction) == '▶':
            if pageNumber < len(pageList) - 1:
                pageNumber += 1
                await botMessage.edit(embed = pageList[pageNumber])
            elif pageNumber == len(pageList) - 1:
                pageNumber = 0
                await botMessage.edit(embed = pageList[pageNumber])
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout = 30.0, check = check)
            await botMessage.remove_reaction(reaction, user)
        except:
            break
        
    await botMessage.clear_reactions()

# Shows crafting information about 'arg'
@bot.command()
async def craft(ctx, arg):

    if ctx.author == bot.user or not arg:
        return

    print('User ' + str(ctx.author) + ' has requested a craft recipe for ' + arg + '.')

    itemList = LoadJSONFile(ITEM_FILE_PATH)
    recipeList = LoadJSONFile(RECIPE_FILE_PATH)
    tableList = LoadJSONFile(TABLE_FILE_PATH)

    #Search for the given item name
    itemInstance = searchByName(itemList, arg)
    if not itemInstance:
        await ctx.send('Item not found. Be sure to spell the item name correctly in quotes')
        return NOT_FOUND

    title = "Craft info about " + itemInstance['name']
    embed = discord.Embed(color=craftColor, title=title)
    embed.set_thumbnail(url=craftThumbNail)
    
    #Check each of the recipes
    for recipeName in recipeNameList:

        #If the JSON doesn't have any recipes left then break
        if not itemInstance[recipeName]:
            if recipeName == 'recipe1':
                await ctx.send("item " + itemInstance['name'] + " doesn't have any recipe")
            break
        
        #Clearing everything
        messageTable = ""
        messageCraft = ""
        descriptionTable = ""
        descriptionCraft = ""
        embed.clear_fields()
        
        recipeInstance = recipeList[int(itemInstance[recipeName]) - 1]
        if not recipeInstance:
            print('(ERROR) recipeInstance is an empty variable.\n')
            return ERROR  
        
        tableInstance = tableList[int(recipeInstance['table']) - 1]
        if not tableInstance:
            print('(ERROR) tableInstance is an empty variable.\n')
            return ERROR
        
        #Get table infos
        descriptionTable = ":hammer_pick: **" + itemInstance['name'] + "** is made on the following tables :hammer_pick:" 
        if tableInstance['alternate_name']:
            messageTable = tableInstance['name'] + ", " + tableInstance['alternate_name']
        else:
            messageTable = tableInstance['name']
        
        embed.add_field(name=descriptionTable, value=messageTable, inline=False)
        descriptionCraft += ":gear: **" + itemInstance['name'] + "** uses the following ingredients :gear:"             
        
        #Get the ingredients
        for ingredientName, amountName in zip(ingredientNameList, amountNameList):
            
            #if the JSON doesn't have any ingredients left then break
            if not recipeInstance[ingredientName]:
                break
                
            ingredientInstance = itemList[int(recipeInstance[ingredientName]) - 1]
            if not ingredientInstance:
                print('(ERROR) ingredientInstance is an empty variable.\n')
                return ERROR
                
            messageCraft += recipeInstance[amountName] + " " + ingredientInstance['name'] + ", "
            
        #remove the last comma
        messageCraft = messageCraft[:-2]
        
        #Send the message to UI discord
        embed.add_field(name=descriptionCraft, value=messageCraft, inline=False)
        await ctx.send(embed=embed)               

#bot.run('MjQ2NTExOTcxMDY5ODUzNjk3.WCVcKQ.quxR1uO0TUb6UQPhvLYzqoApHBI')
bot.run('Nzk2MDY1OTI0NzU1MDk1NTg0.X_SgKg.8UNAsVGPDnbS2nMc40LrpuoepTI')
