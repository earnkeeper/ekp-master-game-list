from ekp_sdk.services import CoingeckoService

from db.price_repo import PriceRepo
from datetime import datetime


class TokenPriceInfoService:
    def __init__(
            self,
            price_repo: PriceRepo,
    ):
        self.price_repo = price_repo

    async def get_price_document(self, game, rate):

        records = self.price_repo.find_by_game_id(game["id"])

        now = datetime.now().timestamp()

        if not len(records):
            return None

        latest_date_timestamp = records[len(records) - 1]["timestamp"]

        document = self.__create_record(game, now, latest_date_timestamp)

        for record in records:
            date_timestamp = record["timestamp"]
            ago = latest_date_timestamp - date_timestamp
            price = record["price_usd"]

            if price is None:
                price = 0

            if ago < 86400:
                document["price24h"] = (document["price24h"] + price) * rate
            elif ago < (2 * 86400):
                document["price48h"] = (document["price48h"] + price) * rate

            if ago < (86400 * 7):
                document["price7d"] = (document["price7d"] + price) * rate
                document["price7dcount"] = document["price7dcount"] + 1

            if document["price48h"] > 0:
                document["priceDelta"] = (document["price24h"] - document["price48h"]) * 100 / document["price48h"]

            if date_timestamp in document["chart7d"]:
                document["chart7d"][date_timestamp]["price"] = float("%.3g" % price) * rate

        document["price24h"] = float("%.3g" % document["price24h"]) * rate
        document["deltaColor"] = "normal"

        if document["priceDelta"] < 0:
            document["deltaColor"] = "danger"
        if document["priceDelta"] > 0:
            document["deltaColor"] = "success"

        return document

    def __create_record(self, game, now, latest_date_timestamp):

        chart7d_template = {}

        for i in range(7):
            chart_timestamp = latest_date_timestamp - 86400 * (6 - i)
            chart7d_template[chart_timestamp] = {
                "timestamp": chart_timestamp,
                "timestamp_ms": chart_timestamp * 1000,
                "price": 0
            }

        return {
            "gameId": game["id"],
            "gameName": game["name"],
            "price24h": 0,
            "price48h": 0,
            "priceDelta": 0,
            "price7d": 0,
            "price7dcount": 0,
            "updated": now,
            "chart7d": chart7d_template,
        }        
