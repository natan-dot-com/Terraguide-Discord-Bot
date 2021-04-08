from logging import ERROR
from os import chdir
import os
from platform import system
if system() == "Linux":
    chdir("../")

import math
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
from package.string_similarity import *

# Main bot token import (if you're hosting in your own machine, just skip it)
try:
    from package.bot_token import BOT_TOKEN
except ModuleNotFoundError:
    pass

bot = commands.Bot(command_prefix=BOT_CONFIG_PREFIX, description=BOT_CONFIG_DESCRIPTION, help_command=None)
itemList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + MAIN_NAME_FILE + JSON_EXT)
tableList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + TABLE_NAME_FILE + JSON_EXT)
rarityList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + RARITY_NAME_FILE + JSON_EXT)
recipesList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + RECIPE_NAME_FILE + JSON_EXT)
tablesList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + TABLE_NAME_FILE + JSON_EXT)
setList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + SET_NAME_FILE + JSON_EXT)
npcTownList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_NPC_DATA + NPC_TOWN_NAME_FILE + JSON_EXT)
npcList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + NPC_NAME_FILE + JSON_EXT)
sellingList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + SELLING_LIST_NAME_FILE + JSON_EXT)
grabBagList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + BAGS_NAME_FILE + JSON_EXT)
grabBagDropList = LoadJSONFile(GLOBAL_JSON_PATH + DIR_ID_REFERENCES + BAGS_DROP_NAME_FILE + JSON_EXT)

itemHash = loadDependencies(itemList)
setHash = loadDependencies(setList, SET_HASH_SIZE, LABEL_SET_NAME)
npcHash = loadDependencies(npcList, NPC_HASH_SIZE, LABEL_NAME)

@bot.event
async def on_ready():

    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name=BOT_CONFIG_PREFIX + "help"))

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):
        await ctx.send(COMMAND_NOT_FOUND_MESSAGE.format(ctx.message.content))
    else:
        raise error

@bot.command()
async def quest(ctx, *args):

    commandFlagList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user:
        return
    if commandFlagList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG
    pass

@bot.command()
async def help(ctx, *args):

    commandFlagList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user:
        return
    if commandFlagList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG
        
    embedList = []

    # Main panel construction
    mainPanel = discord.Embed(color=EMBED_HELP_COLOR, title=HELP_EMBED_TITLE)
    embedInsertField(mainPanel, HELP_INTRODUCTION_DESC, HELP_INTRODUCTION_TITLE, inline=False)
    for command, commandDescription in zip(commandDict.keys(), commandDict.values()):
        embedInsertField(mainPanel, commandDescription, command, inline=False)
    mainPanel.set_footer(text=PAGE_ALERT_MESSAGE.format('1','2'))
    embedList.append(mainPanel)

    # Flags panel construction
    flagsPanel = discord.Embed(color=EMBED_HELP_COLOR, title=HELP_EMBED_TITLE)
    flagsDisplay = ""
    for argumentsDescription in flagDescriptionList:
        flagsDisplay += argumentsDescription + "\n"
    embedInsertField(flagsPanel, flagsDisplay, FLAG_TITLE_LABEL, inline=False)
    flagsPanel.set_footer(text=PAGE_ALERT_MESSAGE.format('2','2'))
    embedList.append(flagsPanel)

    await sendMessage(ctx, bot, embedList, commandFlagList=commandFlagList)

@bot.command()
async def item(ctx, *args):

    commandFlagList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user or not commandStringInput:
        await ctx.send(COMMAND_EMPTY_ERROR_MESSAGE.format(ctx.message.content, ctx.author.mention))
        return ERROR_ARG_NOT_FOUND
    if commandFlagList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG

    # Hash search the current item
    print("User {} has requested a craft recipe for {}.".format(str(ctx.author), commandStringInput))
    itemID = itemHash.search(commandStringInput, LABEL_ID)
    if itemID == NOT_FOUND:
        titleMessage = "Couldn't find item '" + commandStringInput + "' in the data base."
        errorEmbed, similarStrings = getSimilarStringEmbed(titleMessage, commandStringInput, itemList)
        await sendMessage(ctx, bot, errorEmbed)
        await getUserResponse(ctx, bot, similarStrings, ITEM_FUNCTION, commandFlagList=commandFlagList)
        return

    # Gets respective item info dictionary
    itemType = itemList[int(itemID)-1][LABEL_TYPE]
    itemFilePath = GLOBAL_JSON_PATH + DIR_ITEMS_DATA + itemFileManager[itemType] + JSON_EXT
    itemDict = binarySearch(LoadJSONFile(itemFilePath), itemID)
    if itemDict == NOT_FOUND:
        return ERROR_ITEM_NOT_FOUND

    # Starts building each embed panel
    embedList = []

    itemName = itemList[int(itemID)-1][LABEL_NAME]
    imageExt = getImageExt(GLOBAL_IMAGE_PATH, itemName.replace(" ", "_"))
    imageFileName = itemName.replace(" ", "_") + imageExt
    dominantImageColor = pickDominantColor(imageFileName)
    hasSource = False

    # Main info embed panel construction
    mainPage = discord.Embed(color=dominantImageColor, title="General informations about '" + itemName + "':")
    mainImage = discord.File(GLOBAL_IMAGE_PATH + imageFileName, filename="image." + imageExt)
    mainPage.set_thumbnail(url="attachment://image." + imageExt)

    exceptionLabels = [LABEL_ITEM_ID]
    for itemCategory in itemDict.keys():
        if itemCategory in exceptionLabels:
            continue

        if itemCategory == LABEL_SOURCE:
            hasSource = True
            break
        elif type(itemDict[itemCategory]) is list:
            for itemSubcategory in itemDict[itemCategory]:
                embedInsertField(mainPage, itemSubcategory, itemCategory, inline=True)
        elif itemCategory == LABEL_SET_ID:
            embedInsertField(mainPage, setList[int(itemDict[itemCategory])-1][LABEL_SET_NAME], LABEL_SET_NAME, inline=True)
        elif itemCategory == LABEL_RARITY:
            embedInsertRarityField(mainPage, itemDict[itemCategory], rarityList)
        else:
            embedInsertField(mainPage, itemDict[itemCategory], itemCategory, inline=True)
    embedList.append(mainPage)

    # If item has source dict (i.e. if embed will have more than one page)
    nonEmptyLists = []
    if hasSource:

        # LABEL_SOURCE dict analysis
        for sourceCategory in itemDict[LABEL_SOURCE]:
            if itemDict[LABEL_SOURCE][sourceCategory]:
                nonEmptyLists.append(sourceCategory)

        # Source embed panels creation
        for existentCategory in nonEmptyLists:
            newEmbed = None

            # Recipes embed panel cration
            if existentCategory == SOURCE_RECIPES:
                titleMessage = "Showing craft recipes for '" + itemName + "':"
                newEmbed = discord.Embed(title=titleMessage, color=dominantImageColor)
                createRecipesPanel(itemList, tableList, recipesList, itemDict[LABEL_SOURCE][SOURCE_RECIPES], newEmbed)

            # NPC's selling offers embed panel creation
            elif existentCategory == SOURCE_NPC:
                titleMessage = "Showing selling offers for '" + itemName + "':"
                newEmbed = discord.Embed(title=titleMessage, color=dominantImageColor)
                createSellingPanel(npcList, sellingList, itemDict[LABEL_SOURCE][SOURCE_NPC], newEmbed, itemName)

            elif existentCategory == SOURCE_DROP:
                continue

            # Grab bags' drops embed panel creation
            elif existentCategory == SOURCE_GRAB_BAG:
                titleMessage = "Showing bag drops from '" + itemName + "':"
                newEmbed = discord.Embed(title=titleMessage, color=dominantImageColor)
                createBagDropPanel(npcList, grabBagList, grabBagDropList, itemDict[LABEL_SOURCE][SOURCE_GRAB_BAG], newEmbed, itemName)

            elif existentCategory == SOURCE_OTHER:
                fieldTitle = "General availability"
                embedInsertField(mainPage, itemDict[LABEL_SOURCE][SOURCE_OTHER], fieldTitle, inline=False)

            if newEmbed:
                newEmbed.set_thumbnail(url="attachment://image." + imageExt)
                newEmbed.set_footer(text=PAGE_ALERT_MESSAGE.format(str(2+nonEmptyLists.index(existentCategory)),str(1+len(nonEmptyLists))))
                embedList.append(newEmbed)

    if len(embedList) > 1:
        mainPage.set_footer(text=PAGE_ALERT_MESSAGE.format('1', str(1+len(nonEmptyLists))))
    await sendMessage(ctx, bot, embedList, embedImage=mainImage, commandFlagList=commandFlagList)

# Shows a list of  every item which starts with user input argument
@bot.command()
async def list(ctx, *args):

    # Get arguments and flags
    commandFlagList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user or not commandStringInput:
        await ctx.send(COMMAND_EMPTY_ERROR_MESSAGE.format(ctx.message.content, ctx.author.mention))
        return ERROR_ARG_NOT_FOUND
    if commandFlagList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG

    print("User {} has requested a list of items starting with '{}'.".format(str(ctx.author), commandStringInput))
    matchCounter = 0
    matchList = [[]]

    # Regex usage to find every match of the input
    for itemInstance in itemList:
        if re.search("^" + commandStringInput + "+", itemInstance[LABEL_NAME], re.IGNORECASE):
            if len(matchList[len(matchList)-1]) >= PAGE_DEFAULT_SIZE:
                matchList.append([])
            matchCounter += 1

            # matchTuple = (<Identifier>, <Item Name>)
            matchTuple = (str(matchCounter), itemInstance[LABEL_NAME])
            matchList[len(matchList)-1].append(matchTuple)

    if matchCounter == 0:
        await ctx.send("No items containing " + commandStringInput + " were found.")
        return NOT_FOUND

    listDescription = str(matchCounter) + " occurrencies found:\n"

    # Tuple constants
    ITEM_IDENTIFIER = 0
    ITEM_NAME = 1

    # Pages creation within 12 lines each
    pageList = []
    for matchInstance in matchList:
        listMessage = ""
        for subInstance in matchInstance:
            listMessage += "**" + subInstance[ITEM_IDENTIFIER] + ".** " + subInstance[ITEM_NAME] + "\n"

        newPage = discord.Embed(title ="Search Info about '" + commandStringInput + "'", colour=discord.Colour.green())
        infoMessage = "Type the current match number to show all the information about it, guiding yourself by\
 the number shown at left of each item's name. If none, type '0'.\n\n"
        embedInsertField(newPage, infoMessage + listMessage, listDescription, inline=False)
        embedSetFooter(newPage, "Page " + str(matchList.index(matchInstance) + 1) + "/" + str(len(matchList)))
        pageList.append(newPage)

    # Wait until user's response
    botMessage, authorMessage = await sendMessage(ctx, bot, pageList, commandFlagList=commandFlagList)
    if authorMessage.content == "0":
        await authorMessage.add_reaction(EMOJI_WHITE_CHECK_MARK)
        return

    # Invoke t.item based on the user's response
    itemPage = int(int(authorMessage.content)/PAGE_DEFAULT_SIZE)
    chosenItemName = matchList[itemPage][int(authorMessage.content)-itemPage*PAGE_DEFAULT_SIZE-1][ITEM_NAME]
    await ctx.invoke(bot.get_command('item'), chosenItemName)

# Shows crafting information
@bot.command()
async def craft(ctx, *args):

    # Get arguments and flags
    commandFlagList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user or not commandStringInput:
        await ctx.send(COMMAND_EMPTY_ERROR_MESSAGE.format(ctx.message.content, ctx.author.mention))
        return ERROR_ARG_NOT_FOUND
    if commandFlagList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG

    print("User {} has requested a craft recipe for '{}'.".format(str(ctx.author), commandStringInput))

    # Finds input in hash table
    itemID = itemHash.search(commandStringInput, LABEL_ID)
    if itemID == NOT_FOUND:
        # If not found, get similar item names
        titleMessage = "Couldn't find item '" + commandStringInput + "' in the data base."
        errorEmbed, similarStrings = getSimilarStringEmbed(titleMessage, commandStringInput, itemList)
        await sendMessage(ctx, bot, errorEmbed)
        await getUserResponse(ctx, bot, similarStrings, CRAFT_FUNCTION, commandFlagList=commandFlagList)
        return

    itemType = itemList[int(itemID)-1][LABEL_TYPE]
    itemFilePath = GLOBAL_JSON_PATH + DIR_ITEMS_DATA + itemFileManager[itemType] + JSON_EXT
    itemName = itemList[int(itemID)-1][LABEL_NAME]
    itemDict = binarySearch(LoadJSONFile(itemFilePath), itemID)

    imageExt = getImageExt(GLOBAL_IMAGE_PATH, itemName.replace(" ", "_"))
    imageFileName = itemName.replace(" ", "_") + imageExt
    dominantImageColor = pickDominantColor(imageFileName)
    craftTitle = "Craft information about '{}':".format(itemName)

    embedImage = discord.File(GLOBAL_IMAGE_PATH + imageFileName, filename="image." + imageExt)
    embedPage = discord.Embed(color=dominantImageColor, title=craftTitle)
    embedPage.set_thumbnail(url="attachment://image." + imageExt)

    itemRecipes = itemDict[LABEL_SOURCE][SOURCE_RECIPES]
    # Get crafting recipes
    for craftingRecipeIndex in range(len(itemRecipes)):
        ingredients = recipesList[int(itemRecipes[craftingRecipeIndex])-1][RECIPE_IDENTITY]
        resultQuantity = recipesList[int(itemRecipes[craftingRecipeIndex])-1][RECIPE_RESULT_QUANTITY]
        tableId = int(recipesList[int(itemRecipes[craftingRecipeIndex])-1][RECIPE_TABLE])
        tableName = tablesList[tableId-1][LABEL_NAME]
        outputDescription = "Made in {} using:".format(tableName)
        outputMessage = ""

        # Get ingredients' infos
        for ingredientIndex in range(len(ingredients)):
            ingredientId = int(ingredients[ingredientIndex][INGREDIENT_NAME])
            ingredientQuantity = ingredients[ingredientIndex][INGREDIENT_QUANTITY]
            outputMessage += "{} ({})\n".format(itemList[ingredientId-1][LABEL_NAME], ingredientQuantity)
        outputMessage += "Producing {} unit(s).".format(resultQuantity)
        embedInsertField(embedPage, outputMessage, outputDescription, inline=False)

    #Send Message
    await sendMessage(ctx, bot, embedPage, embedImage=embedImage, commandFlagList=commandFlagList)

@bot.command()
async def bagdrop(ctx, *args):

    # Get arguments and flags
    commandFlagList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user or not commandStringInput:
        await ctx.send(COMMAND_EMPTY_ERROR_MESSAGE.format(ctx.message.content, ctx.author.mention))
        return ERROR_ARG_NOT_FOUND
    if commandFlagList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG

    print("User {} has requested drop information about '{}'.".format(str(ctx.author), commandStringInput))

    itemID = itemHash.search(commandStringInput, LABEL_ID)
    if itemID == NOT_FOUND:
        titleMessage = "Couldn't find item '" + commandStringInput + "' in the data base."
        errorEmbed, similarStrings = getSimilarStringEmbed(titleMessage, commandStringInput, itemList)
        await sendMessage(ctx, bot, errorEmbed)
        await getUserResponse(ctx, bot, similarStrings, BAGDROP_FUNCTION, commandFlagList=commandFlagList)
        return

    # Gets respective item info dictionary
    itemType = itemList[int(itemID)-1][LABEL_TYPE]
    itemFilePath = GLOBAL_JSON_PATH + DIR_ITEMS_DATA + itemFileManager[itemType] + JSON_EXT
    itemDict = binarySearch(LoadJSONFile(itemFilePath), itemID)
    if itemDict == NOT_FOUND:
        return ERROR_ITEM_NOT_FOUND


    itemName = itemList[int(itemID)-1][LABEL_NAME]
    imageExt = getImageExt(GLOBAL_IMAGE_PATH, itemName.replace(" ", "_"))
    imageFileName = itemName.replace(" ", "_") + imageExt
    dominantImageColor = pickDominantColor(imageFileName)
    
    # Check if there are bag drops for this item
    hasBagDrop = True
    if LABEL_SOURCE in itemDict.keys():
        if SOURCE_GRAB_BAG in itemDict[LABEL_SOURCE].keys():
            if len(itemDict[LABEL_SOURCE][SOURCE_GRAB_BAG]) == 0:
                hasBagDrop = False
        else:
            hasBagDrop = False
    else:
        hasBagDrop = False

    # Information embed construction
    titleMessage = "Showing bag drops for '{}':".format(itemName)
    embedPage = discord.Embed(color=dominantImageColor, title=titleMessage)
    embedImage = discord.File(GLOBAL_IMAGE_PATH + imageFileName, filename="image." + imageExt)
    embedPage.set_thumbnail(url="attachment://image." + imageExt)

    if hasBagDrop:
        createBagDropPanel(npcList, grabBagList, grabBagDropList, itemDict[LABEL_SOURCE][SOURCE_GRAB_BAG], embedPage, itemName)
    else:
        titleMessage = "Item '{}' has no bag drops.".format(itemName)
        fieldMessage = "Couldn't retrieve any information from our database."
        embedInsertField(embedPage, fieldMessage, titleMessage, inline=False)
    
    #Send Message
    await sendMessage(ctx, bot, embedPage, embedImage=embedImage, commandFlagList=commandFlagList)

@bot.command()
async def sell(ctx, *args):

    # Get arguments and flags
    commandFlagList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user or not commandStringInput:
        await ctx.send(COMMAND_EMPTY_ERROR_MESSAGE.format(ctx.message.content, ctx.author.mention))
        return ERROR_ARG_NOT_FOUND
    if commandFlagList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG

    print("User {} has requested selling offers for '{}'.".format(str(ctx.author), commandStringInput))

    itemID = itemHash.search(commandStringInput, LABEL_ID)
    if itemID == NOT_FOUND:
        titleMessage = "Couldn't find item '" + commandStringInput + "' in the data base."
        errorEmbed, similarStrings = getSimilarStringEmbed(titleMessage, commandStringInput, itemList)
        await sendMessage(ctx, bot, errorEmbed)
        await getUserResponse(ctx, bot, similarStrings, SELL_FUNCTION, commandFlagList=commandFlagList)
        return

    # Gets respective item info dictionary
    itemType = itemList[int(itemID)-1][LABEL_TYPE]
    itemFilePath = GLOBAL_JSON_PATH + DIR_ITEMS_DATA + itemFileManager[itemType] + JSON_EXT
    itemDict = binarySearch(LoadJSONFile(itemFilePath), itemID)
    if itemDict == NOT_FOUND:
        return ERROR_ITEM_NOT_FOUND

    itemName = itemList[int(itemID)-1][LABEL_NAME]
    imageExt = getImageExt(GLOBAL_IMAGE_PATH, itemName.replace(" ", "_"))
    imageFileName = itemName.replace(" ", "_") + imageExt
    dominantImageColor = pickDominantColor(imageFileName)
    
    # Check if there are NPCs selling this item
    hasSellingOffers = True
    if LABEL_SOURCE in itemDict.keys():
        if SOURCE_NPC in itemDict[LABEL_SOURCE].keys():
            if len(itemDict[LABEL_SOURCE][SOURCE_NPC]) == 0:
                hasSellingOffers = False
        else:
            hasSellingOffers = False
    else:
        hasSellingOffers = False

    # Information embed construction
    titleMessage = "Showing selling offers for '{}':".format(itemName)
    embedPage = discord.Embed(color=dominantImageColor, title=titleMessage)
    embedImage = discord.File(GLOBAL_IMAGE_PATH + imageFileName, filename="image." + imageExt)
    embedPage.set_thumbnail(url="attachment://image." + imageExt)

    if hasSellingOffers:
        createSellingPanel(npcList, sellingList, itemDict[LABEL_SOURCE][SOURCE_NPC], embedPage, itemName)
    else:
        titleMessage = "Item '{}' has no selling offers.".format(itemName)
        fieldMessage = "Couldn't retrieve any information from our database."
        embedInsertField(embedPage, fieldMessage, titleMessage, inline=False)
    
    #Send Message
    await sendMessage(ctx, bot, embedPage, embedImage=embedImage, commandFlagList=commandFlagList)

# Shows set information
@bot.command()
async def set(ctx, *args):

    # Get arguments and flags
    commandFlagList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user or not commandStringInput:
        await ctx.send(COMMAND_EMPTY_ERROR_MESSAGE.format(ctx.message.content, ctx.author.mention))
        return ERROR_ARG_NOT_FOUND
    if commandFlagList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG

    print("User {} has requested set information about {}.".format(str(ctx.author), commandStringInput))

    #Find input in hash table
    setID = setHash.search(commandStringInput, LABEL_ID)
    if setID == NOT_FOUND:
        # If not found, get similar set names
        titleMessage = "Couldn't find item '" + commandStringInput + "' in the data base."
        errorEmbed, similarStrings = getSimilarStringEmbed(titleMessage, commandStringInput, setList, label=LABEL_SET_NAME)
        await sendMessage(ctx, bot, errorEmbed)
        await getUserResponse(ctx, bot, similarStrings, SET_FUNCTION, commandFlagList=commandFlagList)
        return

    setDict = setList[int(setID)-1]
    setName = setDict[LABEL_SET_NAME]
    setPieces = setDict[LABEL_SET_PIECES]

    #imageExt = getImageExt(GLOBAL_IMAGE_PATH, setName.replace(" ", "_"))
    #imageFileName = setName.replace(" ", "_") + imageExt
    #dominantImageColor = pickDominantColor(imageFileName)
    setTitle = "General Information about '{}' set:".format(setName)

    #embedImage = discord.File(GLOBAL_IMAGE_PATH + imageFileName, filename="image." + imageExt)
    embedPage = discord.Embed(color=0x0a850e, title=setTitle) #will be updated with dominantImageColor
    #embedPage.set_thumbnail(url="attachment://image." + imageExt)

    # Get fields containing informations about set
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
    await sendMessage(ctx, bot, embedPage, commandFlagList=commandFlagList)

@bot.command()
async def rarity(ctx, *args):

    # Get arguments and flags
    commandFlagList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user:
        return
    if commandFlagList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG

    # If the user didn't type the rarity then the command shows every rarity tier information
    if not commandStringInput:
        print("User {} has requested rarity information.".format(str(ctx.author)))

        rarityPage = 0
        rarityModuleCounter = 0
        rarityPageItemsCount = 4
        rarityTotalPages = math.ceil(len(rarityList) / rarityPageItemsCount)
        rarityTitle = "Information about all Terraria Rarity Tiers:"
        embedPageList = []
        for rarityInstance in rarityList:
            # Check Page counter variable
            if rarityModuleCounter == rarityPageItemsCount:
                rarityModuleCounter = 0
            if rarityModuleCounter == 0:
                rarityPage += 1
                embedPage = discord.Embed(color=0x0a850e, title=rarityTitle)
                rarityPagealert = PAGE_ALERT_MESSAGE.format(rarityPage, rarityTotalPages)
                embedPage.set_footer(text=rarityPagealert)
                embedPageList.append(embedPage)

            rarityModuleCounter += 1
            rarityLabel = rarityInstance[LABEL_RARITY_TIER]
            rarityValue = rarityInstance[LABEL_RARITY_DESC]
            embedInsertField(embedPageList[len(embedPageList)-1], rarityValue, rarityLabel, inline=False)

        # Send Message
        await sendMessage(ctx, bot, embedPageList, commandFlagList=commandFlagList)
    # Get a specific rarity tier
    else:
        print("User '{}' has requested rarity information about '{}'.".format(str(ctx.author), commandStringInput))

        # Search to find rarity tier
        rarityDict = linearSearch(rarityList, LABEL_RARITY_TIER, commandStringInput)
        if rarityDict == NOT_FOUND:
            # If not found, get similar rarity tier names
            titleMessage = "Couldn't find rarity tier '" + commandStringInput + "' in the data base."
            errorEmbed, similarStrings = getSimilarStringEmbed(titleMessage, commandStringInput, rarityList, label=LABEL_RARITY_TIER)
            await sendMessage(ctx, bot, errorEmbed)
            await getUserResponse(ctx, bot, similarStrings, RARITY_FUNCTION, commandFlagList=commandFlagList)
            return

        rarityTitle = "Information about '{}' Rarity:".format(commandStringInput)
        rarityName = rarityDict[LABEL_RARITY_TIER]
        rarityImagePath = GLOBAL_JSON_PATH + DIR_ID_REFERENCES + IMAGE_DIR_RARITY
        imageExt = getImageExt(rarityImagePath, rarityName.replace(" ", "_"))
        imageFileName = rarityName.replace(" ", "_") + imageExt

        # Embed variables
        embedImage = discord.File(rarityImagePath + imageFileName, filename="image" + imageExt)
        dominantImageColor = pickDominantColor(imageFileName, imagePath=rarityImagePath)
        embedPage = discord.Embed(color=dominantImageColor, title=rarityTitle)
        embedPage.set_thumbnail(url="attachment://image" + imageExt)
        rarityLabel = rarityDict[LABEL_RARITY_TIER]
        rarityValue = rarityDict[LABEL_RARITY_DESC]
        embedInsertField(embedPage, rarityValue, rarityLabel, inline=False)

        #Send Message
        await sendMessage(ctx, bot, embedPage, commandFlagList=commandFlagList, embedImage=embedImage)

@bot.command()
async def npc(ctx, *args):

    # Get arguments and flags
    commandFlagList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user:
        return
    if not commandStringInput:
        await ctx.send(COMMAND_EMPTY_ERROR_MESSAGE.format(ctx.message.content, ctx.author.mention))
        return ERROR_ARG_NOT_FOUND
    if commandFlagList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG
        
    print("User {} has requested npc information about {}.".format(str(ctx.author), commandStringInput))

    # Find input in hash table
    npcID = npcHash.search(commandStringInput, NPC_ID)
    if npcID == NOT_FOUND:
        # If not found, get similar NPC names
        titleMessage = "Couldn't find NPC '" + commandStringInput + "' in the data base."
        errorEmbed, similarStrings = getSimilarStringEmbed(titleMessage, commandStringInput, npcList, label=LABEL_NAME)
        await sendMessage(ctx, bot, errorEmbed)
        await getUserResponse(ctx, bot, similarStrings, NPC_FUNCTION, commandFlagList=commandFlagList)
        return

    # Will be supported after enemy npcs drops update on dataset
    elif npcList[int(npcID)-1][LABEL_TYPE] != "Town NPC":
        await ctx.send("NPC type not supported yet.")
        return

    npcPageList = []
    npcDict = npcList[int(npcID)-1]
    npcName = npcDict[LABEL_NAME]

    # Temporary linear search until we improve our npc database
    npcTownDict = linearSearch(npcTownList, NPC_ID, str(npcID))
    if npcTownDict == NOT_FOUND:
        print("Town NPC not found")
        return NOT_FOUND
    if str(npcTownDict[NPC_ID]) != str(npcDict[NPC_ID]):
        print("Inconsistence on NPC ID from {}".format(npcDict[LABEL_NAME]))
        return ERROR_DATASET_INCONSISTENCE

    imageFilePath = GLOBAL_JSON_PATH + DIR_NPC_DATA + DIR_NPC_SPRITES
    imageExt = getImageExt(imageFilePath, npcName.replace(" ", "_").lower())
    imageFileName = npcName.replace(" ", "_").lower() + imageExt

    dominantImageColor = pickDominantColor(imageFileName, imagePath=imageFilePath)
    npcTitle = "General Information about '{}' NPC:".format(npcName)
    sellingListTitle = "Items sold by {}:".format(npcName)


    # First Page with general info about the NPC
    embedImage = discord.File(imageFilePath + imageFileName, filename="image." + imageExt)
    embedGeneralInfoPage = discord.Embed(color=dominantImageColor, title=npcTitle)
    embedGeneralInfoPage.set_thumbnail(url="attachment://image." + imageExt)

    # Get fields containing informations about NPC
    for npcCategory in npcTownDict.keys():
        if npcCategory == NPC_SELLING_LIST:
            break
        elif npcCategory == NPC_ID:
            continue
        else:
            embedInsertField(embedGeneralInfoPage, npcTownDict[npcCategory], npcCategory, inline=False)

    # If has selling list then get infos
    if npcTownDict[NPC_SELLING_LIST]:

        # Put footer because there will be more than one page
        npcTotalPages = math.ceil(len(npcTownDict[NPC_SELLING_LIST]) / PAGE_NPC_ITEMS_COUNT) + 1
        embedSetFooter(embedGeneralInfoPage, PAGE_ALERT_MESSAGE.format(1, npcTotalPages))
        npcPageList.append(embedGeneralInfoPage)

        npcPage = 1
        npcModuleCounter = 0

        for sellingID in npcTownDict[NPC_SELLING_LIST]:
            # Check Page counter variable
            if npcModuleCounter == PAGE_NPC_ITEMS_COUNT:
                npcModuleCounter = 0
            if npcModuleCounter == 0:
                npcPage += 1
                # Second Page with selling info about the NPC
                embedSelligListPage = discord.Embed(color=dominantImageColor, title=sellingListTitle)
                embedSelligListPage.set_thumbnail(url="attachment://image." + imageExt)
                embedSetFooter(embedSelligListPage, PAGE_ALERT_MESSAGE.format(npcPage, npcTotalPages))
                npcPageList.append(embedSelligListPage)

            npcModuleCounter += 1
            sellingDict = sellingList[int(sellingID)-1]

            # Get Label
            itemID = sellingDict[NPC_SELLING_ITEM]
            sellingLabel = itemList[int(itemID)-1][LABEL_NAME]

            # Get Value
            itemCost = sellingDict[NPC_ITEM_COST]
            sellCondition = sellingDict[NPC_SELL_CONDITION]
            sellingValue = "**{}**: {}.\n**{}**: {}.".format(NPC_ITEM_COST, itemCost, NPC_SELL_CONDITION, sellCondition)

            embedInsertField(embedSelligListPage, sellingValue, sellingLabel, inline=False)

        # Send Message
        await sendMessage(ctx, bot, npcPageList, embedImage=embedImage, commandFlagList=commandFlagList)

    # If we don't have any sell items then just send general info
    else:
        await sendMessage(ctx, bot, embedGeneralInfoPage, embedImage=embedImage, commandFlagList=commandFlagList)

bot.run(BOT_TOKEN)
