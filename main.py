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
                    print(1122, account_data['name'])
                    if account_data is not None:
                        await message.reply(f'username: {account_data.get("name")}\n'
                                            f'Steem: {account_data.get("balance_steem")}\n'
                                            f'SBD: {account_data.get("balance_sbd")}\n'
                                            f'VP: {account_data.get("upvote_mana_percent")}\n'
                                            f'RC: {account_data.get("rc_mana_percent")}\n')
                except Exception as e:
                    await message.channel.send("Error " + str(e))


client.run(utils.bot_token)
