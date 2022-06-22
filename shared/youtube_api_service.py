from ekp_sdk.services import RestClient, Limiter


class YoutubeApiService:
    def __init__(
            self,
            api_key: str,
            rest_client: RestClient
    ):
        self.base_url = 'https://youtube.googleapis.com/youtube/v3'
        self.api_key = api_key
        self.rest_client = rest_client
        self.limiter = Limiter(250, 4)

    async def get_game_list_by_query(
            self,
            search_query,
            max_result=10,
            language='en',
            region='US'
    ):
        url = f"{self.base_url}/search?q={search_query}&maxResults={max_result}&relevanceLanguage={language}&regionCode={region}&type=video&key={self.api_key}"

        result = await self.__get(url, fn=lambda data, text, response: data['items'] if data else [])

        return result

    async def get_video_info(self, video_id):
        url = f"{self.base_url}/videos?part=statistics,contentDetails,snippet&id={video_id}&key={self.api_key}"

        result = await self.__get(url, fn=lambda data, text, response: data['items'][0] if data else [])

        return result

    async def get_videos_info(self, cs_video_ids_list):
        url = f"{self.base_url}/videos?part=statistics,contentDetails,snippet&id={cs_video_ids_list}&key={self.api_key}"

        result = await self.__get(url, fn=lambda data, text, response: data['items'] if data else [])

        return result

    async def get_channel_info(self, channel_id):
        url = f"{self.base_url}/channels?part=statistics&id={channel_id}&key={self.api_key}"

        result = await self.__get(url, fn=lambda data, text, response: data['items'][0] if data else [])

        return result

    async def get_channel_subs_count(self, channel_id):
        url = f"{self.base_url}/channels?part=statistics&id={channel_id}&key={self.api_key}"

        result = await self.__get(url, fn=lambda data, text, response: data['items'][0]['statistics'][
            'subscriberCount'] if 'subscriberCount' in data['items'][0]['statistics'] else 0)

        return result

    async def get_channels_info(self, cs_channel_ids_list):
        url = f"{self.base_url}/channels?part=statistics&id={cs_channel_ids_list}&key={self.api_key}"

        result = await self.__get(url, fn=lambda data, text, response: data['items'] if data else [])

        return result

    async def __get(self, url, fn=lambda data, text, response: data["items"], allowed_response_codes=[200]):
        # headers = {"X-API-Key": self.api_key}

        result = await self.rest_client.get(
            url,
            fn,
            limiter=self.limiter,
            allowed_response_codes=allowed_response_codes
        )

        return result
