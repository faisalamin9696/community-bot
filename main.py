import discord

# configure discord intents
intents = discord.Intents.default()
intents.message_content = True

# creating client instance
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} is online')


@client.event
async def on_message(message):
    print(message)


client.run('MTEzODM0OTM0Njg1Nzk0NzE2Nw.Ghpzv2.Z8Y1L18GjZuEgVIDK9q_cylQq2s57Ky3nE82-4')
