import logging
from db.game_repo import GameRepo
from db.youtube_repo import YoutubeRepo
from youtubesearchpython import *


class YoutubeSyncService:
    def __init__(
            self,
            game_repo: GameRepo,
            youtube_repo: YoutubeRepo,
    ):
        self.game_repo = game_repo
        self.youtube_repo = youtube_repo

    async def sync_youtube_games_info(self):
        games = self.game_repo.find_all()

        for game in games:
            game_name = game['name']
            videos = await self.get_youtube_game_videos_info(game_name=game_name)

            self.youtube_repo.save(videos)

    async def get_youtube_game_videos_info(self, game_name):
        videos_list = VideosSearch(game_name, limit=10).result()['result']
        videos = []
        for video in videos_list:
            document = await self.get_single_video_info(video, game_name)
            videos.append(document)

        return videos

    async def get_single_video_info(self, video, game_name):
        return {
            "id": video['id'],
            "game_name": game_name,
            "title": video['accessibility']['title'],
            "video_description": video['descriptionSnippet'][0]['text'] if video['descriptionSnippet'] else None,
            "thumbnail": video['thumbnails'][0]['url'],
            "view_count": video['viewCount']['text'],
            "duration": video['duration'],
            "publish_time": video['publishedTime'],
            "link": video['link']

        }
