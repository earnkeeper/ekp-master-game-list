from pprint import pprint

from shared.get_midnight_utc import get_midnight_utc
from app.utils.proxy_image import proxy_image
from db.activity_repo import ActivityRepo
from db.game_repo import GameRepo
from datetime import datetime
import copy


class AllGamesVolumeService:
    # def __init__(
    #     self,
    #     activity_repo: ActivityRepo,
    #     game_repo: GameRepo,
    # ):
    #     self.activity_repo = activity_repo
    #     self.game_repo = game_repo

    async def get_documents(self, volume_documents):
        all_games_volume_dict = {}

        for volume_document in volume_documents:
            chart7d_volume = volume_document['chart7d_volume']
            for volume_timestamp in list(chart7d_volume.keys()):
                if volume_timestamp not in all_games_volume_dict:
                    all_games_volume_dict[volume_timestamp] = {
                        'timestamp': volume_timestamp,
                        'timestamp_ms': volume_timestamp*1000,
                        'volume': chart7d_volume[volume_timestamp]['volume']
                    }
                else:
                    all_games_volume_dict[volume_timestamp]['volume'] += chart7d_volume[volume_timestamp]['volume']

        return [values for values in all_games_volume_dict.values()]