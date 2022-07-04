
import asyncio
import logging

from decouple import AutoConfig
from ekp_sdk import BaseContainer

from db.game_repo import GameRepo
from sync.coingecko_sync_service import CoingeckoSyncService
from sync.eth_sync_service import EthSyncService
from sync.game_sync_service import GameSyncService
from sync.manual_sync_service import ManualSyncService
from ekp_sdk.db import MgClient

class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        SHEET_ID = config("SHEET_ID")

        MONGO_URI_ETH = config("MONGO_URI_ETH")
        MONGO_DB_NAME = config('MONGO_DB_NAME')
        
        self.mg_client_eth = MgClient(
            uri=MONGO_URI_ETH,
            db_name=MONGO_DB_NAME
        )

        self.game_repo = GameRepo(
            mg_client=self.mg_client,
        )

        self.game_repo_eth = GameRepo(
            mg_client=self.mg_client_eth
        )

        # Services

        self.manual_sync_service = ManualSyncService(
            google_sheets_client=self.google_sheets_client,
            sheet_id=SHEET_ID
        )

        self.coingecko_sync_service = CoingeckoSyncService(
            coingecko_service=self.coingecko_service,
            cache_service=self.cache_service,
        )

        self.game_sync_service = GameSyncService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            coingecko_sync_service=self.coingecko_sync_service,
            game_repo=self.game_repo,
            manual_sync_service=self.manual_sync_service,
        )

        self.eth_sync_service = EthSyncService(
            game_repo=self.game_repo,
            game_repo_eth=self.game_repo_eth
        )


if __name__ == '__main__':
    container = AppContainer()

    logging.basicConfig()

    logging.getLogger().setLevel(logging.INFO)

    logging.info("🚀 Application Start")

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        container.game_sync_service.sync_games()
    )

    loop.run_until_complete(
        container.eth_sync_service.sync_games()
    )
