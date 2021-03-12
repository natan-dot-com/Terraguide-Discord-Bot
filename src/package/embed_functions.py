import discord
from discord.ext import commands
# Functions which are going to build the embed layout relative to the labels

def embedInsertField(embedPage, dictValue, dictLabel):
    embedPage.add_field(name=dictLabel, value=dictValue)
