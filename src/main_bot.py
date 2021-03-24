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
from package.permissions import *
from package.string_similarity import *

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

@bot.command()
async def help(ctx, *args):

    commandArgumentList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user:
        return
    if commandArgumentList == ERROR_INVALID_FLAG:
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

    await sendMessage(ctx, bot, embedList, commandArgumentList=commandArgumentList)

@bot.command()
async def item(ctx, *args):

    commandArgumentList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user or not commandStringInput:
        return ERROR_ARG_NOT_FOUND
    if commandArgumentList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG

    # Hash search the current item
    print("User {} has requested a craft recipe for {}.".format(str(ctx.author), commandStringInput))
    itemID = itemHash.search(commandStringInput, LABEL_ID)
    if itemID == NOT_FOUND:
        titleMessage = "Couldn't find item '" + commandStringInput + "' in the data base."
        errorEmbed = discord.Embed(title=titleMessage, color=0xFFFFFF)

        notFoundTitle =  "Didn't you mean...?"
        notFoundMessage = ""
        similarStrings = getSimilarStrings(commandStringInput, itemList)
        if similarStrings:
            for string in similarStrings:
                notFoundMessage += string + "\n"
        else:
            notFoundMessage = "Couldn't retrieve any suggestions from data base."
        errorEmbed.add_field(name=notFoundTitle, value=notFoundMessage)
        await sendMessage(ctx, bot, errorEmbed, commandArgumentList=commandArgumentList)

        return ERROR_ITEM_NOT_FOUND

    # Gets respective item info dictionary
    itemType = itemList[int(itemID)-1][LABEL_TYPE]
    itemFilePath = GLOBAL_JSON_PATH + DIR_ITEMS_DATA + itemFileManager[itemType] + JSON_EXT
    itemDict = binarySearch(LoadJSONFile(itemFilePath), itemID)
    if itemDict == NOT_FOUND:
        return ERROR_ITEM_NOT_FOUND

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

    exceptionLabels = [LABEL_ITEM_ID]
    for itemCategory in itemDict.keys():
        if itemCategory in exceptionLabels:
            continue
        if itemCategory == LABEL_SOURCE:
            hasSource = True
            break
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
                newEmbed.set_thumbnail(url="attachment://image.png")
                newEmbed.set_footer(text=PAGE_ALERT_MESSAGE.format(str(2+nonEmptyLists.index(existentCategory)),str(1+len(nonEmptyLists))))
                embedList.append(newEmbed)

    if len(embedList) > 1:
        mainPage.set_footer(text=PAGE_ALERT_MESSAGE.format('1', str(1+len(nonEmptyLists))))
    await sendMessage(ctx, bot, embedList, embedImage=mainImage, commandArgumentList=commandArgumentList)

# Shows a list of  every item which starts with 'arg'
@bot.command()
async def list(ctx, *args):

    commandArgumentList, commandStringInput = getCommandArguments(args)
    #arg = " ".join(args)
    if ctx.author == bot.user or not commandStringInput:
        return
    if commandArgumentList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG

    print("User {} has requested a craft recipe for {}.".format(str(ctx.author), commandStringInput))
    matchCounter = 0
    matchList = [[]]

    #Regex usage to find every match of the input
    for itemInstance in itemList:
        if re.search("^" + commandStringInput + "+", itemInstance[LABEL_NAME], re.IGNORECASE):
            if len(matchList[len(matchList)-1]) >= PAGE_DEFAULT_SIZE:
                matchList.append([])
            matchList[len(matchList)-1].append(itemInstance[LABEL_NAME])

    for matchInstance in matchList:
        matchCounter += len(matchInstance)
    if matchCounter == 0:
        await ctx.send("No items were found containing " + commandStringInput)
        return NOT_FOUND

    listDescription = str(matchCounter) + " occurrencies found:\n"
    # Pages creation with 12 lines each
    pageList = []
    for matchInstance in matchList:
        listMessage = ""
        for subInstance in matchInstance:
            listMessage += subInstance + "\n"

        newPage = discord.Embed(title ="Search Info about " + commandStringInput, colour=discord.Colour.green())
        embedInsertField(newPage, listMessage, listDescription, inline=False)
        embedSetFooter(newPage, "Page " + str(matchList.index(matchInstance) + 1) + "/" + str(len(matchList)))
        pageList.append(newPage)

    await sendMessage(ctx, bot, pageList, commandArgumentList=commandArgumentList)

# Shows crafting information
@bot.command()
async def craft(ctx, *args):

    commandArgumentList, commandStringInput = getCommandArguments(args)
    #arg = " ".join(args)
    if ctx.author == bot.user or not commandStringInput:
        return
    if commandArgumentList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG

    print("User {} has requested a craft recipe for {}.".format(str(ctx.author), commandStringInput))

    #Find input in hash table
    itemID = itemHash.search(commandStringInput, LABEL_ID)
    if itemID == -1:
        craftTitle = "Can't find item '{}' in data base.".format(commandStringInput)
        embedMessage = getSimilarStringEmbed(craftTitle, commandStringInput.lower(), itemList, label=LABEL_NAME)
        await ctx.send(embed=embedMessage)
        return ERROR_ITEM_NOT_FOUND

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
        resultQuantity = recipesList[int(itemRecipes[craftingRecipeIndex])-1][RECIPE_RESULT_QUANTITY]
        tableId = int(recipesList[int(itemRecipes[craftingRecipeIndex])-1][RECIPE_TABLE])
        tableName = tablesList[tableId-1][LABEL_NAME]
        outputDescription = "Made in {} using:".format(tableName)
        outputMessage = ""

        #Get ingredients infos
        for ingredientIndex in range(len(ingredients)):
            ingredientId = int(ingredients[ingredientIndex][INGREDIENT_NAME])
            ingredientQuantity = ingredients[ingredientIndex][INGREDIENT_QUANTITY]
            outputMessage += "{} ({})\n".format(itemList[ingredientId-1][LABEL_NAME], ingredientQuantity)
        outputMessage += "Producing {} units.".format(resultQuantity)
        embedInsertField(embedPage, outputMessage, outputDescription, inline=False)

    #Send Message
    await sendMessage(ctx, bot, embedPage, embedImage=embedImage, commandArgumentList=commandArgumentList)

# Shows set information
@bot.command()
async def set(ctx, *args):

    commandArgumentList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user or not commandStringInput:
        return
    if commandArgumentList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG

    print("User {} has requested set information about {}.".format(str(ctx.author), commandStringInput))

    #Find input in hash table
    setID = setHash.search(commandStringInput, LABEL_ID)
    if setID == -1:
        setTitle = "Can't find set '{}' in data base.".format(commandStringInput)
        embedMessage = getSimilarStringEmbed(setTitle, commandStringInput.lower(), setList, label=LABEL_SET_NAME)
        await ctx.send(embed=embedMessage)
        return ERROR_SET_NOT_FOUND

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
    await sendMessage(ctx, bot, embedPage, commandArgumentList=commandArgumentList)

@bot.command()
async def rarity(ctx, *args):

    commandArgumentList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user:
        return
    if commandArgumentList == ERROR_INVALID_FLAG:
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
        await sendMessage(ctx, bot, embedPageList, commandArgumentList=commandArgumentList)
    else:
        print("User '{}' has requested rarity information about '{}'.".format(str(ctx.author), commandStringInput))

        rarityDict = linearSearch(rarityList, LABEL_RARITY_TIER, commandStringInput.lower())
        if rarityDict == NOT_FOUND:
            rarityTitle = "Rarity Tier '{}' was not found in database.".format(commandStringInput)
            print(rarityTitle)
            embedMessage = getSimilarStringEmbed(rarityTitle, commandStringInput.lower(), rarityList, label=LABEL_RARITY_TIER)
            await ctx.send(embed=embedMessage)
            return

        rarityTitle = "Information about '{}' Rarity:".format(commandStringInput)
        rarityImagePath = GLOBAL_JSON_PATH + DIR_ID_REFERENCES + IMAGE_DIR_RARITY
        imageFileName = rarityDict[LABEL_RARITY_TIER].replace(" ", "_").lower() + STATIC_IMAGE_EXT
        embedImage = discord.File(rarityImagePath + imageFileName, filename="image.png")
        dominantImageColor = pickDominantColor(imageFileName, imagePath=rarityImagePath)
        embedPage = discord.Embed(color=dominantImageColor, title=rarityTitle)
        embedPage.set_thumbnail(url="attachment://image.png")

        rarityLabel = rarityDict[LABEL_RARITY_TIER]
        rarityValue = rarityDict[LABEL_RARITY_DESC]
        embedInsertField(embedPage, rarityValue, rarityLabel, inline=False)

        #Send Message
        await sendMessage(ctx, bot, embedPage, commandArgumentList=commandArgumentList, embedImage=embedImage)

@bot.command()
async def npc(ctx, *args):

    commandArgumentList, commandStringInput = getCommandArguments(args)
    if ctx.author == bot.user:
        return
    if not commandStringInput:
        await ctx.send("{} you must type the name of npc you want to find information about.".format(ctx.author))
    if commandArgumentList == ERROR_INVALID_FLAG:
        await ctx.send(FLAG_ERROR_MESSAGE)
        return ERROR_INVALID_FLAG
        
    print("User {} has requested npc information about {}.".format(str(ctx.author), commandStringInput))

    #Find input in hash table
    npcID = npcHash.search(commandStringInput, NPC_ID)
    if npcID == -1:
        npcTitle = "Can't find npc '{}' in data base.".format(commandStringInput)
        embedMessage = getSimilarStringEmbed(npcTitle, commandStringInput.lower(), npcList, label=LABEL_NAME)
        await ctx.send(embed=embedMessage)
        return ERROR_SET_NOT_FOUND
    #Will be supported after enemy npcs drops update on dataset
    elif npcList[int(npcID)-1][LABEL_TYPE] != "Town NPC":
        await ctx.send("Npc type not supported yet.")
        return

    npcPageList = []
    npcDict = npcList[int(npcID)-1]
    npcName = npcDict[LABEL_NAME]

    # Temporary linear search until we improve our npc database
    npcTownDict = linearSearch(npcTownList, NPC_ID, str(npcID))
    if npcTownDict == NOT_FOUND:
        print("NPC Town not found")
        return NOT_FOUND
    if str(npcTownDict[NPC_ID]) != str(npcDict[NPC_ID]):
        print("Inconsistence on NPC id from {}".format(npcDict[LABEL_NAME]))
        return ERROR_DATASET_INCONSISTENCE

    imageFilePath = GLOBAL_JSON_PATH + DIR_NPC_DATA + DIR_NPC_SPRITES
    imageFileName = npcName.replace(" ", "_").lower() + STATIC_IMAGE_EXT
    dominantImageColor = pickDominantColor(imageFileName, imagePath=imageFilePath)
    npcTitle = "General Information about '{}' NPC:".format(npcName)
    sellingListTitle = "Items sold by {}:".format(npcName)

    embedImage = discord.File(imageFilePath + imageFileName, filename="image.png")

    # First Page with general info about the NPC
    embedGeneralInfoPage = discord.Embed(color=dominantImageColor, title=npcTitle)
    embedGeneralInfoPage.set_thumbnail(url="attachment://image.png")

    for npcCategory in npcTownDict.keys():
        if npcCategory == NPC_SELLING_LIST:
            break
        elif npcCategory == NPC_ID:
            continue
        else:
            embedInsertField(embedGeneralInfoPage, npcTownDict[npcCategory], npcCategory, inline=False)

    # If has selling list then get infos
    if npcTownDict[NPC_SELLING_LIST]:

        # Put footer because there will be more than 1 page
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
                embedSelligListPage.set_thumbnail(url="attachment://image.png")
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
        await sendMessage(ctx, bot, npcPageList, embedImage=embedImage, commandArgumentList=commandArgumentList)

    # If we don't have any sell items then just send general info
    else:
        await sendMessage(ctx, bot, embedGeneralInfoPage, embedImage=embedImage, commandArgumentList=commandArgumentList)

# This functions works when it wants.
# Useless now but i will maintain it for future code reference
# Add emojis to bot server
@bot.command()
async def add_emojis(ctx, *args):

    if ctx.author == bot.user or not str(ctx.author.id) in ADMIN_LIST:
        await ctx.send("Permission Denied.")
        return

    await ctx.send("Starting adding emojis. This may take a few moments...")
    emojiFilePath = EMOJI_DIR + EMOJI_NAME_FILE + JSON_EXT
    emojiList = {}
    emojiCount = 0
    rarityFilePath = GLOBAL_JSON_PATH + DIR_ID_REFERENCES + IMAGE_DIR_RARITY
    for filename in os.listdir(rarityFilePath):
        with open(rarityFilePath + filename, "rb") as image:
            emojiFileName, emojiFileFormat = os.path.splitext(filename)
            emojiName = BOT_CONFIG_EMOJI_PREFIX + emojiFileName.lower()
            if emojiFileFormat != DYNAMIC_IMAGE_EXT:
                f = image.read()
                b = bytearray(f)
                guildEmoji = getGuildEmojiByName(emojiName, ctx.guild.emojis)
                if guildEmoji == ERROR_EMOJI_NOT_FOUND:
                    print("Emoji {} is NOT!!!! on server {}".format(emojiName, ctx.guild))
                    emoji = await ctx.guild.create_custom_emoji(image=b, name=emojiName)
                    emojiList[emojiName] = emoji.id
                    emojiCount += 1
                else:
                    print("Emoji {} is already on server {}".format(emojiName, ctx.guild))
                    emojiList[emojiName] = emoji.id


    SaveJSONFile(emojiFilePath, emojiList)
    await ctx.send("Done adding emojis. A total of {} emojis were added.".format(emojiCount))

# Delete emojis from bot server
@bot.command()
async def remove_emojis(ctx, *args):

    if ctx.author == bot.user or not str(ctx.author.id) in ADMIN_LIST:
        await ctx.send("Permission Denied.")
        return

    await ctx.send("Starting removing server emojis. This may take a few moments...")
    emojiFilePath = EMOJI_DIR + EMOJI_NAME_FILE + JSON_EXT
    emojiList = LoadJSONFile(emojiFilePath)
    emojiCount = 0
    rarityFilePath = GLOBAL_JSON_PATH + DIR_ID_REFERENCES + IMAGE_DIR_RARITY
    for filename in os.listdir(rarityFilePath):
        with open(rarityFilePath + filename, "rb") as image:
            emojiFileName, emojiFileFormat = os.path.splitext(filename)
            emojiName = BOT_CONFIG_EMOJI_PREFIX + emojiFileName.lower()
            if emojiFileFormat != DYNAMIC_IMAGE_EXT:
                f = image.read()
                b = bytearray(f)
                guildEmoji = getGuildEmojiByName(emojiName, ctx.guild.emojis)
                if guildEmoji == ERROR_EMOJI_NOT_FOUND:
                    print("Emoji {} not found on server {}".format(emojiName, ctx.guild))
                else:
                    print("Emoji {} found on server {}".format(emojiName, ctx.guild))
                    await guildEmoji.delete()
                    if emojiName in emojiList.keys():
                        emojiList.pop(emojiName)
                    emojiCount += 1

    SaveJSONFile(emojiFilePath, emojiList)
    await ctx.send("Done removing emojis. A total of {} emojis were removed.".format(emojiCount))

bot.run(BOT_TOKEN)
