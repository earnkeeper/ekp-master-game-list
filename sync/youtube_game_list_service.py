import logging
from db.game_repo import GameRepo
from db.youtube_repo import YoutubeRepo
from youtubesearchpython import VideosSearch, Channel


class YoutubeSyncService:
    def __init__(
            self,
            game_repo: GameRepo,
            youtube_repo: YoutubeRepo,
    ):
        self.game_repo = game_repo
        self.youtube_repo = youtube_repo

    async def sync_youtube_games_info(self):
        self.youtube_repo.delete_records()

        games = self.game_repo.find_all()

        for game in games:
            game_name = game['name']
            videos = await self.get_youtube_game_videos_info(game_name=game_name)

            self.youtube_repo.save(videos)

    async def get_youtube_game_videos_info(self, game_name):
        videos_list = VideosSearch(game_name, limit=10).result()['result']
        videos = []
        for video in videos_list:
            channel = None
            try:
                channel = Channel.get(video['channel']['id'])
            except Exception as e:
                print(video['channel']['name'])
                print(video['channel']['id'])
                print(e)
                pass
            document = await self.get_single_video_info(video, game_name, channel)
            videos.append(document)

        return videos

    async def get_single_video_info(self, video, game_name, channel):
        return {
            "id": video['id'],
            "game_name": game_name,
            "title": video['title'].replace('\n', ''),
            "video_description": video['descriptionSnippet'][0]['text'] if video['descriptionSnippet'] else None,
            "thumbnail": video['thumbnails'][0]['url'],
            "view_count": video['viewCount']['text'],
            "duration": video['duration'],
            "publish_time": video['publishedTime'],
            "channel_name": video['channel']['name'],
            "subscribers_count": channel['subscribers']['simpleText'].replace("subscribers", "subs") if channel else None,
            "link": video['link']

        }
