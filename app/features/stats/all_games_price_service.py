from pprint import pprint

from app.features.info.token_price_info_service import TokenPriceInfoService
from app.features.info.price_analytics_service import PriceAnalyticsService

from db.game_repo import GameRepo



class AllGamesPriceService:
    def __init__(
            self,
            token_price_info_service: TokenPriceInfoService,
            price_analytics_service: PriceAnalyticsService,
            game_repo: GameRepo
    ):
        self.token_price_info_service = token_price_info_service
        self.price_analytics_service = price_analytics_service
        self.game_repo = game_repo


    async def get_documents(self, price_days):

        price_records = await self.token_price_info_service.get_all_games_price()

        price_period_chart = self.price_analytics_service.get_period_chart(
            price_days, price_records)
        price_last_period_chart = self.price_analytics_service.get_last_period_chart(
            price_days, price_records)

        price_info = {}

        price_info["analytics_price"] = {
            "price_period_chart": price_period_chart,
            "price_last_period_chart": price_last_period_chart,
        }

        return [price_info]

