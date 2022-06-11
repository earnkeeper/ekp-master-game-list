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

        records = self.social_repo.find_latest_by_game_id()

        if not len(records):
            return []

        documents = []

        now = datetime.now().timestamp()

        for record in records:
            game_id = record['_id']
            
            if game_id not in games_map:
                logging.warn(f"Skipping game {game_id}, not found in games map")
                continue
            
            game = games_map[game_id]
            
            twitter_followers = record['twitter_followers']
            
            chains = self.get_chains(game)
            
            document = {
                "id": game_id,
                "updated": now,
                "game_name": game['name'],
                "twitter_followers": twitter_followers,
                "chains": chains
            }
            
            documents.append(document)

        return documents

    def get_chains(self, game):
        chains = []
        
        if game["name"] == "Nine Chronicles":
            print(game)
            
        if "tokens" not in game:
            return chains
        
        tokens = game['tokens']
        
        chain_names = ['bsc', 'eth', 'polygon']
        
        for chain_name in chain_names:
            if chain_name in tokens and len(tokens[chain_name]) and tokens[chain_name][0]:
                chains.append(chain_name)

        return chains
        
        