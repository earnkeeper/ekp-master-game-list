from pprint import pprint

from db.price_repo import PriceRepo
from shared.get_midnight_utc import get_midnight_utc
from app.utils.proxy_image import proxy_image
from db.game_repo import GameRepo
from ekp_sdk.services import CacheService, CoingeckoService
from datetime import datetime
import copy


class TokenPriceStatsService:
    def __init__(
            self,
            price_repo: PriceRepo,
            cache_service: CoingeckoService,
            coingecko_service: CoingeckoService,
            game_repo: GameRepo,
    ):
        self.price_repo = price_repo
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.game_repo = game_repo

    async def get_documents(self):
        games = self.game_repo.find_all()

        games_map = {}

        for game in games:
            games_map[game["id"]] = game

        # records = self.price_repo.find_all()
        #
        records = self.price_repo.find_all_and_group()
        #
        # metabomb_record = [record_gr for record_gr in records if record_gr['_id'] == 'axie-infinity']
        # pprint(metabomb_record)

        if not len(records):
            return []

        latest_date_timestamp = records[len(records) - 1]["timestamp"]

        today = get_midnight_utc(
            datetime.fromtimestamp(latest_date_timestamp)
        ).timestamp()

        # chart7d_template = {}

        # for i in range(7):
        #     chart_timestamp = latest_date_timestamp - 86400 * (6 - i)
        #     chart7d_template[chart_timestamp] = {
        #         "timestamp": chart_timestamp,
        #         "timestamp_ms": chart_timestamp * 1000,
        #         "volume": 0,
        #     }

        grouped_by_game_id = {}

        now = datetime.now()
        now_midnight = get_midnight_utc(now).timestamp()
        now = now.timestamp()
        now_seconds_into_day = now - now_midnight

        for record in records:
            if record['timestamp'] < 0:
                continue

            game_id = record["_id"]
            date_timestamp = record["timestamp"]

            if game_id not in grouped_by_game_id:
                grouped_by_game_id[game_id] = self.__create_record(
                    game_id,
                    record,
                    games_map,
                    now,
                )

            midnight = get_midnight_utc(
                datetime.fromtimestamp(date_timestamp)
            ).timestamp()

            ago = today - midnight

            price = record["price"]

            if price is None:
                price = 0
            # if record['_id'] == 'axie-infinity':
            #     print(f"Price now_1: {price}")
            # if midnight == now_midnight:
            #     price = int(price * 86400 / now_seconds_into_day)
            # if record['_id'] == 'axie-infinity':
            #     print(f"Price now_2: {price}")
            group = grouped_by_game_id[game_id]

            if ago == 0:
                group["price24h"] = group["price24h"] + price
            elif ago == 86400:
                group["price48h"] = group["price48h"] + price

            # if record['_id'] == 'axie-infinity':
            #     print(f"Group24h price now_1: {group['price24h']}")

            if ago < (86400 * 6):
                group["price7d"] += price
            elif ago < (86400 * 13):
                group["price14d"] += price

            if group["price14d"] > 0:
                group["price7dDelta"] = (
                                                group["price7d"] - group["price14d"]) * 100 / group["price14d"]

            if group["price48h"] > 0:
                group["priceDelta"] = (
                                              group["price24h"] - group["price48h"]) * 100 / group["price48h"]

            # if date_timestamp in group["chart7d_volume"]:
            #     group["chart7d_volume"][date_timestamp]["volume"] = volume

        documents = list(
            filter(lambda x: x["price7d"], grouped_by_game_id.values())
        )

        for document in documents:
            if document["priceDelta"]:
                if document["priceDelta"] < 0:
                    document["price_deltaColor"] = "danger"
                if document["priceDelta"] > 0:
                    document["price_deltaColor"] = "success"

            if document["price7dDelta"]:
                if document["price7dDelta"] < 0:
                    document["price_delta7dColor"] = "danger"
                if document["price7dDelta"] > 0:
                    document["price_delta7dColor"] = "success"

        return documents

    def __create_record(self, game_id, record, games_map, now):
        gameLink = f"https://www.coingecko.com/en/coins/{game_id}"

        website = None
        twitter = None
        discord = None
        telegram = None

        chains = []
        profile_image_url = None

        if game_id in games_map:
            game = games_map[game_id]
            website = game["website"]
            twitter = f'https://twitter.com/{game["twitter"]}'
            discord = game["discord"]
            telegram = game["telegram"]
            chains = self.__get_game_chains(game)
            profile_image_url = game.get('profile_image_url', None)

        return {
            "id": game_id,
            "gameId": game_id,
            # "game_name": record["game_name"],
            "profile_image_url": proxy_image(profile_image_url),
            "chains": chains,
            "gameLink": gameLink,
            "price24h": 0,
            "price48h": 0,
            "priceDelta": None,
            "price7dDelta": None,
            "price7d": 0,
            "price14d": 0,
            "updated": now,
            # "chart7d_volume": copy.deepcopy(chart7d_template),
            "website": website,
            "twitter": twitter,
            "discord": discord,
            "telegram": telegram,
        }

    def __get_game_chains(self, game):
        chains = []

        for chain in ['bsc', 'eth', 'polygon']:
            if len(game['tokens'][chain]):
                chains.append(chain)

        return chains
