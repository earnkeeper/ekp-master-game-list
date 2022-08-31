from db.price_repo import PriceRepo

from shared.get_midnight_utc import get_midnight_utc


class TokenPriceInfoService:
    def __init__(
            self,
            price_repo: PriceRepo,
    ):
        self.price_repo = price_repo

    def get_price_records(self, game):
        records = self.price_repo.find_by_game_id(game["id"])
        return records

    async def get_all_games_price(self):
        records = self.price_repo.get_prices_of_all_games_by_timestamp()
        return records

    async def get_price_document(self, price_records, game, rate):

        ago_7d = get_midnight_utc().timestamp() - 7 * 86400

        price_records = list(filter(
            lambda x: x['timestamp'] >= ago_7d,
            price_records
        ))

        if not len(price_records):
            return None

        price_records.sort(key=lambda record: record['timestamp'])

        current_price = price_records[-1]["price_usd"] * rate
        current_price = float("%.3g" % current_price)
        price_delta = None
        price_delta_pc = None
        price_color = "normal"

        if len(price_records) > 1:
            yesterday_price = price_records[-2]["price_usd"] * rate
            yesterday_price = float("%.3g" % yesterday_price)
            price_delta = current_price - yesterday_price
            price_delta_pc = price_delta * 100 / yesterday_price
            price_delta_pc = round(price_delta_pc, 2)

            if price_delta_pc > 0:
                price_color = "success"
            if price_delta_pc < 0:
                price_color = "danger"

        chart = list(
            map(
                lambda record: {
                    "timestamp_ms": record["timestamp"] * 1000,
                    "price": float("%.3g" % (record["price_usd"] * rate))
                },
                price_records
            )
        )

        return {
            "current_price": current_price,
            "price_delta": price_delta,
            "price_delta_pc": price_delta_pc,
            "price_color": price_color,
            "chart": chart,
        }

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
