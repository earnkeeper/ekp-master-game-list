from ekp_sdk.services import GoogleSheetsClient
from db.game_repo import GameRepo

class SheetsConfigService:
    def __init__(
        self,
        google_sheets_client: GoogleSheetsClient,
        game_repo: GameRepo,
        sheet_id: str
    ):
        self.google_sheets_client = google_sheets_client
        self.game_repo = game_repo
        self.sheet_id = sheet_id

    async def sync_games(self):
        rows = self.google_sheets_client.get_range(
            self.sheet_id, 
            "manual!A2:J"
        )

        new_games = []

        for row in rows:
            if len(row) < 3:
                continue

            
            disable = row[2] == "y"
            bsc_tokens = self.get_tokens_from(row, 3)
            eth_tokens = self.get_tokens_from(row, 4)
            polygon_tokens = self.get_tokens_from(row, 5)

            twitter = self.get_value_from(row, 6)
            telegram = self.get_value_from(row, 7)
            website = self.get_value_from(row, 8)
            discord = self.get_value_from(row, 9)

            new_games.append({
                "id": row[0],
                "disable": disable,
                "name": row[1],
                "source": "manual",
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

        existing_games = self.game_repo.find_by_source("manual")

        for existing_game in existing_games:
            existing_has_been_removed = True
            
            for new_game in new_games:
                if new_game["id"] == existing_game["id"]:
                    existing_has_been_removed = False
                    
            if existing_has_been_removed:
                self.game_repo.delete_by_id(existing_game["id"])
        
        self.game_repo.save(new_games)
        

    def get_value_from(self, row, column_index):
        if len(row) <= column_index:
            return None

        return row[column_index]

    def get_tokens_from(self, row, column_index):

        if len(row) <= column_index:
            return []

        cell = row[column_index]

        addresses = []

        for address in cell.split("\n"):
            addresses.append(address.strip("\r").strip(" "))

        return addresses
