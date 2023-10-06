import json
import os

import discord
from beem.comment import Comment

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
            if len(props) == 2:
                await message.channel.typing()
                community = str(props[1]).lower().replace('@', '')
                community_report = await steemfun.get_community_report(community)
                create_file(f"{community}-report.txt", community_report)
                await message.reply(f'**{community} Report (7-Days):**',
                                    file=discord.File(utils.folder_path + f"{community}-report.txt"))
            if len(props) == 3:
                await message.channel.typing()
                username = str(props[1]).lower().replace('@', '')
                community = str(props[2]).lower().replace('@', '')
                author_report = await steemfun.get_author_report(username, community)
                embed = discord.Embed()
                profile_url = utils.steemit_base + '/@' + username
                user_avatar = 'https://steemitimages.com/u/' + username + '/avatar/small'
                embed.set_author(name=username, url=profile_url, icon_url=user_avatar)
                embed.add_field(name='Posts', value=author_report.get('total_post_count'))
                embed.add_field(name='Comments', value=author_report.get('total_comment_count'))
                embed.add_field(name='Unique Comments', value=author_report.get('unique_comment_count'))
                await message.reply(embed=embed)

        # !vote command
        if command == utils.commands[2]:
            if len(props) == 3:
                post_link = str(props[1]).split('/')
                post_link.reverse()
                perm_link = post_link[0]
                post_author = post_link[1]
                identifier = f'{post_author}/{perm_link}'
                weight = float(props[2])

                await message.channel.typing()
                try:
                    steem = utils.steem_vote_instance
                    response = steem.vote(weight=weight, identifier=identifier, account=utils.voter_username)
                    if response.get('trx_id'):
                        await message.reply(f'Voted at {weight}%')
                    else:
                        await message.reply(f'Failed')

                except Exception as e:
                    await message.channel.send("Error: " + str(e))

        # !send command
        if command == utils.commands[3]:
            if len(props) == 2:
                post_link = str(props[1]).split('/')
                post_link.reverse()
                perm_link = post_link[0]
                post_author = post_link[1]
                identifier = f'{post_author}/{perm_link}'
                body = 'Hello testing the steem community bot created by @faisalamin'
                await message.channel.typing()
                try:
                    steem = utils.steem_vote_instance
                    comment = Comment(authorperm=identifier, blockchain_instance=steem)
                    response = comment.reply(body=body, author=utils.voter_username)
                    if response.get('trx_id'):
                        await message.reply(f'Comment sent to www.steemit.com/@{identifier}')
                    else:
                        await message.reply(f'Failed')

                except Exception as e:
                    await message.channel.send("Error: " + str(e))


client.run(utils.bot_token)
