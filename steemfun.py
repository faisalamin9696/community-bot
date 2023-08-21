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
