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
recipesList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + RECIPE_NAME_FILE + JSON_EXT)
tablesList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + TABLE_NAME_FILE + JSON_EXT)
setList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + SET_NAME_FILE + JSON_EXT)
itemHash = loadDependencies(itemList)
setHash = loadDependencies(setList, SET_HASH_SIZE, LABEL_SET_NAME)

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
    for command, commandDescription in zip(commandList.keys(), commandList.values()):
        embedInsertField(embed, commandDescription, command, inline=False)  
    await ctx.send(embed=embed)

@bot.command()
async def item(ctx, *args):

    # Checks empty argument
    arg = " ".join(args)
    if ctx.author == bot.user or not arg:
        return ARG_NOT_FOUND
    
    # Hash search the current item
    print("User {} has requested a craft recipe for {}.".format(str(ctx.author), arg))
    itemID = itemHash.search(arg, LABEL_ID)
    if itemID == -1:
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
            else:
                pass
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
                reaction, user = await bot.wait_for('reaction_add', timeout = 30.0, check = check)
                await botMessage.remove_reaction(reaction, user)
            except:
                break
            
        await botMessage.clear_reactions()


# Shows a list of  every item which starts with 'arg'
@bot.command()
async def list(ctx, *args):

    arg = " ".join(args)
    if ctx.author == bot.user or not arg:
        return

    print("User {} has requested a craft recipe for {}.".format(str(ctx.author), arg))
    matchCounter = 0
    matchList = [[]]

    #Regex usage to find every match of the input
    for itemInstance in itemList:
        if re.search("^" + arg + "+", itemInstance[LABEL_NAME], re.IGNORECASE): 
            if len(matchList[len(matchList)-1]) >= pageSize:
                matchList.append([])
            matchList[len(matchList)-1].append(itemInstance[LABEL_NAME])
    
    for matchInstance in matchList:
        matchCounter += len(matchInstance)
    if matchCounter == 0:
        await ctx.send("No items were found containing " + arg)
        return NOT_FOUND

    listDescription = str(matchCounter) + " occurrencies found:\n"
    # Pages creation with 12 lines each
    pageList = []
    for matchInstance in matchList:
        listMessage = ""
        for subInstance in matchInstance:
            listMessage += subInstance + "\n"
            
        newPage = discord.Embed(title ="Search Info about " + arg, colour=discord.Colour.green())
        embedInsertField(newPage, listMessage, listDescription, inline=False)
        embedSetFooter(newPage, "Page " + str(matchList.index(matchInstance) + 1) + "/" + str(len(matchList)))
        pageList.append(newPage)

    #Send Message
    botMessage = await ctx.send(embed = pageList[0])

    # Changing page system via Discord reactions
    await embedSetReactions(bot, botMessage, pageList)

# Probably will be removed
# Shows crafting information
@bot.command()
async def craft(ctx, *args):

    arg = " ".join(args)
    if ctx.author == bot.user or not arg:
        return
    print("User {} has requested a craft recipe for {}.".format(str(ctx.author), arg))

    #Find input in hash table
    itemID = itemHash.search(arg, LABEL_ID)
    if itemID == -1:
        await ctx.send("Can't find item '{}' in data base.".format(arg))
        return ITEM_NOT_FOUND

    itemType = itemList[int(itemID)-1][LABEL_TYPE]
    itemFilePath = GLOBAL_JSON_PATH + DIR_ITEMS_DATA + itemFileManager[itemType] + JSON_EXT
    itemName = itemList[int(itemID)-1][LABEL_NAME]
    imageFilename = itemName.replace(" ", "_").lower() + STATIC_IMAGE_EXT
    dominantImageColor = pickDominantColor(imageFilename)
    craftTitle = "Craft information about '{}':".format(itemName)
    embedImage = discord.File(GLOBAL_IMAGE_PATH + imageFilename, filename="image.png")
    itemDict = binarySearch(LoadJSONFile(itemFilePath), itemID)

    embedPage = discord.Embed(color=dominantImageColor, title=craftTitle)
    embedPage.set_thumbnail(url="attachment://image.png")

    itemRecipes = itemDict[LABEL_SOURCE][SOURCE_RECIPES]
    for craftingRecipeIndex in range(len(itemRecipes)):
        ingredients = recipesList[int(itemRecipes[craftingRecipeIndex])-1][RECIPE_IDENTITY]
        tableId = int(recipesList[int(itemRecipes[craftingRecipeIndex])-1][RECIPE_TABLE])
        tableName = tablesList[tableId-1][LABEL_NAME]
        outputDescription = "Table - {}:".format(tableName)
        outputMessage = ""

        #Get ingredients infos
        for ingredientIndex in range(len(ingredients)):
            ingredientId = int(ingredients[ingredientIndex][INGREDIENT_NAME])
            ingredientQuantity = ingredients[ingredientIndex][INGREDIENT_QUANTITY]
            outputMessage += ingredientQuantity + " " + itemList[ingredientId-1][LABEL_NAME] + "\n"

        embedInsertField(embedPage, outputMessage, outputDescription, inline=False)

    #Send Message
    await ctx.send(file=embedImage, embed=embedPage)

# Shows set information
@bot.command()
async def set(ctx, *args):

    arg = " ".join(args)
    if ctx.author == bot.user or not arg:
        return
    print("User {} has requested set information about {}.".format(str(ctx.author), arg))

    #Find input in hash table
    setID = setHash.search(arg, LABEL_ID)
    if setID == -1:
        await ctx.send("Can't find set '{}' in data base.".format(arg))
        return SET_NOT_FOUND

    setDict = setList[int(setID)-1]
    setName = setDict[LABEL_SET_NAME]
    setPieces = setDict[LABEL_SET_PIECES]
    #imageFileName = setName.replace(" ", "_").lower() + STATIC_IMAGE_EXT
    #dominantImageColor = pickDominantColor(imageFileName)
    setTitle = "General Information about '{}' set:".format(setName)

    #embedImage = discord.File(GLOBAL_IMAGE_PATH + imageFileName, filename="image.png")
    embedPage = discord.Embed(color=0x0a850e, title=setTitle) #will be updated with dominantImageColor
    embedPage.set_thumbnail(url="attachment://image.png")
    
    for setCategory in setDict.keys():
        if setCategory == LABEL_RARITY:
            embedInsertRarityField(embedPage, setDict[setCategory], rarityList, inline=False)
        elif setCategory == LABEL_SET_PIECES:
            setPiecesLabel = "Set pieces from '{}':".format(setName)
            setPiecesValue = ""
            for setPieceIndex in range(len(setPieces)):
                setPiecesValue += setDict[setCategory][setPieceIndex] + ","
            embedInsertField(embedPage, setPiecesValue[:-1].replace(",", "\n"), setPiecesLabel)
        elif setCategory == LABEL_ID or setCategory == LABEL_SET_NAME:
            continue
        else:
            embedInsertField(embedPage, setDict[setCategory].replace(" / ", "\n"), setCategory, inline=False)
    #Send Message
    #await ctx.send(file=embedImage, embed=embedPage)
    await ctx.send(embed=embedPage)

bot.run(BotToken)