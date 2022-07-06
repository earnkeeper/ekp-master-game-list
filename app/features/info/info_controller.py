from pprint import pprint

from app.features.info.info_page import page
from app.features.info.info_service import InfoService
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_path, client_currency, form_values

TABLE_COLLECTION_NAME = "game_info"
USERS_CHART_FORM_NAME = "users_chart_form"


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
            page(TABLE_COLLECTION_NAME, USERS_CHART_FORM_NAME)
        )

    async def on_client_state_changed(self, sid, event):
        path = client_path(event)

        if not path or (not path.startswith(f'{self.path}/')):
            return

        game_id = path.replace(f'{self.path}/', '')

        currency = client_currency(event)

        await self.client_service.emit_busy(sid, TABLE_COLLECTION_NAME)

        users_chart_form = form_values(event, USERS_CHART_FORM_NAME)

        users_chart_period_value = "Last 7 days"

        if users_chart_form and "period" in users_chart_form:
            users_chart_period_value = users_chart_form["period"]

        table_documents = await self.info_service.get_documents(game_id, currency, users_chart_period_value)

        await self.client_service.emit_documents(
            sid,
            TABLE_COLLECTION_NAME,
            table_documents,
            layer_id=f'{TABLE_COLLECTION_NAME}_{game_id}'
        )

        await self.client_service.emit_done(sid, TABLE_COLLECTION_NAME)
