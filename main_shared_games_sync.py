import asyncio
import logging

from decouple import AutoConfig
from ekp_sdk import BaseContainer
from ekp_sdk.db import MgClient

from db.game_repo import GameRepo
from db.resources_repo import ResourcesRepo
from db.shared_games_repo import SharedGamesRepo
from db.transaction_repo import TransactionRepo
from sync.resources_sync_service import ResourcesSyncService
from sync.shared_games_sync_service import SharedGamesSyncService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        MONGO_URI_BSC = config("MONGO_URI_BSC")
        MONGO_DB_NAME = config('MONGO_DB_NAME')

        self.mg_client_bsc = MgClient(
            uri=MONGO_URI_BSC,
            db_name=MONGO_DB_NAME
        )


        self.transaction_repo_bsc = TransactionRepo(
            mg_client=self.mg_client_bsc
        )

        self.game_repo_bsc = GameRepo(
            mg_client=self.mg_client_bsc
        )

        self.shared_games_repo_bsc = SharedGamesRepo(
            mg_client=self.mg_client_bsc
        )

        # Services

        self.shared_games_sync_service = SharedGamesSyncService(
            transaction_repo=self.transaction_repo_bsc,
            game_repo=self.game_repo_bsc,
            shared_games_repo=self.shared_games_repo_bsc
        )

        # self.resources_sync_service = ResourcesSyncService(
        #     google_sheets_client=self.google_sheets_client,
        #     resources_repo=self.resources_repo,
        #     sheet_id=SHEET_ID
        # )


if __name__ == '__main__':
    container = AppContainer()

    logging.basicConfig()

    logging.getLogger().setLevel(logging.INFO)

    logging.info("🚀 Application Start")

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        container.shared_games_sync_service.sync_shared_games()
    )
