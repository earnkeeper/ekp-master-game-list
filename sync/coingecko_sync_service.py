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

    async def get_games(self):

        markets = await self.cache_service.wrap(
            "coingecko_markets",
            lambda: self.__get_markets(),
            ex=3600
        )

        games = []

        for market in markets:
            id = market['id']

            games.append({
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
            })

        return games

    async def __get_markets(self):
        page = 1

        markets = []

        while True:
            next_markets = await self.coingecko_service.get_coin_markets(page=page, per_page=self.page_size, category="gaming")

            if not len(next_markets):
                break

            for market in next_markets:
                markets.append(market)

            if len(next_markets) < self.page_size:
                break

            page += 1

        return markets
