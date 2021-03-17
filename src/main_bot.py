from os import chdir
from platform import system
if system() == "Linux":
    chdir("../")

import discord
import re
from discord.ext import commands
from package.json_manager import *
from package.item_hash import *
from package.bot_config import *
from package.search import *
from package.utility_dictionaries import *
from package.utility_functions import *
from package.embed_functions import *

bot = commands.Bot(command_prefix=botPrefix, description=botDescription, help_command=None)
itemList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + MAIN_NAME_FILE + JSON_EXT)
tableList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + TABLE_NAME_FILE + JSON_EXT)
rarityList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + RARITY_NAME_FILE + JSON_EXT)
itemHash = loadDependencies(itemList)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name=botPrefix + "help"))

@bot.command()
async def help(ctx):
    
    if ctx.author == bot.user:
        return

    embed = discord.Embed(color=helpColor, title="Command List")
    embed.set_thumbnail(url=helpThumbNail)
    embed.add_field(name=botPrefix + "help", value=helpCommand, inline=False)
    embed.add_field(name=botPrefix + "craft *Item Name*", value=craftCommand, inline=False)
    embed.add_field(name=botPrefix + "list  *Something to Search*", value=listCommand, inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def item(ctx, *args):

    # Checks empty argument
    arg = " ".join(args)
    if ctx.author == bot.user or not arg:
        return ARG_NOT_FOUND
    
    # Hash search the current item
    print('User ' + str(ctx.author) + ' has requested informations for ' + arg + '.')
    print(arg)
    itemID = itemHash.search(arg, LABEL_ID)
    print(itemID)
    if itemID == NOT_FOUND:
        await ctx.send("Can't find item '" + arg + "' in data base.")
        return ITEM_NOT_FOUND

    # Gets respective item info dictionary
    itemType = itemList[int(itemID)-1][LABEL_TYPE]
    itemFilePath = GLOBAL_JSON_PATH + DIR_ITEMS_DATA + itemFileManager[itemType] + JSON_EXT
    itemDict = binarySearch(LoadJSONFile(itemFilePath), itemID)
    if itemDict == NOT_FOUND:
        return ITEM_NOT_FOUND

    # Starts building each embed panel 
    embedList = []

    itemName = itemList[int(itemID)-1][LABEL_NAME]
    imageFilename = itemName.replace(" ", "_") + STATIC_IMAGE_EXT
    dominantImageColor = pickDominantColor(imageFilename)
    hasSource = False

    # Main info embed panel construction
    mainPage = discord.Embed(color=dominantImageColor, title="General informations about '" + itemName + "':")
    mainImage = discord.File(GLOBAL_IMAGE_PATH + imageFilename, filename="image.png")
    mainPage.set_thumbnail(url="attachment://image.png")
    for itemCategory in itemDict.keys():
        if itemCategory == LABEL_SOURCE:
            hasSource = True
            break
        elif itemCategory == LABEL_RARITY:
            embedInsertRarityField(mainPage, itemDict[itemCategory], rarityList)
        else:
            embedInsertField(mainPage, itemDict[itemCategory], itemCategory, inline=True)
    embedList.append(mainPage)

    # If item has source dict (i.e. if embed will have more than one page)
    if hasSource:

        # LABEL_SOURCE dict analysis
        nonEmptyLists = []
        for sourceCategory in itemDict[LABEL_SOURCE]:
            if itemDict[LABEL_SOURCE][sourceCategory]:
                nonEmptyLists.append(sourceCategory)

        pageAlert = "React to this message to switch between pages!\n"
        mainPage.set_footer(text=pageAlert + "Page 1/" + str(1+len(nonEmptyLists)))

        # Source embed panels creation
        recipesList = [] 
        npcList = []
        sellingList = []
        for existentCategory in nonEmptyLists:
            newEmbed = None

            # Recipes embed panel cration
            if existentCategory == SOURCE_RECIPES:
                if not recipesList:
                    recipesList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + RECIPE_NAME_FILE + JSON_EXT)
                titleMessage = "Showing craft recipes for '" + itemName + "':"
                newEmbed = discord.Embed(title=titleMessage, color=dominantImageColor)
                newEmbed.set_thumbnail(url="attachment://image.png")
                createRecipesPanel(itemList, tableList, recipesList, itemDict[LABEL_SOURCE][SOURCE_RECIPES], newEmbed)
                newEmbed.set_footer(text="Page " + str(2+nonEmptyLists.index(existentCategory)) + "/" + str(1+len(nonEmptyLists)))

            elif existentCategory == SOURCE_NPC:
                if not npcList:
                    npcList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + NPC_NAME_FILE + JSON_EXT)
                if not sellingList:
                    sellingList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + SELLING_LIST_NAME_FILE + JSON_EXT)
                titleMessage = "Showing selling offers for '" + itemName + "':"
                newEmbed = discord.Embed(title=titleMessage, color=dominantImageColor)
                newEmbed.set_thumbnail(url="attachment://image.png")
                createSellingPanel(itemList, npcList, sellingList, itemDict[LABEL_SOURCE][SOURCE_NPC], newEmbed, itemName)
                newEmbed.set_footer(text="Page " + str(2+nonEmptyLists.index(existentCategory)) + "/" + str(1+len(nonEmptyLists)))

            else:
                continue
            embedList.append(newEmbed)

    currentEmbed = 0
    botMessage = await ctx.send(file=mainImage, embed=embedList[currentEmbed])

    # Page system manager (if number of pages greater than one)
    if len(embedList) > 1:
        await botMessage.add_reaction('◀')
        await botMessage.add_reaction('▶')

        def check(reaction, user):
            return user != botMessage.author and reaction.message.id == botMessage.id

        reaction = None
        while True:
            if str(reaction) == '◀':
                if currentEmbed > 0:
                    currentEmbed -= 1
                    await botMessage.edit(embed = embedList[currentEmbed])
                elif currentEmbed == 0:
                    currentEmbed = len(embedList) - 1
                    await botMessage.edit(embed = embedList[currentEmbed])
            elif str(reaction) == '▶':
                if currentEmbed < len(embedList) - 1:
                    currentEmbed += 1
                    await botMessage.edit(embed = embedList[currentEmbed])
                elif currentEmbed == len(embedList) - 1:
                    currentEmbed = 0
                    await botMessage.edit(embed = embedList[currentEmbed])
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout = 20.0, check = check)
                await botMessage.remove_reaction(reaction, user)
            except:
                break
            
        await botMessage.clear_reactions()



# Old bot commands
# Shows a list of  every item which starts with 'arg'
@bot.command()
async def list(ctx, *args):

    arg = " ".join(args)
    if ctx.author == bot.user or not arg:
        return

    print('User ' + str(ctx.author) + ' has requested a list of items for ' + arg + '.')

    matchCounter = 0
    matchList = [[]]
    itemList = LoadJSONFile(GLOBAL_JSON_PATH + MAIN_NAME_FILE + JSON_EXT)

    #Regex usage to find every match of the input
    for itemInstance in itemList:
        if re.search("^" + arg + "+", itemInstance['name'], re.IGNORECASE): 
            #print("^" + arg + "*\n" + itemInstance['name'] + "\n")
            if len(matchList[len(matchList)-1]) >= pageSize:
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
        newPage.set_footer(text="Page " + str(matchList.index(matchInstance) + 1) + "/" + str(len(matchList)))
        pageList.append(newPage)

    # Changing page system via Discord reactions
    pageNumber = 0
    botMessage = await ctx.send(embed = pageList[pageNumber])
    await botMessage.add_reaction('◀')
    await botMessage.add_reaction('▶')

    def check(reaction, user):
        return user != botMessage.author and reaction.message.id == botMessage.id

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
async def craft(ctx, *args):

    arg = " ".join(args)

    if ctx.author == bot.user or not arg:
        return

    print('User ' + str(ctx.author) + ' has requested a craft recipe for ' + arg + '.')

    itemList = LoadJSONFile(GLOBAL_JSON_PATH + MAIN_NAME_FILE + JSON_EXT)
    recipeList = LoadJSONFile(GLOBAL_JSON_PATH + RECIPE_NAME_FILE + JSON_EXT)
    tableList = LoadJSONFile(GLOBAL_JSON_PATH + TABLE_NAME_FILE + JSON_EXT)

    #Search for the given item name
    itemInstance = searchByName(itemList, arg)
    if not itemInstance:
        await ctx.send('Item not found. Be sure to spell the item name correctly.')
        return NOT_FOUND

    title = "Craft info about " + itemInstance['name']
    embed = discord.Embed(color=craftColor, title=title)
    embed.set_thumbnail(url=craftThumbNail)
    
    #Check each of the recipes
    for recipeName in recipeNameList:

        #If the JSON doesn't have any recipes left then break
        if not itemInstance[recipeName]:
            if recipeName == 'recipe1':
                await ctx.send("Item " + itemInstance['name'] + " doesn't have any recipe")
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
