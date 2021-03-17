# Functions which are going to build the embed layout relative to the labels

import discord
from discord.ext import commands
from .json_labels import *
from .bot_config import *

def embedInsertField(embedPage, dictValue, dictLabel, inline=True):
    embedPage.add_field(name=dictLabel, value=dictValue, inline=inline)

def embedInsertRarityField(embedPage, rarityID, rarityList):
    for rarityInstance in rarityList:
        if rarityInstance[LABEL_RARITY_ID] == rarityID:
            embedInsertField(embedPage, rarityInstance[LABEL_RARITY_TIER], LABEL_RARITY_TIER, inline=True)
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
        fieldMessage += "Producing " + recipeInfo[RECIPE_RESULT_QUANTITY] + " units."
        embedInsertField(recipeEmbed, fieldMessage, fieldName)


def createSellingPanel(itemList, npcList, sellingList, npcDict, newEmbed, itemName):
    for sellingInstance in npcDict:
        sellingInstance = int(sellingInstance)
        print(sellingInstance)
        sellingInfo = sellingList[sellingInstance-1]
        fieldName = "Item '" + itemName + "' can be bought from:"
        fieldMessage = npcList[int(sellingInfo[NPC_ID])-1][LABEL_NAME] + ", for " + sellingInfo[NPC_ITEM_COST] +\
            " under the condition: " + sellingInfo[NPC_SELL_CONDITION].strip() + "."
        embedInsertField(newEmbed, fieldMessage, fieldName)
        
