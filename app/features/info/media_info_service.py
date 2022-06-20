from pprint import pprint

from db.youtube_repo import YoutubeRepo


class MediaInfoService:
    def __init__(
            self,
            youtube_repo: YoutubeRepo
    ):
        self.youtube_repo = youtube_repo

    async def get_media_documents(self, game):
        game_name = game["name"]

        top_10_video_info = self.youtube_repo.find_videos_by_game_name(game_name)

        # pprint(top_10_video_info)
        return top_10_video_info

