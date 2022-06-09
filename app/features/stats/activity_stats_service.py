from app.utils.get_midnight_utc import get_midnight_utc
from db.activity_repo import ActivityRepo
from db.game_repo import GameRepo
from ekp_sdk.services import CacheService, CoingeckoService
from datetime import datetime
import copy


class ActivityStatsService:
    def __init__(
        self,
        activity_repo: ActivityRepo,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
        game_repo: GameRepo,
    ):
        self.activity_repo = activity_repo
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.game_repo = game_repo
        
  
    async def get_documents(self):
        games = self.game_repo.find_all()
        
        games_map = {}
        
        for game in games:
            if not game["disable"]:
                games_map[game["id"]] = game
            
        records = self.activity_repo.find_all()

        if not len(records):
            return []
        
        latest_date_timestamp = records[len(records) - 1]["timestamp"]

        chart7d_template = {}

        for i in range(7):
            chart_timestamp = latest_date_timestamp - 86400 * (6-i)
            chart7d_template[chart_timestamp] = {
                "timestamp": chart_timestamp,
                "timestamp_ms": chart_timestamp * 1000,
                "newUsers": 0,
            }

        grouped_by_game_id = {}
        
        now = datetime.now().timestamp()
        
        for record in records:
            game_id = record["game_id"]
            
            if game_id not in games_map:
                continue
            
            date_timestamp = record["timestamp"]
            ago = latest_date_timestamp - date_timestamp
            new_users = record["new_users"]

            if game_id not in grouped_by_game_id:
                grouped_by_game_id[game_id] = self.create_record(
                    game_id, 
                    record, 
                    games_map, 
                    now, 
                    chart7d_template
                )

            group = grouped_by_game_id[game_id]

            if ago < 86400:
                group["newUsers24h"] = group["newUsers24h"] + new_users
            elif ago < (2 * 86400):
                group["newUsers48h"] = group["newUsers48h"] + new_users
                
            if ago < (86400 * 7):
                group["newUsers7d"] = group["newUsers7d"] + new_users
                group["newUsers7dcount"] = group["newUsers7dcount"] + 1

            if group["newUsers48h"] > 0:
                group["newUsersDelta"] = (group["newUsers24h"] - group["newUsers48h"]) * 100 / group["newUsers48h"]

            if date_timestamp in group["chart7d"]:
                group["chart7d"][date_timestamp]["newUsers"] = new_users


        documents = list(
            filter(lambda x: x["newUsers7d"], grouped_by_game_id.values())
        )
        
        for document in documents:
            if not document["newUsers7d"] or not document["newUsers24h"]:
                continue
            
            avg7d = document["newUsers7d"] / document["newUsers7dcount"]
            
            document["newUsersDelta"] = (document["newUsers24h"]) * 100 / document["newUsers7d"]

        return list(
            filter(
                lambda x: x["newUsers7d"] > 100,
                documents,
            ),
        )
            

    def create_record(self, game_id, record, games_map, now, chart7d_template):
        gameLink = f"https://www.coingecko.com/en/coins/{game_id}"
        
        website = None
        twitter = None
        
        if game_id in games_map:
            game = games_map[game_id]
            website = game["website"]
            twitter = f'https://twitter.com/{game["twitter"]}'
        
        return {
            "gameId": game_id,
            "gameName": record["game_name"],
            "gameLink": gameLink,
            "chain": record["game_chain"],
            "newUsers24h": 0,
            "newUsers48h": 0,
            "newUsersDelta": None,
            "newUsers7d": 0,
            "newUsers7dcount": 0,
            "updated": now,
            "chart7d": copy.deepcopy(chart7d_template),
            "website": website,
            "twitter": twitter
        }        
        
