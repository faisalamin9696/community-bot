from beem import Steem


class Utils:
    def __init__(self):
        # discord bot token
        self.bot_token = 'BOT_TOKEN_HERE'

        # bot commands
        self.commands = ['!info', '!report', '!vote']

        # steemit base url
        self.steemit_base = 'https://steemit.com'

        # sds base url
        self.sds_base = 'https://sds0.steemworld.org'

        self.folder_path = 'community-bot/files/'

        # private posting key of voter account
        self.voter_username = 'faisalamin'

        # private posting key of voter account
        self.voter_private_posting_key = ''

        # Nodes for the steem instance
        self.steem_nodes = "https://api.steemit.com"

        # steem vote instances
        self.steem_vote_instance = Steem(node=self.steem_nodes, keys=self.voter_private_posting_key)
