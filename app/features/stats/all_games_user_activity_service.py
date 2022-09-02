from pprint import pprint

from app.features.info.token_volume_info_service import TokenVolumeInfoService
from app.features.info.volume_analytics_service import VolumeAnalyticsService
from app.features.stats.all_users_analytics_service import AllUsersAnalyticsService

from db.game_repo import GameRepo


class AllGamesUserActivityService:
    def __init__(
            self,
            # token_volume_info_service: TokenVolumeInfoService,
            all_users_analytics_service: AllUsersAnalyticsService,
            game_repo: GameRepo
    ):
        # self.token_volume_info_service = token_volume_info_service
        self.all_users_analytics_service = all_users_analytics_service
        self.game_repo = game_repo

    async def get_documents(self, volume_days, is_subscribed):

        all_games_users_analytic_records = self.all_users_analytics_service.get_period_chart(volume_days)

        all_games_last_users_analytic_records = self.all_users_analytics_service.get_last_period_chart(volume_days)

        analytics_info = {}

        analytics_info["analytics_users"] = {
            "users_period_chart": all_games_users_analytic_records,
            "users_last_period_chart": all_games_last_users_analytic_records
        }

        if is_subscribed:
            analytics_info["analytics_users"]["is_subscribed"] = True

        return [analytics_info]


        # pprint()
        # volume_records = await self.token_volume_info_service.get_all_games_volume()
        #
        # volume_period_chart = self.volume_analytics_service.get_period_chart(
        #     volume_days, volume_records)
        # volume_last_period_chart = self.volume_analytics_service.get_last_period_chart(
        #     volume_days, volume_records)
        #
        # volume_info = {}
        #
        # volume_info["analytics_volume"] = {
        #     "volume_period_chart": volume_period_chart,
        #     "volume_last_period_chart": volume_last_period_chart,
        # }
        #
        # return [volume_info]
