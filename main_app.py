import logging
from decouple import AutoConfig
from ekp_sdk import BaseContainer
from ekp_sdk.db import MgClient
from app.features.info.activity_info_service import ActivityInfoService
from app.features.info.game_alert_service import GameAlertService
from app.features.info.info_controller import InfoController
from app.features.info.info_service import InfoService
from app.features.info.media_info_service import MediaInfoService
from app.features.info.price_analytics_service import PriceAnalyticsService
from app.features.info.resources_info_service import ResourcesInfoService
from app.features.info.social_followers_info_service import SocialFollowersInfoService
from app.features.info.token_price_info_service import TokenPriceInfoService
from app.features.info.token_volume_info_service import TokenVolumeInfoService
from app.features.info.user_analytics_service import UserAnalyticsService
from app.features.info.volume_analytics_service import VolumeAnalyticsService
from app.features.shared_games.shared_games_controller import SharedGamesController
from app.features.shared_games.shared_games_service import SharedGamesService
from app.features.stats.activity_stats_service import ActivityStatsService
from app.features.stats.social_stats_service import SocialStatsService
from app.features.stats.stats_controller import StatsController
from app.features.stats.token_price_stats_service import TokenPriceStatsService
from app.features.stats.volume_stats_service import VolumeStatsService
from db.activity_repo import ActivityRepo
from db.alert_config_repo import AlertConfigRepo
from db.contract_aggregate_repo import ContractAggregateRepo
from db.price_repo import PriceRepo
from db.resources_repo import ResourcesRepo
from db.social_repo import SocialRepo
from db.transaction_repo import TransactionRepo
from db.volume_repo import VolumeRepo
from ekp_sdk.services.web3_service import Web3
from db.game_repo import GameRepo
from db.youtube_repo import YoutubeRepo

from aiohttp import ClientSession, web


async def image_handler(req: web.Request):
    url = req.query.get("url", None)

    if not url:
        return web.HTTPNotFound()

    async with ClientSession() as session:
        async with await session.get(url) as res:
            if res.status != 200:
                return web.HTTPNotFound()

            img_raw = await res.read()

    return web.Response(body=img_raw, content_type='image/jpeg')


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")

        super().__init__(config)

        MONGO_URI_ETH = config("MONGO_URI_ETH")
        MONGO_URI_BSC = config("MONGO_URI_BSC")
        MONGO_DB_NAME = config('MONGO_DB_NAME')

        # Image Proxy

        self.client_service.app.add_routes([
            web.get('/image', image_handler)
        ])

        # DB

        self.mg_client_eth = MgClient(
            uri=MONGO_URI_ETH,
            db_name=MONGO_DB_NAME
        )

        self.mg_client_bsc = MgClient(
            uri=MONGO_URI_BSC,
            db_name=MONGO_DB_NAME
        )

        self.activity_repo = ActivityRepo(
            mg_client=self.mg_client
        )

        self.volume_repo = VolumeRepo(
            mg_client=self.mg_client
        )

        self.price_repo = PriceRepo(
            mg_client=self.mg_client
        )

        self.game_repo = GameRepo(
            mg_client=self.mg_client
        )

        self.game_repo_bsc = GameRepo(
            mg_client=self.mg_client_bsc
        )

        self.youtube_repo = YoutubeRepo(
            mg_client=self.mg_client
        )

        self.social_repo = SocialRepo(
            mg_client=self.mg_client
        )

        self.resources_repo = ResourcesRepo(
            mg_client=self.mg_client
        )

        self.contract_aggregate_repo_eth = ContractAggregateRepo(
            mg_client=self.mg_client_eth
        )
        
        self.contract_aggregate_repo_bsc = ContractAggregateRepo(
            mg_client=self.mg_client_bsc
        )

        self.transaction_repo_eth = TransactionRepo(
            mg_client=self.mg_client_eth
        )

        self.transaction_repo_bsc = TransactionRepo(
            mg_client=self.mg_client_bsc
        )

        # FEATURES - INFO

        self.activity_info_service = ActivityInfoService(
            activity_repo=self.activity_repo,
        )

        self.social_followers_info_service = SocialFollowersInfoService(
            game_repo=self.game_repo,
            social_repo=self.social_repo
        )

        self.token_volume_info_service = TokenVolumeInfoService(
            volume_repo=self.volume_repo,
        )

        self.token_price_info_service = TokenPriceInfoService(
            price_repo=self.price_repo,
        )

        self.media_info_service = MediaInfoService(
            youtube_repo=self.youtube_repo
        )

        self.resources_info_service = ResourcesInfoService(
            resources_repo=self.resources_repo
        )

        self.user_aggregate_service = UserAnalyticsService(
            contract_aggregate_repo_eth=self.contract_aggregate_repo_eth,
            contract_aggregate_repo_bsc=self.contract_aggregate_repo_bsc,
            transaction_repo_eth=self.transaction_repo_eth,
            game_repo=self.game_repo
        )

        self.shared_games_service = SharedGamesService(
            transaction_repo=self.transaction_repo_bsc,
            game_repo=self.game_repo_bsc,
        )

        self.alert_config_repo = AlertConfigRepo(
            mg_client=self.mg_client
        )

        self.volume_analytics_service = VolumeAnalyticsService()
        self.price_analytics_service = PriceAnalyticsService()
        
        self.info_service = InfoService(
            activity_info_service=self.activity_info_service,
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            game_repo=self.game_repo,
            social_repo=self.social_repo,
            token_volume_info_service=self.token_volume_info_service,
            price_repo=self.price_repo,
            token_price_info_service=self.token_price_info_service,
            social_followers_info_service=self.social_followers_info_service,
            media_info_service=self.media_info_service,
            resources_info_service=self.resources_info_service,
            contract_aggregate_repo=self.contract_aggregate_repo_eth,
            user_analytics_service=self.user_aggregate_service,
            volume_analytics_service=self.volume_analytics_service,
            price_analytics_service=self.price_analytics_service,
        )

        self.info_controller = InfoController(
            client_service=self.client_service,
            info_service=self.info_service
        )

        # FEATURES - STATS

        self.social_stats_service = SocialStatsService(
            social_repo=self.social_repo,
            game_repo=self.game_repo,
        )

        self.activity_stats_service = ActivityStatsService(
            activity_repo=self.activity_repo,
            game_repo=self.game_repo,
        )

        self.volume_stats_service = VolumeStatsService(
            volume_repo=self.volume_repo,
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            game_repo=self.game_repo,
        )

        self.token_price_stats_service = TokenPriceStatsService(
            price_repo=self.price_repo,
        )

        self.game_alert_service = GameAlertService(
            alert_config_repo=self.alert_config_repo
        )

        self.stats_controller = StatsController(
            client_service=self.client_service,
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            activity_stats_service=self.activity_stats_service,
            social_stats_service=self.social_stats_service,
            volume_stats_service=self.volume_stats_service,
            token_price_stats_service=self.token_price_stats_service,
            game_alert_service=self.game_alert_service
        )

        self.shared_games_controller = SharedGamesController(
            client_service=self.client_service,
            shared_games_service=self.shared_games_service
        )


if __name__ == '__main__':
    container = AppContainer()

    logging.basicConfig()

    logging.getLogger().setLevel(logging.INFO)

    container.client_service.add_controller(container.info_controller)
    container.client_service.add_controller(container.stats_controller)

    container.client_service.add_controller(container.shared_games_controller)

    logging.info("🚀 App started")

    container.client_service.listen()
