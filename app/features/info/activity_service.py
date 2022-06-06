from datetime import datetime
from db.activity_repo import ActivityRepo
from db.game_repo import GameRepo


class ActivityService:
    def __init__(
        self,
        activity_repo: ActivityRepo,
    ):
        self.activity_repo = activity_repo

    async def get_activity_document(self, game):

        records = self.activity_repo.find_by_game_id(game["id"])

        if not len(records):
            return {
                "gameId": game["id"],
                "gameName": game["name"],
                "newUsers24h": 0,
                "newUsers48h": 0,
                "newUsersDelta": None,
                "newUsers7d": 0,
                "newUsers7dcount": 0,
                "updated": now,
                "chart7d": {},
            }

        latest_date_timestamp = records[len(records) - 1]["timestamp"]

        now = datetime.now().timestamp()

        document = self.__create_record(game, now, latest_date_timestamp)

        for record in records:
            date_timestamp = record["timestamp"]
            ago = latest_date_timestamp - date_timestamp
            new_users = record["new_users"]

            if ago < 86400:
                document["newUsers24h"] = document["newUsers24h"] + new_users
            elif ago < (2 * 86400):
                document["newUsers48h"] = document["newUsers48h"] + new_users

            if ago < (86400 * 7):
                document["newUsers7d"] = document["newUsers7d"] + new_users
                document["newUsers7dcount"] = document["newUsers7dcount"] + 1

            if document["newUsers48h"] > 0:
                document["newUsersDelta"] = (
                    document["newUsers24h"] - document["newUsers48h"]) * 100 / document["newUsers48h"]

            if date_timestamp in document["chart7d"]:
                document["chart7d"][date_timestamp]["newUsers"] = new_users

        if document["newUsers7d"] and document["newUsers24h"]:
            document["newUsersDelta"] = (
                document["newUsers24h"]) * 100 / document["newUsers7d"]

        document["deltaColor"] = "normal"

        if document["newUsersDelta"] < 0:
            document["deltaColor"] = "danger"
        if document["newUsersDelta"] > 0:
            document["deltaColor"] = "success"
            
        return document

    def __create_record(self, game, now, latest_date_timestamp):

        chart7d_template = {}

        for i in range(7):
            chart_timestamp = latest_date_timestamp - 86400 * (6-i)
            chart7d_template[chart_timestamp] = {
                "timestamp": chart_timestamp,
                "timestamp_ms": chart_timestamp * 1000,
                "newUsers": 0,
            }

        return {
            "gameId": game["id"],
            "gameName": game["name"],
            "newUsers24h": 0,
            "newUsers48h": 0,
            "newUsersDelta": 0,
            "newUsers7d": 0,
            "newUsers7dcount": 0,
            "updated": now,
            "chart7d": chart7d_template,
        }
