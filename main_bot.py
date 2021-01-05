import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message():
    if message.author == client.user:
        return

    if message.content.startwith('$hello'):
        await message.channel.send('Hello!')

client.run('Nzk2MDYzMTE0NDk1NTI0OTI1.X_SdjA.dZnQYOHJJqmjxoNeIp2lCnXQID8')
