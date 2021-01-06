import discord
from discord.ext import commands
import json_manager
import utility

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ping'):
        await message.channel.send('Pong!')

@client.command()
async def recp(ctx, item):
    if ctx.author == client.user or not item:
        return

    returnMessage = ""


client.run('Nzk2MDY1OTI0NzU1MDk1NTg0.X_SgKg.8UNAsVGPDnbS2nMc40LrpuoepTI')
