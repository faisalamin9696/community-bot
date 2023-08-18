import requests

from utils import Utils


class SteemFun:
    utils = Utils()

    async def get_account_ext(self, username):
        if username is None:
            return
        else:
            api = self.utils.sds_base+ f"/accounts_api/getAccountExt/{username}"
            response = requests.get(api).json()
            print(response)
