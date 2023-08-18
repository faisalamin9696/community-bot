import discord

from steemfun import SteemFun
from utils import Utils

# creating utils and steemfun instance
utils = Utils()
steemfun = SteemFun()

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
    # message from the bot itself
    if message.author == client.user:
        return

    props = message.content.split(maxsplit=6)
    command = props[0]

    # command validation
    if command in utils.commands:

        # !info command
        if command == utils.commands[0]:
            await steemfun.get_account_ext('faisalamin')


client.run(utils.bot_token)
