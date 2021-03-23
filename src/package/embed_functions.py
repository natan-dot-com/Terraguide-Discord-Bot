# Functions which are going to build the embed layout relative to the labels

import discord
from discord.ext import commands
from .json_labels import *
from .bot_config import *

# Not used because of discord UI emoji issues
# Get emoji message format from emoji json
def getRarityEmoji(rarityTier):
    emojiFilePath = EMOJI_DIR + EMOJI_NAME_FILE + JSON_EXT
    emojiList = LoadJSONFile(emojiFilePath)
    emojiName = emojiPrefix + rarityTier.replace(" ", "_").lower()
    if emojiName in emojiList.keys():
        return "<:" + emojiName + ":" + str(emojiList[emojiName]) + ">"
    else:
        return rarityTier

def embedInsertField(embedPage, dictValue, dictLabel, inline=False):
    embedPage.add_field(name=dictLabel, value=dictValue, inline=inline)

def embedInsertRarityField(embedPage, rarityID, rarityList, inline=True):
    for rarityInstance in rarityList:
        if rarityInstance[LABEL_RARITY_ID] == rarityID:
            embedInsertField(embedPage, rarityInstance[LABEL_RARITY_TIER], LABEL_RARITY_TIER, inline=inline)
            return

# Builds the recipe's panel UI inside a discord embed class
def createRecipesPanel(itemList, tableList, recipesList, recipeDict, recipeEmbed):
    for recipeInstance in recipeDict:
        recipeInstance = int(recipeInstance)
        recipeInfo = recipesList[recipeInstance-1]
        fieldName = "Made in " + tableList[int(recipeInfo[RECIPE_TABLE])-1][LABEL_NAME] + " using:"
        fieldMessage = ""
        for ingredientInstance in recipeInfo[RECIPE_IDENTITY]:
            fieldMessage += itemList[int(ingredientInstance[INGREDIENT_NAME])-1][LABEL_NAME] + " (" +\
            ingredientInstance[INGREDIENT_QUANTITY] + ")\n"
        fieldMessage += "Producing " + recipeInfo[RECIPE_RESULT_QUANTITY] + " unit(s)."
        embedInsertField(recipeEmbed, fieldMessage, fieldName, inline=False)


def createSellingPanel(npcList, sellingList, npcDict, newEmbed, itemName):
    for sellingInstance in npcDict:
        sellingInstance = int(sellingInstance)
        sellingInfo = sellingList[sellingInstance-1]
        fieldName = "Item '" + itemName + "' can be bought from:"
        fieldMessage = npcList[int(sellingInfo[NPC_ID])-1][LABEL_NAME] + ", for " + sellingInfo[NPC_ITEM_COST] +\
            " under the condition: " + sellingInfo[NPC_SELL_CONDITION].strip() + "."
        embedInsertField(newEmbed, fieldMessage, fieldName, inline=False)

def createBagDropPanel(npcList, bagList, bagDropList, bagDropDict, newEmbed, itemName):
    for bagDropInstance in bagDropDict:
        bagDropInstance = int(bagDropInstance)
        bagDropInfo = bagDropList[bagDropInstance-1]
        fieldName = "Item '" + itemName + "' can be dropped from:"
        fieldMessage = bagList[int(bagDropInfo[BAG_ID])-1][LABEL_NAME] + ", with probability of " + bagDropInfo[BAG_DROP_PROBABILITY] +\
            ".\n It commonly drops " + bagDropInfo[BAG_DROP_QUANTITY] + " instance(s)."
        embedInsertField(newEmbed, fieldMessage, fieldName, inline=False)

def embedSetFooter(embedPage, embedText):
    embedPage.set_footer(text=embedText)

async def embedSetReactions(bot, botMessage, pageList):
    await botMessage.add_reaction('◀')
    await botMessage.add_reaction('▶')

    def check(reaction, user):
        return user != botMessage.author and reaction.message.id == botMessage.id

    pageNumber = 0
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
            reaction, user = await bot.wait_for('reaction_add', timeout=reactionTimeOut, check=check)
            await botMessage.remove_reaction(reaction, user)
        except:
            break

    await botMessage.clear_reactions()

def checkImageFile(embedImage):
    if embedImage:
        if embedImage.fp.closed:
            embedImage = discord.File(embedImage.fp.raw.name , filename=embedImage.filename)
    return embedImage

# Function to send message acording to parameters
# If a list of embed is passed, it will add reactions to navigate between pages
# If command arguments are passed, it will treat the message acording to the arguments
async def sendMessage(ctx, bot, embed, commandArgumentList=[], embedImage=None):

    # Message will be sent as private
    if sendDM in commandArgumentList:
        if type(embed) is list:
            for embedInstance in embed:
                embedImage = checkImageFile(embedImage)
                embedInstance.set_footer()
                await ctx.author.send(file=embedImage, embed=embedInstance)        
        else:
            await ctx.author.send(file=embedImage, embed=embed)
        await ctx.message.add_reaction(whiteCheckMark)

    # Message will be sent without pages on the server
    elif sendLinear in commandArgumentList:
        if type(embed) is list:
            for embedInstance in embed:
                embedImage = checkImageFile(embedImage)
                embedInstance.set_footer()
                await ctx.send(file=embedImage, embed=embedInstance)
        else:
            await ctx.send(file=embedImage, embed=embed)

    # Message will be sent normaly on server
    else:
        if type(embed) is list:
            botMessage = await ctx.send(file=embedImage, embed=embed[0])

            # Reactions to switch between pages
            await embedSetReactions(bot, botMessage, embed)
        else:
            await ctx.send(file=embedImage, embed=embed)
    
