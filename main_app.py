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
from app.features.info.shared_games_service import SharedGamesService
from app.features.stats.activity_stats_service import ActivityStatsService
from app.features.stats.all_games_price_service import AllGamesPriceService
from app.features.stats.all_games_user_activity_service import AllGamesUserActivityService
from app.features.stats.all_games_volume_service import AllGamesVolumeService
from app.features.stats.all_users_analytics_service import AllUsersAnalyticsService
from app.features.stats.social_stats_service import SocialStatsService
from app.features.stats.stats_controller import StatsController
from app.features.stats.token_price_stats_service import TokenPriceStatsService
from app.features.stats.volume_stats_service import VolumeStatsService
from db.activity_repo import ActivityRepo
from db.alert_config_repo import AlertConfigRepo
from db.contract_aggregate_repo import ContractAggregateRepo
from db.price_repo import PriceRepo
from db.resources_repo import ResourcesRepo
from db.shared_games_repo import SharedGamesRepo
from db.social_repo import SocialRepo
from db.transaction_repo import TransactionRepo
from db.volume_repo import VolumeRepo
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

        # Image Proxy

        self.client_service.app.add_routes([
            web.get('/image', image_handler)
        ])

        # DB

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

        self.youtube_repo = YoutubeRepo(
            mg_client=self.mg_client
        )

        self.social_repo = SocialRepo(
            mg_client=self.mg_client
        )

        self.resources_repo = ResourcesRepo(
            mg_client=self.mg_client
        )

        self.shared_games_repo = SharedGamesRepo(
            mg_client=self.mg_client
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
            game_repo=self.game_repo
        )

        self.shared_games_service = SharedGamesService(
            shared_games_repo=self.shared_games_repo
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
            user_analytics_service=self.user_aggregate_service,
            volume_analytics_service=self.volume_analytics_service,
            price_analytics_service=self.price_analytics_service,
            shared_games_service=self.shared_games_service
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

        self.all_games_volume_service = AllGamesVolumeService(
            token_volume_info_service=self.token_volume_info_service,
            volume_analytics_service=self.volume_analytics_service,
            game_repo=self.game_repo
        )

        self.all_games_price_service = AllGamesPriceService(
            token_price_info_service=self.token_price_info_service,
            price_analytics_service=self.price_analytics_service,
            game_repo=self.game_repo
        )

        self.all_users_analytics_service = AllUsersAnalyticsService(
            game_repo=self.game_repo
        )

        self.all_games_users_activity_service = AllGamesUserActivityService(
            all_users_analytics_service=self.all_users_analytics_service,
            game_repo=self.game_repo
        )

        self.stats_controller = StatsController(
            client_service=self.client_service,
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            activity_stats_service=self.activity_stats_service,
            social_stats_service=self.social_stats_service,
            volume_stats_service=self.volume_stats_service,
            token_price_stats_service=self.token_price_stats_service,
            game_alert_service=self.game_alert_service,
            all_games_volume_service=self.all_games_volume_service,
            all_games_price_service=self.all_games_price_service,
            all_games_users_activity_service=self.all_games_users_activity_service
        )


if __name__ == '__main__':
    container = AppContainer()

    logging.basicConfig()

    logging.getLogger().setLevel(logging.INFO)

    container.client_service.add_controller(container.info_controller)
    container.client_service.add_controller(container.stats_controller)

    logging.info("🚀 App started")

    container.client_service.listen()
