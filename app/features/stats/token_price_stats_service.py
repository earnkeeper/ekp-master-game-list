from pprint import pprint
from db.price_repo import PriceRepo

from shared.get_midnight_utc import get_midnight_utc


class TokenPriceStatsService:
    def __init__(
            self,
            price_repo: PriceRepo
    ):
        self.price_repo = price_repo

    async def get_documents(self, rate):
        current_prices = self.price_repo.find_latest_price_by_game_id()

        if not len(current_prices):
            return []

        start_of_day_prices = self.price_repo.find_latest_daily_price_by_game_id()

        start_of_day_prices_map = {}

        for record in start_of_day_prices:
            start_of_day_prices_map[record["_id"]] = record

        documents = []

        for record in current_prices:
            game_id = record["_id"]
            price = record["price"]

            if price is None:
                continue

            if game_id not in start_of_day_prices_map:
                continue

            start_of_day_record = start_of_day_prices_map[game_id]

            if "price" not in start_of_day_record or not start_of_day_record["price"]:
                continue

            delta_today = price - start_of_day_record["price"]
            delta_today_pc = delta_today * 100 / start_of_day_record["price"]
            delta_today_color = "normal"
            if delta_today > 0:
                delta_today_color = "success"
            if delta_today < 0:
                delta_today_color = "danger"

            price = float("%.2f" % (price*rate))

            document = {
                "id": game_id,
                "game_id": game_id,
                "price": price,
                "price_delta": delta_today,
                "price_delta_pc": delta_today_pc,
                "price_delta_color": delta_today_color
            }
            
            documents.append(document)

        return documents
