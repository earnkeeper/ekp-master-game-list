
import asyncio
import logging

from decouple import AutoConfig
from ekp_sdk import BaseContainer

from db.game_repo import GameRepo
from sync.coingecko_config_service import CoingeckoConfigService
from sync.sheets_config_service import SheetsConfigService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        SHEET_ID = config("SHEET_ID")

        # DB

        self.game_repo = GameRepo(
            mg_client=self.mg_client,
        )

        # Services

        self.sheets_config_service = SheetsConfigService(
            google_sheets_client=self.google_sheets_client,
            game_repo = self.game_repo,
            sheet_id=SHEET_ID
        )

        self.coingecko_config_service = CoingeckoConfigService(
            coingecko_service=self.coingecko_service,
            cache_service=self.cache_service,
            game_repo = self.game_repo
        )



if __name__ == '__main__':
    container = AppContainer()

    logging.basicConfig(level=logging.INFO)

    logging.info("🚀 Application Start")

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        container.sheets_config_service.sync_games()
    )
    
    loop.run_until_complete(
        container.coingecko_config_service.sync_games()
    )
