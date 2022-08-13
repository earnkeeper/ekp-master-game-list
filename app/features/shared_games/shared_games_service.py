from datetime import datetime
from db.game_repo import GameRepo
from db.transaction_repo import TransactionRepo


class SharedGamesService:

    def __init__(
            self,
            transaction_repo: TransactionRepo,
            game_repo: GameRepo,
    ):
        self.transaction_repo = transaction_repo
        self.game_repo = game_repo

    def get_games(self, game_id):
        games = list(self.game_repo.collection.find())

        game_contracts = []

        for game in games:
            if game['id'] == game_id:
                game_contracts = game['tokens']['bsc']

        shared_games = []

        if len(game_contracts):

            since = datetime.now().timestamp() - 86400 * 9

            target_transactions = list(self.transaction_repo.collection.find(
                {
                    "to": {"$in": game_contracts},
                    "timestamp": {"$gt": since}
                }
            ))

            target_players = list(
                map(
                    lambda record: record["from"],
                    target_transactions
                )
            )

            filtered_players = []

            for player in target_players:
                if player in filtered_players:
                    continue
                filtered_players.append(player)

            if len(filtered_players):
                shared_transactions = list(self.transaction_repo.collection.aggregate(
                    [
                        {
                            "$match": {
                                "from": {"$in": target_players},
                                "timestamp": {"$gt": since},
                            }
                        },
                        {
                            "$group": {
                                "_id": "$to",
                                "count": {"$sum": 1}
                            }
                        },
                        {
                            "$sort": {
                                "count": -1
                            }
                        }
                    ]
                ))

                for record in shared_transactions:
                    if record['_id'] in game_contracts:
                        continue
                    for game in games:
                        if record["_id"] in game["tokens"]["bsc"]:
                            shared_games.append(
                                {
                                    "game_id": game["id"],
                                    "game": game["name"],
                                    "banner_url": game["banner_url"],
                                    "players": record["count"]
                                }
                            )

        return shared_games
