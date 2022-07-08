from pprint import pprint

from shared.get_midnight_utc import get_midnight_utc
from app.utils.proxy_image import proxy_image
from db.activity_repo import ActivityRepo
from db.game_repo import GameRepo
from datetime import datetime
import copy


class ActivityStatsService:
    def __init__(
        self,
        activity_repo: ActivityRepo,
        game_repo: GameRepo,
    ):
        self.activity_repo = activity_repo
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

        today = get_midnight_utc(datetime.fromtimestamp(
            latest_date_timestamp)).timestamp()

        chart7d_template = {}

        for i in range(7):
            chart_timestamp = today - 86400 * (6-i)
            chart7d_template[chart_timestamp] = {
                "timestamp": chart_timestamp,
                "timestamp_ms": chart_timestamp * 1000,
                "newUsers": 0,
            }

        grouped_by_id = {}

        now = datetime.now()
        now_midnight = get_midnight_utc(now).timestamp()
        now = now.timestamp()
        now_seconds_into_day = now - now_midnight

        for record in records:
            game_id = record["game_id"]

            if game_id not in games_map:
                continue

            game_chain = record["game_chain"]

            date_timestamp = record["timestamp"]

            midnight = get_midnight_utc(
                datetime.fromtimestamp(date_timestamp)
            ).timestamp()

            ago = today - midnight

            new_users = record["new_users"]

            if midnight == now_midnight:
                new_users = int(new_users * 86400 / now_seconds_into_day)

            id = f"{game_id}"

            if id not in grouped_by_id:
                grouped_by_id[id] = self.create_record(
                    id,
                    record,
                    games_map,
                    now,
                    chart7d_template,
                )

            group = grouped_by_id[id]

            if game_chain not in group["chains"]:
                group["chains"].append(game_chain)

            if ago == 0:
                group["newUsers24h"] = group["newUsers24h"] + new_users
            elif ago == 86400:
                group["newUsers48h"] = group["newUsers48h"] + new_users

            if ago < (86400 * 6):
                group["newUsers7d"] += new_users
            elif ago < (86400 * 13):
                group["newUsers14d"] += new_users

            if group["newUsers14d"] > 0:
                group["newUsers7dDelta"] = (
                    group["newUsers7d"] - group["newUsers14d"]) * 100 / group["newUsers14d"]

            if group["newUsers48h"] > 0:
                group["newUsersDelta"] = (
                    group["newUsers24h"] - group["newUsers48h"]) * 100 / group["newUsers48h"]

            if midnight in group["chart7d"]:
                group["chart7d"][midnight]["newUsers"] += new_users

        documents = list(grouped_by_id.values())

        for document in documents:
            if not document["newUsersDelta"]:
                continue

            if document["newUsersDelta"] < 0:
                document["activity_deltaColor"] = "danger"
            if document["newUsersDelta"] > 0:
                document["activity_deltaColor"] = "success"

            if document["newUsers7dDelta"] < 0:
                document["activity_delta7dColor"] = "danger"
            if document["newUsers7dDelta"] > 0:
                document["activity_delta7dColor"] = "success"

        return documents


    def create_record(self, id, record, games_map, now, chart7d_template):
        gameLink = f"https://www.coingecko.com/en/coins/{id}"

        website = None
        twitter = None
        discord = None
        telegram = None
        profile_image_url = None
        name = record["game_name"]

        if id in games_map:
            game = games_map[id]
            name = game['name']
            website = game["website"]
            twitter = f'https://twitter.com/{game["twitter"]}'
            discord = game["discord"]
            telegram = game["telegram"]
            profile_image_url = game.get('profile_image_url', None)

        return {
            "id": id,
            "gameId": record["game_id"],
            "game_name": name,
            "gameLink": gameLink,
            "chains": [record["game_chain"]],
            "profile_image_url": proxy_image(profile_image_url),
            "newUsers24h": 0,
            "newUsers48h": 0,
            "newUsersDelta": None,
            "newUsers7d": 0,
            "newUsers14d": 0,
            "newUsers7dDelta": 0,
            "updated": now,
            "chart7d": copy.deepcopy(chart7d_template),
            "website": website,
            "twitter": twitter,
            "discord": discord,
            "telegram": telegram,
            "deltaColor": "normal"
        }
