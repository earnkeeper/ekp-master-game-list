from pprint import pprint

from db.resouces_repo import ResourcesRepo

class ResourcesInfoService:
    def __init__(
            self,
            resources_repo: ResourcesRepo
    ):
        self.resources_repo = resources_repo

    async def get_resources_documents(self, game):
        game_id = game["id"]

        game_resources = self.resources_repo.find_resources_by_game_id(game_id)

        if not game_resources:
            return None
        # pprint(game_resources)
        return game_resources

