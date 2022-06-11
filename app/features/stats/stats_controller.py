from ekp_sdk.services import ClientService
from ekp_sdk.util import client_path, client_query_param

from app.features.stats.activity_stats_service import ActivityStatsService
from app.features.stats.social_stats_service import SocialStatsService
from app.features.stats.stats_page import stats_page
from app.features.stats.volume_stats_service import VolumeStatsService

SOCIAL_TABLE_COLLECTION_NAME = "game_stats_social"
ACTIVITY_TABLE_COLLECTION_NAME = "game_stats_activity"
VOLUME_TABLE_COLLECTION_NAME = "game_stats_volume"


class StatsController:
    def __init__(
        self,
        client_service: ClientService,
        activity_stats_service: ActivityStatsService,
        social_stats_service: SocialStatsService,
        volume_stats_service: VolumeStatsService
    ):
        self.client_service = client_service
        self.activity_stats_service = activity_stats_service
        self.social_stats_service = social_stats_service
        self.volume_stats_service = volume_stats_service
        self.path = 'stats'
        

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'activity',
            'Games',
            self.path
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            stats_page(ACTIVITY_TABLE_COLLECTION_NAME, VOLUME_TABLE_COLLECTION_NAME, SOCIAL_TABLE_COLLECTION_NAME)
        )
    
    async def on_client_state_changed(self, sid, event):
        path = client_path(event)

        if not path or (path != self.path):
            return
        
        tab_param = client_query_param(event, "tab")
        

        if tab_param is None:
            tab_param = 0

        tab_param = int(tab_param)
        
        if tab_param == 0:
            await self.client_service.emit_busy(sid, SOCIAL_TABLE_COLLECTION_NAME)
            
            social_document = await self.social_stats_service.get_documents()
            
            await self.client_service.emit_documents(
                sid,
                SOCIAL_TABLE_COLLECTION_NAME,
                social_document,
            )
            
            await self.client_service.emit_done(sid, SOCIAL_TABLE_COLLECTION_NAME)
                    
        if tab_param == 1:
            await self.client_service.emit_busy(sid, ACTIVITY_TABLE_COLLECTION_NAME)
            
            social_document = await self.activity_stats_service.get_documents()
            
            await self.client_service.emit_documents(
                sid,
                ACTIVITY_TABLE_COLLECTION_NAME,
                social_document,
            )
            
            await self.client_service.emit_done(sid, ACTIVITY_TABLE_COLLECTION_NAME)

        if tab_param == 2:
            await self.client_service.emit_busy(sid, VOLUME_TABLE_COLLECTION_NAME)

            volume_documents = await self.volume_stats_service.get_documents()
            
            await self.client_service.emit_documents(
                sid,
                VOLUME_TABLE_COLLECTION_NAME,
                volume_documents,
            )

            await self.client_service.emit_done(sid, VOLUME_TABLE_COLLECTION_NAME)