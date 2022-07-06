from pprint import pprint

from app.features.info.user_aggregate_service import UserAggregateService
from app.utils.proxy_image import proxy_image
from app.features.info.activity_info_service import ActivityInfoService
from app.features.info.media_info_service import MediaInfoService
from app.features.info.resources_info_service import ResourcesInfoService
from app.features.info.social_followers_info_service import SocialFollowersInfoService
from app.features.info.token_price_info_service import TokenPriceInfoService
from app.features.info.token_volume_info_service import TokenVolumeInfoService
from db.contract_aggregate_repo import ContractAggregateRepo
from db.price_repo import PriceRepo
from shared.map_get import map_get
from db.game_repo import GameRepo
from datetime import datetime
from ekp_sdk.services import CacheService, CoingeckoService, TwitterClient

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
        user_aggregate_service: UserAggregateService
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
        self.user_aggregate_service = user_aggregate_service

    async def get_documents(self, game_id, currency):
        
        game = self.game_repo.find_one_by_id(game_id)

        # eth_addresses = game['tokens']['eth']
        #
        # if len(eth_addresses):
        #     results = self.contract_aggregate_repo.get_since(eth_addresses, 0)
        #     print(len(results))
        
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

        price_records = self.price_repo.find_by_game_id(game["id"])

        price_records.sort(key=lambda record: record['timestamp'])

        price = None
        price_change = None
        price_change_pc = None
        price_color = "normal"

        rate = 1

        if currency["id"] != "usd":
            rate = await self.cache_service.wrap(
                f"coingecko_price_usd_{currency['id']}",
                lambda: self.coingecko_service.get_latest_price(
                    'usd-coin', currency["id"]),
                ex=3600
            )

        if len(price_records):
            current_price = price_records[-1]["price_usd"]
            price = f'{currency["symbol"]} {float("%.3g" % (current_price * rate))}'

            if len(price_records) > 1:
                yesterday_price = price_records[-2]["price_usd"]
                price_change = current_price - yesterday_price
                price_change_pc = price_change * 100 / yesterday_price
                price_change_pc = round(price_change_pc, 2)
                price += f' (+{price_change_pc} %)' if price_change_pc > 0 else f' ({price_change_pc} %)'
                if price_change_pc > 0:
                    price_color = "success"
                if price_change_pc < 0:
                    price_color = "danger"

        if twitter_followers is None:
            twitter_followers = "Twitter"

        if discord_members is None:
            discord_members = "Discord"

        if telegram_members is None:
            telegram_members = "Telegram"

        description = game.get("description", None)

        activity_document = await self.activity_info_service.get_activity_document(game)
        volume_document = await self.token_volume_info_service.get_volume_document(game, rate)
        price_document = await self.token_price_info_service.get_price_document(game, rate, currency['symbol'])
        social_document = await self.social_followers_info_service.get_social_document(game)
        media_documents = await self.media_info_service.get_media_documents(game)
        resources_documents = await self.resources_info_service.get_resources_documents(game)
        users_period_chart = self.user_aggregate_service.get_period_chart(game, 7)
        users_last_period_chart = self.user_aggregate_service.get_last_period_chart(game, 7)

        pprint(users_period_chart)
        telegram = game["telegram"] if (
            game["telegram"] and game["telegram"] != "https://t.me/") else None
        
        if telegram and not telegram.startswith("http"):
            telegram = f"https://t.me/{telegram}"
            
        stats_available = activity_document is not None or volume_document is not None or price_document is not None or social_document is not None
        
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
                "volume": volume_document,
                "social": social_document,
                "media": media_documents,
                "resources": resources_documents,
                "users_period_chart": users_period_chart,
                "users_last_period_chart": users_last_period_chart,
                "price_doc": price_document,
                "coingecko": f"https://www.coingecko.com/en/coins/{game['id']}" if price else None,
                "statsAvailable": stats_available,
                "fiat_symbol": currency['symbol'],
                "price": price,
                "price_color": price_color,
            }
        ]
