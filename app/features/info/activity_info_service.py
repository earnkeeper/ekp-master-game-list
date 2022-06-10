from datetime import datetime
from app.utils.get_midnight_utc import get_midnight_utc
from db.activity_repo import ActivityRepo


class ActivityInfoService:
    def __init__(
        self,
        activity_repo: ActivityRepo,
    ):
        self.activity_repo = activity_repo

    async def get_activity_document(self, game):

        records = self.activity_repo.find_by_game_id(game["id"])

        if not len(records):
            return None

        now = datetime.now()
        now_midnight = get_midnight_utc(now).timestamp()
        now = now.timestamp()
        now_seconds_into_day = now - now_midnight

        latest_date_timestamp = records[len(records) - 1]["timestamp"]
        today = get_midnight_utc(
            datetime.fromtimestamp(latest_date_timestamp)
        ).timestamp()

        document = self.__create_record(game, now, today)
        
        for record in records:
            date_timestamp = record["timestamp"]

            midnight = get_midnight_utc(
                datetime.fromtimestamp(date_timestamp)
            ).timestamp()

            ago = today - midnight

            new_users = record["new_users"]

            if midnight == now_midnight:
                new_users = int(new_users * 86400 / now_seconds_into_day)

            if ago == 0:
                document["newUsers24h"] = document["newUsers24h"] + new_users
            elif ago == 86400:
                document["newUsers48h"] = document["newUsers48h"] + new_users

            if ago < (86400 * 6):
                document["newUsers7d"] += new_users
            elif ago < (86400 * 13):
                document["newUsers14d"] += new_users

            if document["newUsers48h"] > 0:
                document["newUsersDelta"] = (
                    document["newUsers24h"] - document["newUsers48h"]) * 100 / document["newUsers48h"]

            if document["newUsers14d"] > 0:
                document["newUsers7dDelta"] = (
                    document["newUsers7d"] - document["newUsers14d"]) * 100 / document["newUsers14d"]

            if midnight in document["chart7d"]:
                document["chart7d"][midnight]["newUsers"] += new_users

        if document["newUsersDelta"] < 0:
            document["deltaColor"] = "danger"
        if document["newUsersDelta"] > 0:
            document["deltaColor"] = "success"

        if document["newUsers7dDelta"] < 0:
            document["delta7dColor"] = "danger"
        if document["newUsers7dDelta"] > 0:
            document["delta7dColor"] = "success"

        return document

    def __create_record(self, game, now, today):

        chart7d_template = {}

        for i in range(7):
            chart_timestamp = today - 86400 * (6-i)
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
            "newUsers14d": 0,
            "newUsers7dDelta": 0,
            "updated": now,
            "chart7d": chart7d_template,
            "deltaColor": "normal",
            "delta7dColor": "normal",
        }
