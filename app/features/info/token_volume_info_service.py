from ekp_sdk.services import CoingeckoService

from db.volume_repo import VolumeRepo
from datetime import datetime

class TokenVolumeInfoService:
    def __init__(
        self,
        volume_repo: VolumeRepo,
    ):
        self.volume_repo = volume_repo

    async def get_volume_document(self, game, rate):

        records = self.volume_repo.find_by_game_id(game["id"])

        now = datetime.now().timestamp()
        
        if not len(records):
            return None
        
        latest_date_timestamp = records[len(records) - 1]["timestamp"]

        document = self.__create_record(game, now, latest_date_timestamp)

        for record in records:
            date_timestamp = record["timestamp"]
            ago = latest_date_timestamp - date_timestamp
            volume = record["volume_usd"]
            
            if volume is None:
                volume = 0

            if ago < 86400:
                document["volume24h"] = (document["volume24h"] + volume) * rate
            elif ago < (2 * 86400):
                document["volume48h"] = (document["volume48h"] + volume) * rate
                
            if ago < (86400 * 7):
                document["volume7d"] = (document["volume7d"] + volume) * rate
                document["volume7dcount"] = document["volume7dcount"] + 1

            if document["volume48h"] > 0:
                document["volumeDelta"] = (document["volume24h"] - document["volume48h"]) * 100 / document["volume48h"]

            if date_timestamp in document["chart7d"]:
                document["chart7d"][date_timestamp]["volume"] = volume * rate

        if document["volume7d"] and document["volume24h"]:
            document["volumeDelta"] = (document["volume24h"]) * 100 / document["volume7d"]

        document["deltaColor"] = "normal"

        if document["volumeDelta"] < 0:
            document["deltaColor"] = "danger"
        if document["volumeDelta"] > 0:
            document["deltaColor"] = "success"
            

        return document
            

    def __create_record(self, game, now, latest_date_timestamp):
        
        chart7d_template = {}

        for i in range(7):
            chart_timestamp = latest_date_timestamp - 86400 * (6-i)
            chart7d_template[chart_timestamp] = {
                "timestamp": chart_timestamp,
                "timestamp_ms": chart_timestamp * 1000,
                "volume": 0,
            }        
            
        return {
            "gameId": game["id"],
            "gameName": game["name"],
            "volume24h": 0,
            "volume48h": 0,
            "volumeDelta": 0,
            "volume7d": 0,
            "volume7dcount": 0,
            "updated": now,
            "chart7d": chart7d_template,
        }        
        