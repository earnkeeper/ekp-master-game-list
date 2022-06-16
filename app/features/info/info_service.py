from app.features.info.activity_info_service import ActivityInfoService
from app.features.info.token_volume_info_service import TokenVolumeInfoService
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
    ):
        self.activity_info_service = activity_info_service
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.game_repo = game_repo
        self.social_repo = social_repo
        self.price_repo = price_repo
        self.token_volume_info_service = token_volume_info_service

    async def get_documents(self, game_id, currency):
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
        # price = "Coingecko"
        # price_color = "normal"
        telegram_members = None
        discord_members = None
        twitter = None
        twitter_followers = None
        description = None

        latest_social_record = self.social_repo.find_latest(game_id)
        
        if game["twitter"]:
            twitter = f'https://twitter.com/{game["twitter"]}'

            if latest_social_record is not None:
                twitter_followers = latest_social_record.get("twitter_followers", None)

        if game["discord"]:
            if latest_social_record is not None:
                discord_members = latest_social_record.get("discord_members", None)

        if game["telegram"]:
            if latest_social_record is not None:
                telegram_members = latest_social_record.get("telegram_members", None)

        price_records = self.price_repo.find_by_game_id(game["id"])

        price_records.sort(key=lambda record: record['timestamp'])

        price = None
        price_change = None
        price_change_pc = None
        price_color = "normal"

        if len(price_records):
            current_price = price_records[-1]["price_usd"]
            price = f'{currency["symbol"]} {float("%.3g" % current_price)}'

            if len(price_records) > 1:
                yesterday_price = price_records[-2]["price_usd"]
                price_change = current_price - yesterday_price
                price_change_pc = price_change * 100 / yesterday_price
                price += f' (+{price_change_pc} %)' if price_change_pc > 0 else f' ({price_change_pc} %)'
                if price_change_pc > 0:
                    price_color = "success"
                if price_change_pc < 0:
                    price_color = "danger"
        
        coingecko_info = None
        
        if twitter_followers is None:
            twitter_followers = "Twitter"
        
        if discord_members is None:
            discord_members = "Discord"
        
        if telegram_members is None:
            telegram_members = "Telegram"
        
        description = game.get("description", None)



        activity_document = await self.activity_info_service.get_activity_document(game)
        volume_document = await self.token_volume_info_service.get_volume_document(game)

        telegram = game["telegram"] if (game["telegram"] and game["telegram"] != "https://t.me/") else None
        if telegram and not telegram.startswith("http"):
            telegram = f"https://t.me/{telegram}"
        return [
            {
                "id": game_id,
                "updated": now,
                "name": game["name"],
                "banner": banner_url,
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
                "coingecko": f"https://www.coingecko.com/en/coins/{game['id']}" if coingecko_info else None,
                "statsAvailable": activity_document is not None or volume_document is not None,
                "fiat_symbol": currency['symbol'],
                "price": price,
                "price_color": price_color,
            }
        ]
