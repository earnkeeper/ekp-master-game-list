from pprint import pprint
from app.features.info.activity_info_service import ActivityInfoService
from app.features.info.token_volume_info_service import TokenVolumeInfoService
from db.game_repo import GameRepo
from datetime import datetime
from ekp_sdk.services import CacheService, CoingeckoService


class InfoService:
    def __init__(
        self,
        activity_info_service: ActivityInfoService,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
        game_repo: GameRepo,
        token_volume_info_service: TokenVolumeInfoService,
    ):
        self.activity_info_service = activity_info_service
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.game_repo = game_repo
        self.token_volume_info_service = token_volume_info_service
        
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
        
        if game["twitter"]:
            twitter = f'https://twitter.com/{game["twitter"]}'

        activity_document = await self.activity_info_service.get_activity_document(game)
        volume_document = await self.token_volume_info_service.get_volume_document(game)
            
        return [
            {
                "id": game_id,
                "updated": now,
                "name": game["name"],
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