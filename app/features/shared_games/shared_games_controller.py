from pprint import pprint
from app.features.info.info_page import page
from app.features.info.info_service import InfoService
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_path, client_currency, form_values

SHARED_GAMES_COLLECTION_NAME = "game_info"
# TABLE_COLLECTION_NAME = "game_info"
# USERS_CHART_NAME = "users"
# VOLUME_CHART_NAME = "volume"
# PRICE_CHART_NAME = "price"
from app.features.shared_games.shared_games_service import SharedGamesService


class SharedGamesController:
    def __init__(
            self,
            client_service: ClientService,
            shared_games_service: SharedGamesService
    ):
        self.client_service = client_service
        self.shared_games_service = shared_games_service
        self.path = 'shared'

    # async def on_connect(self, sid):
    #     await self.client_service.emit_page(
    #         sid,
    #         f'{self.path}/:gameId',
    #         page(TABLE_COLLECTION_NAME, USERS_CHART_NAME, VOLUME_CHART_NAME, PRICE_CHART_NAME)
    #     )

    async def on_client_state_changed(self, sid, event):
        path = client_path(event)

        if not path or (not path.startswith(f'{self.path}/')):
            return

        game_id = path.replace(f'{self.path}/', '')

        shared_game_documents = self.shared_games_service.get_games()

        await self.client_service.emit_documents(
            sid,
            SHARED_GAMES_COLLECTION_NAME,
            shared_game_documents,
            layer_id=f'{SHARED_GAMES_COLLECTION_NAME}_{game_id}'
        )

        await self.client_service.emit_done(sid, SHARED_GAMES_COLLECTION_NAME)


def client_is_subscribed(event):
    if (event is None):
        return False

    if ("state" not in event.keys()):
        return False

    if ("client" not in event["state"].keys()):
        return False

    if ("subscribed" not in event["state"]["client"].keys()):
        return False

    return event["state"]["client"]["subscribed"]
