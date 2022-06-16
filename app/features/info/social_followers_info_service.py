from datetime import datetime
from app.utils.get_midnight_utc import get_midnight_utc
from db.social_repo import SocialRepo


class SocialFollowersInfoService:
    def __init__(
            self,
            social_repo: SocialRepo,
    ):
        self.social_repo = social_repo

    async def get_social_info_document(self, game):

        records = self.social_repo.find_by_game_id(game["id"])

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

            twitter_followers = record["twitter_followers"]

            if midnight == now_midnight:
                twitter_followers = int(twitter_followers * 86400 / now_seconds_into_day)

            if ago == 0:
                document["twitter_followers24h"] = document["twitter_followers24h"] + twitter_followers
            elif ago == 86400:
                document["twitter_followers48h"] = document["twitter_followers48h"] + twitter_followers

            if ago < (86400 * 6):
                document["twitter_followers7d"] += twitter_followers
            elif ago < (86400 * 13):
                document["twitter_followers14d"] += twitter_followers

            if document["twitter_followers48h"] > 0:
                document["twitter_followersDelta"] = (
                                                    document["twitter_followers24h"] - document["twitter_followers48h"]) * 100 / document[
                                                "twitter_followers48h"]

            if document["twitter_followers14d"] > 0:
                document["twitter_followers7dDelta"] = (
                                                      document["twitter_followers7d"] - document["twitter_followers14d"]) * 100 / \
                                              document["twitter_followers14d"]

            if midnight in document["chart7d"]:
                document["chart7d"][midnight]["twitterFollowers"] += twitter_followers

        if document["twitter_followersDelta"] < 0:
            document["deltaColor"] = "danger"
        if document["twitter_followersDelta"] > 0:
            document["deltaColor"] = "success"

        if document["twitter_followers7dDelta"] < 0:
            document["delta7dColor"] = "danger"
        if document["twitter_followers7dDelta"] > 0:
            document["delta7dColor"] = "success"

        return document

    def __create_record(self, game, now, today):

        chart7d_template = {}

        for i in range(7):
            chart_timestamp = today - 86400 * (6 - i)
            chart7d_template[chart_timestamp] = {
                "timestamp": chart_timestamp,
                "timestamp_ms": chart_timestamp * 1000,
                "twitterFollowers": 0,
            }

        return {
            "gameId": game["id"],
            "gameName": game["name"],
            "twitter_followers24h": 0,
            "twitter_followers48h": 0,
            "twitter_followersDelta": 0,
            "twitter_followers7d": 0,
            "twitter_followers14d": 0,
            "twitter_followers7dDelta": 0,
            "updated": now,
            "chart7d": chart7d_template,
            "deltaColor": "normal",
            "delta7dColor": "normal",
        }
