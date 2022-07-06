from datetime import datetime
from pprint import pprint

from db.social_repo import SocialRepo
from db.game_repo import GameRepo


class SocialFollowersInfoService:
    def __init__(
            self,
            game_repo: GameRepo,
            social_repo: SocialRepo,
    ):
        self.game_repo = game_repo
        self.social_repo = social_repo

    async def get_social_document(self, game):
        records = self.social_repo.group_by_date(game['id'])

        if not len(records):
            return None

        # pprint(records)

        records.sort(key=lambda record: record["_id"])

        now = datetime.now().timestamp()

        document = self.__create_document(game, now)

        last_record = None

        for record in records:
            if record["value"] is None:
                continue
                
            date_timestamp = record["_id"]

            document["twitter_followers"] = record["value"]

            if last_record is not None:
                document["change_24h"] = record["value"] - last_record["value"]

                if (last_record["value"]):
                    document["change_24h_pc"] = (
                        record["value"] - last_record["value"]) / last_record["value"]

                document["chart"].append({
                    "timestamp_ms": date_timestamp * 1000,
                    "value": document["change_24h"]
                })

                document["twitter_plus"] = False

                if document["change_24h"] > 0:
                    document["change_24h_color"] = "success"
                    document["twitter_plus"] = True
                if document["change_24h"] < 0:
                    document["change_24h_color"] = "danger"

            last_record = record

        return document


    def __create_document(self, game, now):
        document = {
            "id": game['id'],
            "updated": now,
            "game_name": game['name'],
            "twitter_followers": None,
            "chart": [],
            "banner_url": game.get('banner_url', None),
            "change_24h": 0,
            "change_24h_pc": 0,
            "change_24h_color": "normal",
            "twitter_plus": False,
        }

        return document

