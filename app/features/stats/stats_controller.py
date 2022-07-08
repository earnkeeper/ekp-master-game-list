import asyncio
from collections import defaultdict
from pprint import pprint

from ekp_sdk.services import ClientService
from ekp_sdk.util import client_path, client_query_param

from app.features.stats.activity_stats_service import ActivityStatsService
from app.features.stats.social_stats_service import SocialStatsService
from app.features.stats.activity_stats_page import activity_tab
from app.features.stats.token_price_stats_service import TokenPriceStatsService
from app.features.stats.volume_stats_service import VolumeStatsService

STATS_TABLE_COLLECTION_NAME = "game_stats_service"


class StatsController:
    def __init__(
            self,
            client_service: ClientService,
            activity_stats_service: ActivityStatsService,
            social_stats_service: SocialStatsService,
            volume_stats_service: VolumeStatsService,
            token_price_stats_service: TokenPriceStatsService
    ):
        self.client_service = client_service
        self.activity_stats_service = activity_stats_service
        self.social_stats_service = social_stats_service
        self.volume_stats_service = volume_stats_service
        self.token_price_stats_service = token_price_stats_service
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
            activity_tab(STATS_TABLE_COLLECTION_NAME)
        )

    async def on_client_state_changed(self, sid, event):
        path = client_path(event)

        if path and (path != self.path):
            return

        await self.client_service.emit_busy(sid, STATS_TABLE_COLLECTION_NAME)

        social_document = await self.social_stats_service.get_documents()

        activity_document = await self.activity_stats_service.get_documents()

        volume_documents = await self.volume_stats_service.get_documents()

        price_documents = await self.token_price_stats_service.get_documents()

        documents_dict = defaultdict(dict)
        for document in (social_document, activity_document, volume_documents, price_documents):
            for elem in document:
                documents_dict[elem['id']].update(elem)
        all_documents = list(documents_dict.values())

        pprint(all_documents[:10])
        # for doc in all_documents:
        #     if doc["id"] == 'ape-in':
            # if "game_name" not in doc or not doc['game_name'] or doc['game_name'] == "":
            #     pprint(doc)

        await self.client_service.emit_documents(
            sid,
            STATS_TABLE_COLLECTION_NAME,
            all_documents,
        )

        await self.client_service.emit_done(sid, STATS_TABLE_COLLECTION_NAME)

        # futures = [update_socials(), update_activity(), update_volumes()]

        # await asyncio.gather(*futures)
