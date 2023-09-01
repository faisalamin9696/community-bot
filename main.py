import json
import os

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


def create_directory(path):
    # Check whether the specified path exists or not
    is_exist = os.path.exists(path)

    if not is_exist:
        # Create a new directory because it does not exist
        os.makedirs(path)


# Commit
create_directory(utils.folder_path)


def create_file(file_name, content):
    f = open(utils.folder_path + file_name, "w")
    f.write(content)
    f.close()


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
                await message.channel.typing()
                community = str(props[1]).lower().replace('@', '')
                community_report = await steemfun.get_community_report(community)
                create_file(f"{community}-report.txt", community_report)
                await message.reply(f'**{community} Report (7-Days):**',
                                file=discord.File(utils.folder_path + f"{community}-report.txt"))



client.run(utils.bot_token)
