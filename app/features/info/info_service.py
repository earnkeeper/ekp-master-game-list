from app.features.info.activity_info_service import ActivityInfoService
from app.features.info.token_volume_info_service import TokenVolumeInfoService
from db.game_repo import GameRepo
from datetime import datetime
from ekp_sdk.services import CacheService, CoingeckoService, TwitterClient


class InfoService:
    def __init__(
        self,
        activity_info_service: ActivityInfoService,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
        game_repo: GameRepo,
        token_volume_info_service: TokenVolumeInfoService,
        twitter_client: TwitterClient,
    ):
        self.activity_info_service = activity_info_service
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.game_repo = game_repo
        self.token_volume_info_service = token_volume_info_service
        self.twitter_client = twitter_client
        
    async def get_documents(self, game_id):
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

        coingecko_info = await self.cache_service.wrap(
            f"coingecko_info_{game_id}",
            lambda: self.coingecko_service.get_coin(game_id)
        )
        
        
        twitter = None
        twitter_user_info = None
        
        if game["twitter"]:
            twitter = f'https://twitter.com/{game["twitter"]}'
            twitter_user_info = await self.cache_service.wrap(
                f"twitter_info_{game['twitter']}",
                lambda: self.twitter_client.get_user_info_by_screen_name(game['twitter']),
                ex=3600
            )

        activity_document = await self.activity_info_service.get_activity_document(game)
        volume_document = await self.token_volume_info_service.get_volume_document(game)
            
        return [
            {
                "id": game_id,
                "updated": now,
                "name": game["name"],
                "banner": twitter_user_info["profile_banner_url"] if twitter_user_info else None,
                "twitter_followers": twitter_user_info["followers_count"] if twitter_user_info else "Twitter",
                "description": coingecko_info["description"]["en"],
                "twitter": twitter,
                "telegram": game["telegram"],
                "discord": game["discord"],
                "website": game["website"],
                "activity": activity_document,
                "volume": volume_document,
                "statsAvailable": activity_document is not None or volume_document is not None
            }
        ]
