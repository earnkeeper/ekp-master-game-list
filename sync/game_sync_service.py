import logging
from db.game_repo import GameRepo
from shared.map_get import map_get
from ekp_sdk.services import CacheService, CoingeckoService
from sync.coingecko_sync_service import CoingeckoSyncService
from sync.manual_sync_service import ManualSyncService


class GameSyncService:
    def __init__(
        self,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
        coingecko_sync_service: CoingeckoSyncService,
        game_repo: GameRepo,
        manual_sync_service: ManualSyncService,
    ):
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.coingecko_sync_service = coingecko_sync_service
        self.game_repo = game_repo
        self.manual_sync_service = manual_sync_service

    async def sync_games(self):
        manual_games = self.manual_sync_service.get_games()

        coingecko_games = await self.coingecko_sync_service.get_games()

        games = self.__merge_lists(manual_games, coingecko_games)

        for game in games:
            if game['disable']:
                self.game_repo.upsert(game)
                continue

            for coin_id in game['coin_ids']:
                coin = await self.cache_service.wrap(
                    f"coin_{coin_id}",
                    lambda: self.coingecko_service.get_coin(coin_id),
                    ex=3600
                )

                if not coin:
                    logging.warn(f"Could not get coingecko info for {coin_id}")
                    continue

                self.__update_game_field(game, "name", coin["name"])
                self.__update_game_field(game, "website", map_get(
                    coin, ["links", "homepage", 0]
                ))
                self.__update_game_field(game, "twitter", map_get(
                    coin, ["links", "twitter_screen_name"]
                ))
                self.__update_game_field(game, "telegram", map_get(
                    coin, ["links", "telegram_channel_identifier"]
                ))

                chat_url = map_get(coin, ["links", "chat_url"])

                if chat_url:
                    for chat in chat_url:
                        if ("discord.com" in chat or "discord.gg" in chat):
                            self.__update_game_field(game, "discord", chat)
                        if "t.me" in chat:
                            self.__update_game_field(game, "telegram", chat)

                platforms = coin["platforms"]

                if "binance-smart-chain" in platforms:
                    token = platforms["binance-smart-chain"]
                    if token not in game['tokens']['bsc']:
                        game['tokens']['bsc'].append(token)

                if "ethereum" in platforms:
                    token = platforms["ethereum"]
                    if token not in game['tokens']['eth']:
                        game['tokens']['eth'].append(token)

                if "polygon-pos" in platforms:
                    token = platforms["polygon-pos"]
                    if token not in game['tokens']['polygon']:
                        game['tokens']['polygon'].append(token)

            self.game_repo.upsert(game)

    def __update_game_field(self, game, key, value):
        if not value:
            return

        if key in game and game[key]:
            return

        game[key] = value

    def __merge_lists(self, manual_games, coingecko_games):
        games_map = {}

        for game in manual_games:
            games_map[game['id']] = game

        for game in coingecko_games:
            game_id = game['id']

            if game_id not in games_map:
                games_map[game_id] = game
                continue

            existing_game = games_map[game_id]

            for coin_id in game['coin_ids']:
                if coin_id not in existing_game['coin_ids']:
                    existing_game['coin_ids'].append(coin_id)

        return games_map.values()
