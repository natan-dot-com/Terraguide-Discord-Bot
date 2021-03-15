# Functions which are going to build the embed layout relative to the labels
import discord
from discord.ext import commands
from .json_labels import *

def embedInsertField(embedPage, dictValue, dictLabel):
    embedPage.add_field(name=dictLabel, value=dictValue)

def embedInsertRarityField(embedPage, rarityID, rarityList):
    for rarityInstance in rarityList:
        if rarityInstance[LABEL_RARITY_ID] == rarityID:
            embedInsertField(embedPage, rarityInstance[LABEL_RARITY_TIER], LABEL_RARITY_TIER)
            return
