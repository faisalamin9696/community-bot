import json

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
            if len(props) >= 2:
                username = str(props[1]).lower().replace('@', '')
                await message.channel.typing()
                try:
                    account_data = await  steemfun.get_account_ext(username)
                    embed = await steemfun.generate_info_embed(account_data)
                    await message.reply(embed=embed)

                except Exception as e:
                    await message.channel.send("Error: " + str(e))

        # !report command
        if command == utils.commands[1]:
            if len(props) >= 2:
                community = str(props[1]).lower().replace('@', '')
                community_report = await steemfun.get_community_report(community)
                print(community_report)


client.run(utils.bot_token)
