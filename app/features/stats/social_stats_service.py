
from datetime import datetime
from app.utils.get_chains import get_chains

from db.game_repo import GameRepo
from db.social_repo import SocialRepo

class SocialStatsService:
    def __init__(
        self,
        social_repo: SocialRepo,
        game_repo: GameRepo,
    ):
        self.social_repo = social_repo
        self.game_repo = game_repo

    async def get_documents(self):
        games = self.game_repo.find_all()

        games_map = {}

        for game in games:
            if not game["disable"]:
                games_map[game["id"]] = game

        records = self.social_repo.group_by_game_id_and_date()

        records.sort(key=lambda record: record["_id"]["date_timestamp"])

        now = datetime.now().timestamp()

        documents_map = {}

        last_records = {}

        for record in records:
            if record["value"] is None:
                continue
                
            game_id = record["_id"]["game_id"]

            if game_id not in games_map:
                continue

            game = games_map[game_id]

            date_timestamp = record["_id"]["date_timestamp"]

            if game_id not in documents_map:
                documents_map[game_id] = self.__create_document(
                    game,
                    now
                )

            document = documents_map[game_id]

            document["twitter_followers"] = record["value"]

            if game_id in last_records:
                last_record = last_records[game_id]
                                
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

            last_records[game_id] = record

        return list(documents_map.values())

    def __create_document(self, game, now):
        chains = get_chains(game)

        document = {
            "id": game['id'],
            "updated": now,
            "game_name": game['name'],
            "twitter_followers": 0,
            "chains": chains,
            "chart": [],
            "banner_url": game.get('banner_url', None),
            "profile_image_url": game.get('profile_image_url', None),
            "change_24h": 0,
            "change_24h_pc": 0,
            "change_24h_color": "normal",
            "twitter_plus": False,
        }

        return document

