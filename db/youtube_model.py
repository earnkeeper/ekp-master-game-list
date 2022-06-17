from typing import TypedDict


class YoutubeGamesModel(TypedDict):
    id: str
    title: str
    game_name: str
    video_description: str
    thumbnail: str
    view_count: str
    duration: str
    publish_time: str
    link: str