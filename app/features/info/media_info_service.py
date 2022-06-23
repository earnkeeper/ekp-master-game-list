from pprint import pprint

from db.youtube_repo import YoutubeRepo


class MediaInfoService:
    def __init__(
            self,
            youtube_repo: YoutubeRepo
    ):
        self.youtube_repo = youtube_repo

    async def get_media_documents(self, game):
        game_id = game["id"]

        top_10_video_info = self.youtube_repo.find_videos_by_game_id(game_id)

        for video in top_10_video_info:
            if len(video["title"]) > 80:
                video["title"] = video["title"][:78] + "..."

        if not top_10_video_info:
            return None

        return top_10_video_info

