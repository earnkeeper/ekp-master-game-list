from pprint import pprint
from app.features.info.info_page import page
from app.features.info.info_service import InfoService
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_path, client_currency, form_values

TABLE_COLLECTION_NAME = "game_info"
USERS_CHART_NAME = "users"
VOLUME_CHART_NAME = "volume"
PRICE_CHART_NAME = "price"


class InfoController:
    def __init__(
            self,
            client_service: ClientService,
            info_service: InfoService
    ):
        self.client_service = client_service
        self.info_service = info_service
        self.path = 'info'

    async def on_connect(self, sid):
        await self.client_service.emit_page(
            sid,
            f'{self.path}/:gameId',
            page(TABLE_COLLECTION_NAME, USERS_CHART_NAME, VOLUME_CHART_NAME, PRICE_CHART_NAME)
        )

    async def on_client_state_changed(self, sid, event):
        path = client_path(event)

        if not path or (not path.startswith(f'{self.path}/')):
            return

        is_subscribed = client_is_subscribed(event)

        game_id = path.replace(f'{self.path}/', '')

        currency = client_currency(event)

        await self.client_service.emit_busy(sid, TABLE_COLLECTION_NAME)

        users_chart_form = form_values(event, f"chart_{USERS_CHART_NAME}")

        users_days = 7

        if users_chart_form and "days" in users_chart_form:
            users_days = users_chart_form["days"]

        volume_chart_form = form_values(event, f"chart_{VOLUME_CHART_NAME}")

        volume_days = 7

        if volume_chart_form and "days" in volume_chart_form:
            volume_days = volume_chart_form["days"]

        price_chart_form = form_values(event, f"chart_{PRICE_CHART_NAME}")

        price_days = 7

        if price_chart_form and "days" in price_chart_form:
            price_days = price_chart_form["days"]

        table_documents = await self.info_service.get_documents(game_id, currency, users_days, volume_days, price_days,
                                                                is_subscribed)

        await self.client_service.emit_documents(
            sid,
            TABLE_COLLECTION_NAME,
            table_documents,
            layer_id=f'{TABLE_COLLECTION_NAME}_{game_id}'
        )

        await self.client_service.emit_done(sid, TABLE_COLLECTION_NAME)


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
