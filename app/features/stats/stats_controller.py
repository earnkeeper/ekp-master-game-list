from app.features.info.info_page import page
from ekp_sdk.services import ClientService
from ekp_sdk.util import  client_path

from app.features.stats.activity_stats_service import ActivityStatsService

TABLE_COLLECTION_NAME = "game_stats"

class StatsController:
    def __init__(
        self,
        client_service: ClientService,
        activity_stats_service: ActivityStatsService
    ):
        self.client_service = client_service
        self.activity_stats_service = activity_stats_service
        self.path = 'stats'

    async def on_connect(self, sid):
        await self.client_service.emit_page(
            sid,
            f'{self.path}/:gameId',
            page(TABLE_COLLECTION_NAME)
        )
    
    async def on_client_state_changed(self, sid, event):
        path = client_path(event)

        if not path or (not path.startswith(f'{self.path}/')):
            return
        
        game_id = path.replace(f'{self.path}/', '')
        
        await self.client_service.emit_busy(sid, TABLE_COLLECTION_NAME)

        table_documents = await self.activity_stats_service.get_documents(game_id)
        
        await self.client_service.emit_documents(
            sid,
            TABLE_COLLECTION_NAME,
            table_documents,
            layer_id=f'{TABLE_COLLECTION_NAME}_{game_id}'
        )

        await self.client_service.emit_done(sid, TABLE_COLLECTION_NAME)
