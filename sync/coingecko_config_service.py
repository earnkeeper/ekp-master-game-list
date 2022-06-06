from db.game_repo import GameRepo
from ekp_sdk.services import CacheService, CoingeckoService


class CoingeckoConfigService:
    def __init__(
        self,
        coingecko_service: CoingeckoService,
        cache_service: CacheService,
        game_repo: GameRepo,
    ):
        self.coingecko_service = coingecko_service
        self.game_repo = game_repo
        self.cache_service = cache_service
        self.page_size = 50

    async def get_coin_map(self):
        coins = await self.coingecko_service.get_coins()

        coin_map = {}

        for coin in coins:
            if "platforms" not in coin:
                continue

            platforms = coin["platforms"]

            if ("binance-smart-chain" not in platforms) and ("ethereum" not in platforms) and ("polygon-pos" not in platforms):
                continue

            coin_map[coin["id"]] = coin

        return coin_map

    async def get_markets(self):
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

    async def sync_games(self):

        coin_map = await self.cache_service.wrap(
            "coingecko_coin_map",
            lambda: self.get_coin_map(),
            ex=3600
        )

        # ----------------------

        markets = await self.cache_service.wrap(
            "coingecko_markets",
            lambda: self.get_markets(),
            ex=3600
        )
        coingecko_game_ids = list(
            map(
                lambda market: market['id'],
                markets
            ),
        )

        # ----------------------
        existing_games = self.game_repo.find_by_source("coingecko")

        existing_games_map = {}

        for game in existing_games:
            existing_games_map[game["id"]] = 1

        # ----------------------
        manual_games = self.game_repo.find_by_source("manual")

        manual_games_map = {}

        for game in manual_games:
            id = game['id']
            manual_games_map[id] = game
            if id in coingecko_game_ids:
                if game['disable']:
                    coingecko_game_ids.remove(id)
            else:
                if not game['disable']:
                    coingecko_game_ids.append(id)

        # ----------------------
        for id in coingecko_game_ids:
            if (id in existing_games_map) or (id not in coin_map):
                continue

            coin = await self.cache_service.wrap(
                f"coin_{id}",
                lambda: self.coingecko_service.get_coin(id),
                ex=3600
            )
            
            platforms = coin_map[id]["platforms"]

            bsc_tokens = []
            eth_tokens = []
            polygon_tokens = []

            if "binance-smart-chain" in platforms:
                bsc_tokens.append(platforms["binance-smart-chain"])

            if "ethereum" in platforms:
                eth_tokens.append(platforms["ethereum"])

            if "polygon-pos" in platforms:
                polygon_tokens.append(platforms["polygon-pos"])

            twitter = None
            website = None
            discord = None
            telegram = None

            if "links" in coin:
                if ("homepage" in coin["links"]) and len(coin["links"]["homepage"]):
                    website = coin["links"]["homepage"][0]
                if "twitter_screen_name" in coin["links"]:
                    twitter = coin["links"]["twitter_screen_name"]
                if "telegram_channel_identifier" in coin["links"]:
                    telegram = f"https://t.me/{coin['links']['telegram_channel_identifier']}"
                if "chat_url" in coin["links"]:
                    for chat in coin["links"]["chat_url"]:
                        if ("discord.com" in chat or "discord.gg" in chat):
                            discord = chat
                        if "t.me" in chat:
                            telegram = chat

            game = {
                "id": id,
                "disable": False,
                "name": coin["name"],
                "source": "coingecko",
                "tokens": {
                    "bsc": bsc_tokens,
                    "eth": eth_tokens,
                    "polygon": polygon_tokens,
                },
                "twitter": twitter,
                "telegram": telegram,
                "website": website,
                "discord": discord,
            }

            self.game_repo.save([game])
