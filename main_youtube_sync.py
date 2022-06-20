import asyncio
import logging

from decouple import AutoConfig
from ekp_sdk import BaseContainer

from db.game_repo import GameRepo
from db.youtube_repo import YoutubeRepo
from sync.youtube_game_list_service import YoutubeSyncService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        # DB

        self.game_repo = GameRepo(
            mg_client=self.mg_client,
        )

        self.youtube_repo = YoutubeRepo(
            mg_client=self.mg_client
        )

        # Services

        self.youtube_sync_service = YoutubeSyncService(
            game_repo=self.game_repo,
            youtube_repo=self.youtube_repo,
            cache_service=self.cache_service
        )


if __name__ == '__main__':
    container = AppContainer()

    logging.basicConfig()

    logging.getLogger().setLevel(logging.INFO)

    logging.info("🚀 Application Start")

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        container.youtube_sync_service.sync_youtube_games_info()
    )
