from pprint import pprint

from app.features.info.token_volume_info_service import TokenVolumeInfoService
from app.features.info.volume_analytics_service import VolumeAnalyticsService

from db.game_repo import GameRepo



class AllGamesVolumeService:
    def __init__(
            self,
            token_volume_info_service: TokenVolumeInfoService,
            volume_analytics_service: VolumeAnalyticsService,
            game_repo: GameRepo
    ):
        self.token_volume_info_service = token_volume_info_service
        self.volume_analytics_service = volume_analytics_service
        self.game_repo = game_repo


    async def get_documents(self, volume_days, rate):

        volume_records = await self.token_volume_info_service.get_all_games_volume()

        volume_period_chart = self.volume_analytics_service.get_period_chart(
            volume_days, volume_records, rate)
        volume_last_period_chart = self.volume_analytics_service.get_last_period_chart(
            volume_days, volume_records, rate)

        volume_info = {}

        volume_info["analytics_volume"] = {
            "volume_period_chart": volume_period_chart,
            "volume_last_period_chart": volume_last_period_chart,
        }

        return [volume_info]

