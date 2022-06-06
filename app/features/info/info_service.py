from pprint import pprint
from app.features.info.activity_service import ActivityService
from db.game_repo import GameRepo
from datetime import datetime
from ekp_sdk.services import CacheService, CoingeckoService


class InfoService:
    def __init__(
        self,
        activity_service: ActivityService,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
        game_repo: GameRepo,
    ):
        self.activity_service = activity_service
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.game_repo = game_repo

    async def get_documents(self, game_id):
        game = self.game_repo.find_one_by_id(game_id)
        
        activity_document = await self.activity_service.get_activity_document(game)
        
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
                "activity": activity_document
            }
        ]
