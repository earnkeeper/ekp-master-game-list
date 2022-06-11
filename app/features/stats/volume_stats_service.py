from app.utils.get_midnight_utc import get_midnight_utc
from db.game_repo import GameRepo
from ekp_sdk.services import CacheService, CoingeckoService
from datetime import datetime
import copy

from db.volume_repo import VolumeRepo


class VolumeStatsService:
    def __init__(
        self,
        volume_repo: VolumeRepo,
        cache_service: CoingeckoService,
        coingecko_service: CoingeckoService,
        game_repo: GameRepo,
    ):
        self.volume_repo = volume_repo
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.game_repo = game_repo

    async def get_documents(self):
        games = self.game_repo.find_all()
        
        games_map = {}
        
        for game in games:
            games_map[game["id"]] = game
            
        records = self.volume_repo.find_all()

        if not len(records):
            return []
        
        latest_date_timestamp = records[len(records) - 1]["timestamp"]

        chart7d_template = {}

        for i in range(7):
            chart_timestamp = latest_date_timestamp - 86400 * (6-i)
            chart7d_template[chart_timestamp] = {
                "timestamp": chart_timestamp,
                "timestamp_ms": chart_timestamp * 1000,
                "volume": 0,
            }

        grouped_by_game_id = {}
        
        now = datetime.now().timestamp()
        
        for record in records:
            game_id = record["game_id"]
            date_timestamp = record["timestamp"]
            ago = latest_date_timestamp - date_timestamp
            volume = record["volume_usd"]
            
            if volume is None:
                volume = 0

            game_chain = record["game_chain"]
            
            if game_id not in grouped_by_game_id:
                grouped_by_game_id[game_id] = self.create_record(
                    game_id, 
                    record, 
                    games_map, 
                    now, 
                    chart7d_template
                )

            group = grouped_by_game_id[game_id]

            if game_chain not in group["chains"]:
                group["chains"].append(game_chain)
                
            if ago < 86400:
                group["volume24h"] = group["volume24h"] + volume
            elif ago < (2 * 86400):
                group["volume48h"] = group["volume48h"] + volume
                
            if ago < (86400 * 7):
                group["volume7d"] = group["volume7d"] + volume
                group["volume7dcount"] = group["volume7dcount"] + 1

            if group["volume48h"] > 0:
                group["volumeDelta"] = (group["volume24h"] - group["volume48h"]) * 100 / group["volume48h"]

            if date_timestamp in group["chart7d"]:
                group["chart7d"][date_timestamp]["volume"] = volume


        documents = list(
            filter(lambda x: x["volume7d"], grouped_by_game_id.values())
        )
        
        for document in documents:
            if not document["volumeDelta"]:
                continue

            if document["volumeDelta"] < 0:
                document["deltaColor"] = "danger"
            if document["volumeDelta"] > 0:
                document["deltaColor"] = "success"
                        
        return documents
            

    def create_record(self, game_id, record, games_map, now, chart7d_template):
        gameLink = f"https://www.coingecko.com/en/coins/{game_id}"
        
        website = None
        twitter = None
        discord = None
        telegram = None
        
        if game_id in games_map:
            game = games_map[game_id]
            website = game["website"]
            twitter = f'https://twitter.com/{game["twitter"]}'
            discord = game["discord"]
            telegram = game["telegram"]
        
        return {
            "gameId": game_id,
            "gameName": record["game_name"],
            "chains": [record["game_chain"]],
            "gameLink": gameLink,
            "chain": record["game_chain"],
            "volume24h": 0,
            "volume48h": 0,
            "volumeDelta": None,
            "volume7d": 0,
            "volume7dcount": 0,
            "updated": now,
            "chart7d": copy.deepcopy(chart7d_template),
            "website": website,
            "twitter": twitter,
            "discord": discord,
            "telegram": telegram,
        }        