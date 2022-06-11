from app.features.info.activity_info_service import ActivityInfoService
from app.features.info.token_volume_info_service import TokenVolumeInfoService
from app.utils.map_get import map_get
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
        token_volume_info_service: TokenVolumeInfoService,
    ):
        self.activity_info_service = activity_info_service
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.game_repo = game_repo
        self.social_repo = social_repo
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

        banner_url = None
        price = "Coingecko"
        price_color = "normal"
        telegram_members = "Telegram"
        twitter = None
        twitter_followers = "Twitter"
        description = None

        if game["twitter"]:
            twitter = f'https://twitter.com/{game["twitter"]}'
            latest = self.social_repo.find_latest(game_id, "twitter")

            if latest is not None:
                banner_url = latest.get("banner_image_url", None)
                twitter_followers = latest.get("members", None)

        coingecko_info = await self.cache_service.wrap(
            f"coingecko_info_{game_id}_v2",
            lambda: self.coingecko_service.get_coin(game_id),
            ex=60
        )

        if coingecko_info:
            telegram_members = map_get(
                coingecko_info,
                ["community_data", "telegram_channel_user_count"]
            )
            description = map_get(coingecko_info, "description", "en")

            if "market_data" in coingecko_info:
                market_data = coingecko_info["market_data"]
                if "current_price" in market_data:
                    current_price = market_data["current_price"]
                    if currency["id"] in current_price and current_price[currency["id"]]:
                        price = f'{currency["symbol"]} {float("%.3g" % current_price[currency["id"]])}'
                if "price_change_percentage_24h" in market_data and market_data["price_change_percentage_24h"]:
                    price_change_percentage_24h = market_data["price_change_percentage_24h"]
                    price_change_percentage_24h = round(
                        price_change_percentage_24h, 1)
                    price += f' (+{price_change_percentage_24h} %)' if price_change_percentage_24h > 0 else f' ({price_change_percentage_24h} %)'
                    if price_change_percentage_24h > 0:
                        price_color = "success"
                    if price_change_percentage_24h < 0:
                        price_color = "danger"

        activity_document = await self.activity_info_service.get_activity_document(game)
        volume_document = await self.token_volume_info_service.get_volume_document(game)

        return [
            {
                "id": game_id,
                "updated": now,
                "name": game["name"],
                "banner": banner_url,
                "twitter_followers": twitter_followers,
                "telegram_members": telegram_members,
                "description": description,
                "twitter": twitter,
                "telegram": game["telegram"] if game["telegram"] and game["telegram"] != "https://t.me/" else None,
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
