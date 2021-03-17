# Functions which are going to build the embed layout relative to the labels

import discord
from discord.ext import commands
from .json_labels import *

def embedInsertField(embedPage, dictValue, dictLabel, inline=False):
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
        embedInsertField(recipeEmbed, fieldMessage, fieldName)
