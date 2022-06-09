from ekp_sdk.services import ClientService
from ekp_sdk.util import  client_path

from app.features.stats.activity_stats_service import ActivityStatsService
from app.features.stats.stats_page import stats_page

ACTIVITY_TABLE_COLLECTION_NAME = "game_stats_activity"

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
            self.path,
            stats_page(ACTIVITY_TABLE_COLLECTION_NAME)
        )
    
    async def on_client_state_changed(self, sid, event):
        path = client_path(event)

        if not path or (path != self.path):
            return
        
        await self.client_service.emit_busy(sid, ACTIVITY_TABLE_COLLECTION_NAME)

        table_documents = await self.activity_stats_service.get_documents()
        
        await self.client_service.emit_documents(
            sid,
            ACTIVITY_TABLE_COLLECTION_NAME,
            table_documents,
        )

        await self.client_service.emit_done(sid, ACTIVITY_TABLE_COLLECTION_NAME)
