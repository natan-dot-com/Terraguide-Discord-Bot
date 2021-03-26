# Functions which are going to build the embed layout relative to the labels

import sys
import discord
from discord.ext import commands
from .json_labels import *
from .bot_config import *

# Constant values for colors related to UI output commands
EMBED_CRAFTING_COLOR = 0x0a850e
EMBED_LIST_COLOR = 0xe40101
EMBED_HELP_COLOR = 0x000000

task = None

# Not used because of discord UI emoji issues
# Get emoji message format from emoji json
def getRarityEmoji(rarityTier):
    emojiFilePath = EMOJI_DIR + EMOJI_NAME_FILE + JSON_EXT
    emojiList = LoadJSONFile(emojiFilePath)
    emojiName = BOT_CONFIG_EMOJI_PREFIX + rarityTier.replace(" ", "_").lower()
    if emojiName in emojiList.keys():
        return "<:" + emojiName + ":" + str(emojiList[emojiName]) + ">"
    else:
        return rarityTier

def embedInsertField(embedPage: discord.Embed, dictValue: str, dictLabel: str, inline=False):
    embedPage.add_field(name=dictLabel, value=dictValue, inline=inline)

def embedInsertRarityField(embedPage: discord.Embed, rarityID: int, rarityList: list, inline=True):
    for rarityInstance in rarityList:
        if rarityInstance[LABEL_RARITY_ID] == rarityID:
            embedInsertField(embedPage, rarityInstance[LABEL_RARITY_TIER], LABEL_RARITY_TIER, inline=inline)
            return

# Builds the recipe's panel UI inside a discord embed class
def createRecipesPanel(itemList: list, tableList: list, recipesList: list, recipeDict, recipeEmbed: discord.Embed):
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


def createSellingPanel(npcList: list, sellingList: list, npcDict, newEmbed: discord.Embed, itemName: str):
    for sellingInstance in npcDict:
        sellingInstance = int(sellingInstance)
        sellingInfo = sellingList[sellingInstance-1]
        fieldName = "Item '" + itemName + "' can be bought from:"
        fieldMessage = npcList[int(sellingInfo[NPC_ID])-1][LABEL_NAME] + ", for " + sellingInfo[NPC_ITEM_COST] +\
            " under the condition: " + sellingInfo[NPC_SELL_CONDITION].strip() + "."
        embedInsertField(newEmbed, fieldMessage, fieldName, inline=False)

def createBagDropPanel(npcList: list, bagList: list, bagDropList: list, bagDropDict, newEmbed: discord.Embed, itemName: str):
    for bagDropInstance in bagDropDict:
        bagDropInstance = int(bagDropInstance)
        bagDropInfo = bagDropList[bagDropInstance-1]
        fieldName = "Item '" + itemName + "' can be dropped from:"
        fieldMessage = bagList[int(bagDropInfo[BAG_ID])-1][LABEL_NAME] + ", with probability of " + bagDropInfo[BAG_DROP_PROBABILITY] +\
            ".\n It commonly drops " + bagDropInfo[BAG_DROP_QUANTITY] + " instance(s)."
        embedInsertField(newEmbed, fieldMessage, fieldName, inline=False)

def embedSetFooter(embedPage: discord.Embed, embedText: str):
    embedPage.set_footer(text=embedText)

async def embedSetReactions(bot: commands.Bot, botMessage, pageList: list):
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
            reaction, user = await bot.wait_for('reaction_add', timeout=PAGE_REACTION_TIMEOUT, check=check)
            await botMessage.remove_reaction(reaction, user)
        except:
            break

    await botMessage.clear_reactions()

def checkImageFile(embedImage: discord.File):
    if embedImage:
        if embedImage.fp.closed:
            embedImage = discord.File(embedImage.fp.raw.name , filename=embedImage.filename)
    return embedImage

# Function to send message acording to parameters
# If a list of embed is passed, it will add reactions to navigate between pages
# If command arguments are passed, it will treat the message acording to the arguments
async def sendMessage(ctx, bot: commands.Bot, embed: discord.Embed, commandArgumentList=[], embedImage=None):

    # Message will be sent as private
    if FLAG_PRIVATE in commandArgumentList:
        if type(embed) is list:
            for embedInstance in embed:
                embedImage = checkImageFile(embedImage)
                embedInstance.set_footer()
                await ctx.author.send(file=embedImage, embed=embedInstance)        
        else:
            await ctx.author.send(file=embedImage, embed=embed)
        await ctx.message.add_reaction(EMOJI_WHITE_CHECK_MARK)

    # Message will be sent without pages on the server
    elif FLAG_LINEAR in commandArgumentList:
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

            def messageCheck(author):
                def innerCheck(message):
                    return author == message.author
                return 

            def RepresentsInt(s):
                try: 
                    int(s)
                    return True
                except ValueError:
                    return False

            # Reactions to switch between pages
            if len(embed) > 1:
                global task
                authorMessage = None
                task = bot.loop.create_task(embedSetReactions(bot, botMessage, embed))

                if sys._getframe().f_back.f_code.co_name == "list":
                    embedSize = int(embed[0].fields[0].name.split(" ")[0])
                    while True:
                        authorMessage = await bot.wait_for('message', check=messageCheck(ctx.author), timeout=PAGE_REACTION_TIMEOUT)
                        if RepresentsInt(authorMessage.content):
                            if int(authorMessage.content) >= 0 and int(authorMessage.content) <= embedSize:
                                task.cancel()
                                task = None
                                break
                    return botMessage, authorMessage
                else:
                    await embedSetReactions(bot, botMessage, embed)
        else:
            await ctx.send(file=embedImage, embed=embed)
