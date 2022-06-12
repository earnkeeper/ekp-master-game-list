from ekp_sdk.services import GoogleSheetsClient
from db.game_repo import GameRepo


class ManualSyncService:
    def __init__(
        self,
        google_sheets_client: GoogleSheetsClient,
        sheet_id: str
    ):
        self.google_sheets_client = google_sheets_client
        self.sheet_id = sheet_id

    def get_games(self):
        rows = self.google_sheets_client.get_range(
            self.sheet_id,
            "manual!A2:J"
        )

        games = []

        for row in rows:
            if len(row) < 1:
                continue

            game_id = row[0]
            game_name = self.__get_value_from(row, 1)
            coin_ids = row[2] if len(row) > 2 else None
            disable = len(row) > 3 and row[3] == "y"
            bsc_tokens = self.__get_tokens_from(row, 4)
            eth_tokens = self.__get_tokens_from(row, 5)
            polygon_tokens = self.__get_tokens_from(row, 6)

            if not coin_ids:
                coin_ids = [game_id]
            else:
                coin_ids = self.__split_new_lines(coin_ids)

            twitter = self.__get_value_from(row, 6)
            telegram = self.__get_value_from(row, 7)
            website = self.__get_value_from(row, 8)
            discord = self.__get_value_from(row, 9)

            games.append({
                "id": game_id,
                "disable": disable,
                "name": game_name,
                "coin_ids": coin_ids,
                "tokens": {
                    "bsc": bsc_tokens,
                    "eth": eth_tokens,
                    "polygon": polygon_tokens,
                },
                "twitter": twitter,
                "telegram": telegram,
                "website": website,
                "discord": discord,
            })

        return games

    def __get_value_from(self, row, column_index):
        if len(row) <= column_index:
            return None

        return row[column_index]

    def __get_tokens_from(self, row, column_index):

        if len(row) <= column_index:
            return []

        cell = row[column_index]

        return self.__split_new_lines(cell)

    def __split_new_lines(self, cell):
        return list(
            filter(
                lambda x: x,
                map(
                    lambda x: x.strip("\r").strip(" "),
                    cell.split("\n")
                ),
            )
        )
