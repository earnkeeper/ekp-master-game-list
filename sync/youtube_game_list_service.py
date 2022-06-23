import datetime

from dateutil.relativedelta import relativedelta
from db.game_repo import GameRepo
from db.youtube_repo import YoutubeRepo
from ekp_sdk.services import CacheService
from shared.get_midnight_utc import get_midnight_utc
from shared.youtube_api_service import YoutubeApiService
from youtubesearchpython import *


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

        today_timestamp = get_midnight_utc(datetime.datetime.now()).timestamp()

        game_ids_with_videos_today = self.youtube_repo.find_game_ids_with_videos_today(
            today_timestamp
        )

        for game in games:
            if game['id'] in game_ids_with_videos_today:
                continue
            
            if game['disable'] or not game['name']:
                continue

            search_query = game['name'] + " play to earn"

            if 'youtube_search_query' in game and game['youtube_search_query']:
                search_query = game['youtube_search_query']

            videos = await self.get_youtube_game_videos_info(search_query, today_timestamp, game)

            self.youtube_repo.save(videos)

        self.youtube_repo.delete_where_timestamp_before(today_timestamp)

    async def get_channel_subs_by_id(self, channel_id):
        channel_subs = None
        try:
            channel = Channel.get(channel_id)
            channel_subs = channel['subscribers']['simpleText'].replace(
                "subscribers", "")
        except Exception as e:
            pass
        return channel_subs if channel_subs else "0"

    async def get_youtube_game_videos_info(self, search_query, today_timestamp, game):
        videos_list = VideosSearch(search_query, limit=10).result()['result']

        videos = []

        for video in videos_list:
            if not video['publishedTime']:
                continue
            channel_subs = await self.cache_service.wrap(
                f"channelId_{video['channel']['id']}",
                lambda: self.get_channel_subs_by_id(video['channel']['id']),
                ex=3600
            )

            document = await self.get_single_video_info(video, search_query, channel_subs, today_timestamp, game)

            videos.append(document)

        return videos

    async def get_single_video_info(self, video, search_query, channel_subs, today_timestamp, game):

        view_count = None

        if "viewCount" in video and 'text' in video['viewCount']:
            view_count = video['viewCount']['text']

        return {
            "id": video['id'],
            "search_query": search_query,
            "game_id": game['id'],
            "date_timestamp": today_timestamp,
            "title": video['title'].replace('\n', ''),
            "video_description": video['descriptionSnippet'][0]['text'] if video['descriptionSnippet'] else None,
            "thumbnail": video['thumbnails'][0]['url'],
            "view_count": view_count,
            "duration": video['duration'],
            "publish_time": self.get_timestamp_of_publish_date(video['publishedTime']),
            "channel_name": video['channel']['name'],
            "subscribers_count": channel_subs,
            "link": video['link']
        }

    def get_timestamp_of_publish_date(self, pb_time):
        map_dict = {
            'minute ': 'minutes ',
            'hour ': 'hours ',
            'day ': 'days ',
            'month ': 'months ',
            'year ': 'years '
        }

        for key in map_dict.keys():
            pb_time = pb_time.replace(key, map_dict[key])

        parsed_s = [pb_time.split()[:2]]
        if 'Streamed' in pb_time:
            parsed_s = [pb_time.split()[1:3]]
        time_dict = dict((fmt, float(amount)) for amount, fmt in parsed_s)
        dt = relativedelta(**time_dict)
        past_time = datetime.datetime.now() - dt

        return int(past_time.timestamp())
