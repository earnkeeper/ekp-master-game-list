import logging
import datetime
import time
from pprint import pprint

import isodate
from ekp_sdk.services import CacheService
from app.utils.get_midnight_utc import get_midnight_utc

from db.game_repo import GameRepo
from db.youtube_repo import YoutubeRepo

from shared.youtube_api_service import YoutubeApiService


class YoutubeSyncService:
    def __init__(
            self,
            cache_service: CacheService,
            game_repo: GameRepo,
            youtube_repo: YoutubeRepo,
            youtube_api_service: YoutubeApiService
    ):
        self.cache_service = cache_service
        self.game_repo = game_repo
        self.youtube_repo = youtube_repo
        self.youtube_api_service = youtube_api_service

    async def sync_youtube_games_info(self):
        
        games = self.game_repo.find_all()
        
        today_timestamp = get_midnight_utc(datetime.now()).timestamp()

        game_ids_with_videos_today = self.youtube_repo.find_game_ids_with_videos_today(today_timestamp)

        for game in games:
            if game['id'] in game_ids_with_videos_today:
                continue
            
            search_query = game['name']
            
            if 'youtube_search_query' in game and game['youtube_search_query']:
                search_query = game['youtube_search_query']

            videos_id_list = await self.youtube_api_service.get_game_list_by_query(
                search_query=search_query
            )

            videos = await self.get_youtube_game_videos_info(videos_id_list, game, today_timestamp, search_query)

            self.youtube_repo.save(videos)
            
        self.youtube_repo.delete_where_timestamp_before(today_timestamp)

    async def get_youtube_game_videos_info(self, videos_id_list, game, today_timestamp, search_query):
        video_ids = []
        videos = []
        
        for video_id in videos_id_list:
            video_ids.append(video_id['id']['videoId'])

        video_ids_str = ','.join(video_ids)
        videos_info = await self.youtube_api_service.get_videos_info(video_ids_str)

        for video in videos_info:
            document = await self.get_single_video_info(video, game, today_timestamp, search_query)
            videos.append(document)

        return videos


    async def get_single_video_info(self, video, game, today_timestamp, search_query):
        channel_subs = await self.cache_service.wrap(
            f"channelId_{video['snippet']['channelId']}",
            lambda: self.youtube_api_service.get_channel_subs_count(video['snippet']['channelId']),
            ex=3600
        )
        
        view_count = None
        
        if "statistics" in video and "viewCount" in video["statistics"]:
            view_count = video['statistics']['viewCount']
            
        return {
            "id": video['id'],
            "search_query": search_query,
            "game_id": game['id'],
            "date_timestamp": today_timestamp,
            "title": video['snippet']['title'],
            "video_description": video['snippet']['description'] if video['snippet']['description'] else None,
            "thumbnail": video['snippet']['thumbnails']['medium']['url'],
            "view_count": view_count,
            "duration": str(datetime.timedelta(seconds=isodate.parse_duration('PT12M23S').total_seconds())),
            "publish_time": int(time.mktime(datetime.datetime.strptime(video['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").timetuple())),
            "channel_name": video['snippet']['channelTitle'],
            "subscribers_count": channel_subs,
            "link": f"https://www.youtube.com/watch?v={video['id']}"
        }