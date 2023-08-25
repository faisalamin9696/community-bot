import json

import discord
import requests

from utils import Utils


def map_sds_response(response):
    """ Returns the mapped rows and columns of given SDS response

                            :param response: SDS response
                            :type response: json, dict
                        """
    result = response.get('result')
    if not result:
        result = response

    cols = result.get('cols')
    rows = result.get('rows')
    if not cols:
        if not rows:
            return result
        else:
            return rows

    keys = list(cols.keys())
    redefined_data = []
    for row in rows:
        mapped_obj = {}
        loop = 0
        for value in row:
            mapped_obj[keys[loop]] = value
            loop += 1
        # noinspection PyBroadException
        try:
            if mapped_obj.get('author_reputation'):
                mapped_obj['author_reputation'] = round(mapped_obj['author_reputation'], 2)

            if mapped_obj.get('observer_reputation'):
                mapped_obj['observer_reputation'] = round(mapped_obj['observer_reputation'], 2)

            if mapped_obj.get('reputation'):
                mapped_obj['reputation'] = round(mapped_obj['reputation'], 2)
        except Exception:
            pass

        redefined_data.append(mapped_obj)
    return redefined_data


class SteemFun:
    utils = Utils()

    async def get_account_ext(self, username):
        if username is None:
            return
        else:
            api = self.utils.sds_base + f"/accounts_api/getAccountExt/{username}"
            response = requests.get(api).json()
            return map_sds_response(response)

    async def get_steem_props(self):
        api = self.utils.sds_base + "/steem_requests_api/getSteemProps"
        response = requests.get(api).json()
        return map_sds_response(response)

    async def vest_to_steem(self, vests):
        steem_props = await self.get_steem_props()
        # noinspection PyTypeChecker
        return vests * steem_props['steem_per_share']


    # noinspection PyMethodMayBeStatic
    async def generate_info_embed(self, account_data):
        embed = discord.Embed()
        name = account_data['name']
        if account_data['posting_json_metadata']:
            posting_json = json.loads(account_data['posting_json_metadata'])
            if posting_json['profile']:
                try:
                    user_cover = posting_json['profile']['cover_image']
                    user_name = posting_json['profile']['name']
                    if user_cover is not None:
                        embed.set_image(url=user_cover)
                    if user_name is not None:
                        embed.add_field(name='Name', value=user_name)
                except Exception:
                    pass

        user_avatar = 'https://steemitimages.com/u/' + name + '/avatar/small'

        profile_url = self.utils.steemit_base + '/@' + name
        steem_power = await self.vest_to_steem(account_data['vests_own'])
        embed.set_author(name=name, url=profile_url, icon_url=user_avatar)

        embed.add_field(name='Upvote Power', value=account_data['upvote_mana_percent'])
        embed.add_field(name='Downvote Power', value=account_data['downvote_mana_percent'])
        embed.add_field(name='Resource Credits', value=account_data['rc_mana_percent'])
        embed.add_field(name='Resource Credits', value=account_data['rc_mana_percent'])
        embed.add_field(name='Creator', value=account_data['creator'])
        embed.add_field(name='Recovery Account', value=account_data['recovery_account'])
        embed.add_field(name='Steem Balance', value=account_data['balance_steem'])
        embed.add_field(name='SBD Balance', value=account_data['balance_sbd'])
        # fixing 3 decimal points of Steem Power
        embed.add_field(name='Steem Power', value=f"{steem_power:.3f}")

        return embed
