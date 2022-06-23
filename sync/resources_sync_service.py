from ekp_sdk.services import GoogleSheetsClient
from db.game_repo import GameRepo
from db.resouces_repo import ResourcesRepo


class ResourcesSyncService:
    def __init__(
        self,
        google_sheets_client: GoogleSheetsClient,
        resources_repo: ResourcesRepo,
        sheet_id: str
    ):
        self.google_sheets_client = google_sheets_client
        self.resources_repo = resources_repo
        self.sheet_id = sheet_id

    async def sync_resources(self):
        rows = self.google_sheets_client.get_range(
            self.sheet_id,
            "resources!A2:E"
        )

        resources = []

        for row in rows:
            if len(row) < 1:
                continue

            game_id = row[0]
            rank = self.__get_value_from(row, 1)
            icon = self.__get_value_from(row, 2)
            title = self.__get_value_from(row, 3)
            link = self.__get_value_from(row, 4)

            # resource = {
            #     "game_id": game_id,
            #     "rank": rank,
            #     "icon": icon,
            #     "title": title,
            #     "link": link
            # }
            resources.append({
                "game_id": game_id,
                "rank": rank,
                "icon": icon,
                "title": title,
                "link": link,
            })

        self.resources_repo.save(resources)

        # return resources

    def __get_value_from(self, row, column_index):
        if len(row) <= column_index:
            return None

        return row[column_index]