from ekp_sdk.services import CacheService, CoingeckoService


class CoingeckoSyncService:
    def __init__(
        self,
        coingecko_service: CoingeckoService,
        cache_service: CacheService,
    ):
        self.coingecko_service = coingecko_service
        self.cache_service = cache_service
        self.page_size = 50

    async def __add_category_to_games(self, category, games_map):
        
        markets = await self.cache_service.wrap(
            f"coingecko_markets_{category}",
            lambda: self.__get_markets(category),
            ex=3600
        )
        
        for market in markets:
            id = market['id']
            
            if id in games_map:
                continue

            games_map[id] = {
                "id": id,
                "coin_ids": [id],
                "disable": False,
                "tokens": {
                    "bsc": [],
                    "eth": [],
                    "polygon": [],
                },
                "twitter": None,
                "telegram": None,
                "website": None,
                "discord": None,
                "description": None
            }
        
        
    async def get_games(self):

        games_map = {}
        
        await self.__add_category_to_games("gaming", games_map)
        await self.__add_category_to_games("play-to-earn", games_map)
        await self.__add_category_to_games("move-to-earn", games_map)
        
        return list(games_map.values())


    async def __get_markets(self, category):
        page = 1

        markets = []

        while True:
            next_markets = await self.coingecko_service.get_coin_markets(page=page, per_page=self.page_size, category=category)

            if not len(next_markets):
                break

            for market in next_markets:
                markets.append(market)

            if len(next_markets) < self.page_size:
                break

            page += 1

        return markets
