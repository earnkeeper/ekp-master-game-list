from datetime import datetime
from pprint import pprint

from db.game_repo import GameRepo
from db.transaction_repo import TransactionRepo
from ekp_sdk.services.web3_service import Web3, Web3Service


class SharedGamesService:

    def __init__(
            self,
            transaction_repo: TransactionRepo,
            game_repo: GameRepo,
            web3: Web3,
            web3_service: Web3Service
    ):
        self.transaction_repo = transaction_repo
        self.game_repo = game_repo
        self.web3 = web3
        self.web3_service = web3_service

    def get_games(self, game_id):
        # game_id = 'gala'

        games = list(self.game_repo.collection.find())

        game_contracts = []

        for game in games:
            if game['id'] == game_id:
                game_contracts = game['tokens']['bsc']

        # print(game_contracts)
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
                if self.web3_service.w3.eth.get_code(self.web3.toChecksumAddress(player)) != b'':
                    continue
                filtered_players.append(player)

            # print('target_transactions')
            # pprint(target_transactions)
            # print('target_players')
            # pprint(target_players)
            # print('filtered_players')
            # pprint(filtered_players)

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


                # print('shared_transactions')
                #
                # pprint(shared_transactions)
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
                            # print(f"{record['count']} - {game['name']} - https://earnkeeper.io/i/{game['id']}")
                            # pprint(record)
                            # pprint(game)

                # return shared_games

        return shared_games