from db.game_repo import GameRepo
from db.shared_games_repo import SharedGamesRepo
from db.transaction_repo import TransactionRepo
from datetime import datetime
from shared.get_midnight_utc import get_midnight_utc



class SharedGamesSyncService:
    def __init__(
            self,
            transaction_repo: TransactionRepo,
            game_repo: GameRepo,
            shared_games_repo: SharedGamesRepo
    ):
        self.transaction_repo = transaction_repo
        self.game_repo = game_repo
        self.shared_games_repo = shared_games_repo

    async def sync_shared_games(self):

        games = self.game_repo.find_all()

        today_timestamp = get_midnight_utc(datetime.now()).timestamp()

        game_ids_with_shared_games_today = self.shared_games_repo.find_game_ids_with_shared_games_today(
            today_timestamp
        )

        for game in games:

            if game['id'] in game_ids_with_shared_games_today:
                continue

            game_contracts = []

            if not game['tokens']['bsc']:
                continue
            else:
                game_contracts = game['tokens']['bsc']

            shared_games = []

            count = 0

            if len(game_contracts):

                since = datetime.now().timestamp() - 86400 * 7

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

                    # print(f'Game_id: {game["id"]}')

                    for record in shared_transactions:
                        if record['_id'] in game_contracts:
                            continue

                        for g in games:
                            # print(f'count before {count}')
                            if count == 10:
                                continue
                            # print(f'count before {count}')
                            if record["_id"] in g["tokens"]["bsc"]:
                                shared_games.append(
                                    {
                                        "game_id": game["id"],
                                        "shared_game_id": g["id"],
                                        "game": g["name"],
                                        "date_timestamp": today_timestamp,
                                        "banner_url": g["banner_url"] if "banner_url" in g else None,
                                        "players": record["count"]
                                    }
                                )
                                count += 1
                            # print(f'count after {count}')
                                # print(f"{record['count']} - {g['name']} - https://earnkeeper.io/i/{g['id']}")

            self.shared_games_repo.save(shared_games)

        self.shared_games_repo.delete_where_timestamp_before(today_timestamp)