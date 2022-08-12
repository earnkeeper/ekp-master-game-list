from app.features.info.price_analytics_service import PriceAnalyticsService
from app.features.info.user_analytics_service import UserAnalyticsService
from app.features.info.volume_analytics_service import VolumeAnalyticsService
from app.utils.proxy_image import proxy_image
from app.features.info.activity_info_service import ActivityInfoService
from app.features.info.media_info_service import MediaInfoService
from app.features.info.resources_info_service import ResourcesInfoService
from app.features.info.social_followers_info_service import SocialFollowersInfoService
from app.features.info.token_price_info_service import TokenPriceInfoService
from app.features.info.token_volume_info_service import TokenVolumeInfoService
from db.contract_aggregate_repo import ContractAggregateRepo
from db.price_repo import PriceRepo
from db.game_repo import GameRepo
from datetime import datetime
from ekp_sdk.services import CacheService, CoingeckoService

from db.social_repo import SocialRepo


class InfoService:
    def __init__(
        self,
        activity_info_service: ActivityInfoService,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
        game_repo: GameRepo,
        social_repo: SocialRepo,
        price_repo: PriceRepo,
        token_volume_info_service: TokenVolumeInfoService,
        token_price_info_service: TokenPriceInfoService,
        social_followers_info_service: SocialFollowersInfoService,
        media_info_service: MediaInfoService,
        resources_info_service: ResourcesInfoService,
        contract_aggregate_repo: ContractAggregateRepo,
        user_analytics_service: UserAnalyticsService,
        volume_analytics_service: VolumeAnalyticsService,
        price_analytics_service: PriceAnalyticsService,
        # shared_games_service: SharedGamesService
    ):
        self.activity_info_service = activity_info_service
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.game_repo = game_repo
        self.social_repo = social_repo
        self.price_repo = price_repo
        self.token_volume_info_service = token_volume_info_service
        self.token_price_info_service = token_price_info_service
        self.social_followers_info_service = social_followers_info_service
        self.media_info_service = media_info_service
        self.resources_info_service = resources_info_service
        self.contract_aggregate_repo = contract_aggregate_repo
        self.user_analytics_service = user_analytics_service
        self.volume_analytics_service = volume_analytics_service
        self.price_analytics_service = price_analytics_service
        # self.shared_games_service = shared_games_service

    async def get_documents(self, game_id, currency, users_days, volume_days, price_days, is_subscribed):
        
        game = self.game_repo.find_one_by_id(game_id)
        now = datetime.now().timestamp()

        if not game:
            return [
                {
                    "id": game_id,
                    "updated": now,
                    "name": "Unknown Game"
                }
            ]

        banner_url = game.get('banner_url', None)
        telegram_members = None
        discord_members = None
        twitter = None
        twitter_followers = None
        description = None

        latest_social_record = self.social_repo.find_latest(game_id)

        if game["twitter"]:
            twitter = f'https://twitter.com/{game["twitter"]}'

            if latest_social_record is not None:
                twitter_followers = latest_social_record.get(
                    "twitter_followers", None)

        if game["discord"]:
            if latest_social_record is not None:
                discord_members = latest_social_record.get(
                    "discord_members", None)

        if game["telegram"]:
            if latest_social_record is not None:
                telegram_members = latest_social_record.get(
                    "telegram_members", None)

        rate = 1

        if currency["id"] != "usd":
            rate = await self.cache_service.wrap(
                f"coingecko_price_usd_{currency['id']}",
                lambda: self.coingecko_service.get_latest_price(
                    'usd-coin', currency["id"]),
                ex=3600
            )

        if twitter_followers is None:
            twitter_followers = "Twitter"

        if discord_members is None:
            discord_members = "Discord"

        if telegram_members is None:
            telegram_members = "Telegram"

        description = game.get("description", None)

        activity_document = await self.activity_info_service.get_activity_document(game)
        social_document = await self.social_followers_info_service.get_social_document(game)
        media_documents = await self.media_info_service.get_media_documents(game)
        resources_documents = await self.resources_info_service.get_resources_documents(game)

        price_records = self.token_price_info_service.get_price_records(game)
        price_document = await self.token_price_info_service.get_price_document(price_records, game, rate)
        price_period_chart = self.price_analytics_service.get_period_chart(price_days, price_records)
        price_last_period_chart = self.price_analytics_service.get_last_period_chart(price_days, price_records)

        volume_records = await self.token_volume_info_service.get_volume_records(game)
        volume_document = await self.token_volume_info_service.get_volume_document(volume_records, game, rate)
        volume_period_chart = self.volume_analytics_service.get_period_chart(volume_days, volume_records)
        volume_last_period_chart = self.volume_analytics_service.get_last_period_chart(volume_days, volume_records)
        volume_period_total = self.volume_analytics_service.get_period_total(volume_days, volume_records)

        users_period_chart = self.user_analytics_service.get_period_chart(game, users_days)
        users_last_period_chart = self.user_analytics_service.get_last_period_chart(game, users_days)
        users_period_count = self.user_analytics_service.get_period_users(game, users_days)

        # shared_games_service = self.shared_games_service.get_games()

        telegram = game["telegram"] if (
            game["telegram"] and game["telegram"] != "https://t.me/") else None
        
        if telegram and not telegram.startswith("http"):
            telegram = f"https://t.me/{telegram}"
            
        stats_available = activity_document is not None or volume_document is not None or price_document is not None or social_document is not None
        
        coingecko_link = None
        
        if price_document and isinstance(game['coin_ids'], list) and len(game['coin_ids']):
            coingecko_link = f"https://www.coingecko.com/en/coins/{game['coin_ids'][0]}"
        
        return [
            {
                "id": game_id,
                "updated": now,
                "name": game["name"],
                "banner": proxy_image(banner_url),
                "twitter_followers": twitter_followers,
                "telegram_members": telegram_members,
                "discord_members": discord_members,
                "description": description,
                "twitter": twitter,
                "telegram": telegram,
                "discord": game["discord"],
                "website": game["website"],
                "activity": activity_document,
                "is_subscribed": is_subscribed,
                "volume": volume_document,
                "social": social_document,
                "price": price_document,
                "media": media_documents,
                "resources": resources_documents,
                "analytics_available": len(price_last_period_chart) or len(volume_period_chart) or len(users_period_chart),
                "analytics_price": {
                    "price_period_chart": price_period_chart,
                    "price_last_period_chart": price_last_period_chart,
                },
                "analytics_volume": {
                    "volume_period_chart": volume_period_chart,
                    "volume_last_period_chart": volume_last_period_chart,
                },
                "analytics_users": {
                    "users_period_chart": users_period_chart,
                    "users_last_period_chart": users_last_period_chart,
                },
                "coingecko": f"https://www.coingecko.com/en/coins/{game['id']}" if price_document else None,
                "users_period_chart": users_period_chart,
                "users_last_period_chart": users_last_period_chart,
                "coingecko": coingecko_link,
                "statsAvailable": stats_available,
                "fiat_symbol": currency['symbol'],
            }
        ]
