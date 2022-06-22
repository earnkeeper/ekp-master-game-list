import datetime
import logging

from ekp_sdk.services import CacheService

from app.utils.get_midnight_utc import get_midnight_utc
from db.game_repo import GameRepo
from db.youtube_repo import YoutubeRepo
from youtubesearchpython import VideosSearch, Channel


class YoutubeSyncService:
    def __init__(
            self,
            cache_service: CacheService,
            game_repo: GameRepo,
            youtube_repo: YoutubeRepo,
    ):
        self.cache_service = cache_service
        self.game_repo = game_repo
        self.youtube_repo = youtube_repo

    async def sync_youtube_games_info(self):
        self.youtube_repo.delete_records()

        games = self.game_repo.find_all()

        today_timestamp = get_midnight_utc(datetime.datetime.now()).timestamp()

        game_ids_with_videos_today = self.youtube_repo.find_game_ids_with_videos_today(today_timestamp)

        for game in games:

            if game['id'] in game_ids_with_videos_today:
                continue

            search_query = game['name']
            if 'youtube_search_query' in game and game['youtube_search_query']:
                search_query = game['youtube_search_query']

            videos = await self.get_youtube_game_videos_info(game_name=search_query, today_timestamp=today_timestamp)

            self.youtube_repo.save(videos)

        self.youtube_repo.delete_where_timestamp_before(today_timestamp)

    async def get_channel_subs_by_id(self, channel_id):
        channel_subs = None
        try:
            channel = Channel.get(channel_id)
            channel_subs = channel['subscribers']['simpleText'].replace("subscribers", "")
        except Exception as e:
            pass
        return channel_subs if channel_subs else "0"

    async def get_youtube_game_videos_info(self, game_name, today_timestamp):
        videos_list = VideosSearch(game_name, limit=10).result()['result']
        videos = []
        for video in videos_list:
            channel_subs = await self.cache_service.wrap(
                f"channelId_{video['channel']['id']}",
                lambda: self.get_channel_subs_by_id(video['channel']['id']),
                ex=3600
            )

            document = await self.get_single_video_info(video, game_name, channel_subs, today_timestamp)
            videos.append(document)

        return videos

    async def get_single_video_info(self, video, game_name, channel_subs, today_timestamp):

        view_count = None

        if "viewCount" in video and 'text' in video['viewCount']:
            view_count = video['viewCount']['text']

        return {
            "id": video['id'],
            "game_name": game_name,
            "game_id": video['id'],
            "date_timestamp": today_timestamp,
            "title": video['title'].replace('\n', ''),
            "video_description": video['descriptionSnippet'][0]['text'] if video['descriptionSnippet'] else None,
            "thumbnail": video['thumbnails'][0]['url'],
            "view_count": view_count,
            "duration": video['duration'],
            "publish_time": video['publishedTime'],
            "channel_name": video['channel']['name'],
            "subscribers_count": channel_subs,
            "link": video['link']

        }
