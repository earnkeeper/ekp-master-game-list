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

        totals = self.social_repo.find_latest_by_game_id()

        if not len(totals):
            return []

        all = self.social_repo.find_all_since(0)

        all_by_game_id = {}

        for record in all:
            game_id = record["game_id"]

            if game_id not in all_by_game_id:
                all_by_game_id[game_id] = []

            all_by_game_id[game_id].append(record)

        documents = []

        now = datetime.now().timestamp()

        for record in totals:
            game_id = record['_id']

            if game_id not in games_map:
                logging.warn(
                    f"Skipping game {game_id}, not found in games map")
                continue

            game = games_map[game_id]

            twitter_followers = record['twitter_followers']

            chains = self.get_chains(game)

            chart_records = all_by_game_id[game_id]
            
            chart_records.sort(key=lambda x: x['timestamp'])
            
            last_record = None
            
            chart = []
            
            for chart_record in chart_records:
                if "twitter_followers" not in chart_record:
                    continue
                
                if last_record is None:
                    last_record = chart_record
                    continue
                    
                chart.append({
                    "timestamp_ms": chart_record["timestamp"] * 1000,
                    "value": chart_record["twitter_followers"] - last_record["twitter_followers"]
                })
                
                last_record = chart_record

            document = {
                "id": game_id,
                "updated": now,
                "game_name": game['name'],
                "twitter_followers": twitter_followers,
                "chains": chains,
                "chart": chart
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
