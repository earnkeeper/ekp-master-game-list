import asyncio
import logging

from decouple import AutoConfig
from ekp_sdk import BaseContainer

from db.resouces_repo import ResourcesRepo
from sync.resources_sync_service import ResourcesSyncService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        SHEET_ID = config("SHEET_ID")

        self.resources_repo = ResourcesRepo(
            mg_client=self.mg_client
        )

        # Services

        self.resources_sync_service = ResourcesSyncService(
            google_sheets_client=self.google_sheets_client,
            resources_repo=self.resources_repo,
            sheet_id=SHEET_ID
        )


if __name__ == '__main__':
    container = AppContainer()

    logging.basicConfig()

    logging.getLogger().setLevel(logging.INFO)

    logging.info("🚀 Application Start")

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        container.resources_sync_service.sync_resources()
    )
