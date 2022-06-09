import logging
from decouple import AutoConfig
from ekp_sdk import BaseContainer
from app.features.info.activity_service import ActivityService
from app.features.info.info_controller import InfoController
from app.features.info.info_service import InfoService
from app.features.info.token_volume_service import TokenVolumeService
from app.features.stats.activity_stats_service import ActivityStatsService
from app.features.stats.stats_controller import StatsController
from db.activity_repo import ActivityRepo
from db.volume_repo import VolumeRepo


from db.game_repo import GameRepo


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")

        super().__init__(config)

        # DB

        self.activity_repo = ActivityRepo(
            mg_client=self.mg_client
        )

        self.volume_repo = VolumeRepo(
            mg_client=self.mg_client
        )

        self.game_repo = GameRepo(
            mg_client=self.mg_client
        )

        # FEATURES - ACTIVITY

        self.activity_service = ActivityService(
            activity_repo=self.activity_repo,
        )

        # FEATURES - TOKEN VOLUME

        self.token_volume_service = TokenVolumeService(
            volume_repo=self.volume_repo,
        )

        # FEATURES - INFO

        self.info_service = InfoService(
            activity_service=self.activity_service,
            token_volume_service=self.token_volume_service,
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            game_repo=self.game_repo
        )

        self.info_controller = InfoController(
            client_service=self.client_service,
            info_service=self.info_service
        )

        # FEATURES - STATS

        self.activity_stats_service = ActivityStatsService(
            activity_service=self.activity_service,
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            game_repo=self.game_repo,
        )

        self.stats_controller = StatsController(
            client_service=self.client_service,
            activity_stats_service=self.activity_stats_service
        )


if __name__ == '__main__':
    container = AppContainer()

    logging.basicConfig()

    logging.getLogger().setLevel(logging.INFO)

    container.client_service.add_controller(container.info_controller)
    container.client_service.add_controller(container.stats_controller)

    logging.info("🚀 App started")

    container.client_service.listen()
