import logging
from app.utils.get_midnight_utc import get_midnight_utc
from db.activity_repo import ActivityRepo
from db.game_repo import GameRepo
from datetime import datetime
import copy

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

        game_records = self.social_repo.find_latest_by_game_id()

        daily_chart_records = self.social_repo.find_chart_by_game_id()

        grouped_by_day = {}

        for chart_record in daily_chart_records:
            game_id = chart_record["_id"]["game_id"]
            date_timestamp = str(chart_record["_id"]["date_timestamp"])

            if game_id not in grouped_by_day:
                grouped_by_day[game_id] = {}

            grouped_by_day[game_id][date_timestamp] = chart_record["value"]

        if not len(game_records):
            return []

        all = self.social_repo.find_all_since(1655056950)

        all_by_game_id = {}

        for record in all:
            game_id = record["game_id"]

            if game_id not in all_by_game_id:
                all_by_game_id[game_id] = []

            all_by_game_id[game_id].append(record)

        documents = []

        now = datetime.now().timestamp()

        for record in game_records:
            game_id = record['_id']

            if game_id not in games_map:
                logging.warn(
                    f"Skipping game {game_id}, not found in games map")
                continue

            game = games_map[game_id]

            twitter_followers = record['twitter_followers']

            chains = self.get_chains(game)

            chart_records = []
            if game_id in all_by_game_id:
                chart_records = all_by_game_id[game_id]

            chart_records.sort(key=lambda x: x['timestamp'])

            last_record = None

            chart = []

            for chart_record in chart_records:
                if "twitter_followers" not in chart_record or not chart_record["twitter_followers"]:
                    continue

                if last_record is None:
                    last_record = chart_record
                    continue

                chart.append({
                    "timestamp_ms": chart_record["timestamp"] * 1000,
                    "value": chart_record["twitter_followers"] - last_record["twitter_followers"]
                })

                last_record = chart_record

            game_daily_chart_records = []

            change_24h = None
            change_24h_pc = None

            if game_id in grouped_by_day:
                for key in grouped_by_day[game_id].keys():
                    game_daily_chart_records.append({
                        "date_timestamp": key,
                        "value": grouped_by_day[game_id][key]
                    })

            if len(game_daily_chart_records) > 1 and twitter_followers:
                game_daily_chart_records.sort(
                    key=lambda x: int(x['date_timestamp']))
                change_24h = game_daily_chart_records[len(
                    game_daily_chart_records) - 1]["value"] - game_daily_chart_records[len(game_daily_chart_records) - 2]["value"]
                change_24h_pc = round(change_24h * 100 / twitter_followers, 3)

            change_24h_color = "normal"
            
            twitter_plus = None
            
            if change_24h is not None:
                if change_24h > 0:
                    change_24h_color = "success"
                    twitter_plus = True

                if change_24h < 0:
                    change_24h_color = "danger"

            document = {
                "id": game_id,
                "updated": now,
                "game_name": game['name'],
                "twitter_followers": twitter_followers,
                "chains": chains,
                "chart": chart,
                "banner_url": game.get('banner_url', None),
                "profile_image_url": game.get('profile_image_url', None),
                "change_24h": change_24h,
                "change_24h_pc": change_24h_pc,
                "change_24h_color": change_24h_color,
                "twitter_plus": twitter_plus,
            }
            
            documents.append(document)

        return documents

    def get_chains(self, game):
        chains = []

        if "tokens" not in game:
            return chains

        tokens = game['tokens']

        chain_names = ['bsc', 'eth', 'polygon']

        for chain_name in chain_names:
            if chain_name in tokens and len(tokens[chain_name]) and tokens[chain_name][0]:
                chains.append(chain_name)

        return chains
