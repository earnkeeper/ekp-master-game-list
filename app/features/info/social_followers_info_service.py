from datetime import datetime
from app.utils.get_midnight_utc import get_midnight_utc
from db.social_repo import SocialRepo
from db.game_repo import GameRepo


class SocialFollowersInfoService:
    def __init__(
            self,
            game_repo: GameRepo,
            social_repo: SocialRepo,
    ):
        self.game_repo = game_repo
        self.social_repo = social_repo

    async def get_social_document(self, game):
        game_id = game['id']

        latest_record = self.social_repo.find_latest_for_game_id(game_id)

        if not latest_record:
            return None

        daily_chart_records = self.social_repo.find_chart_for_game_id(game_id)

        grouped_by_day = {}

        for chart_record in daily_chart_records:
            date_timestamp = str(chart_record["_id"])
            grouped_by_day[date_timestamp] = chart_record["value"]

        all = self.social_repo.find_all_since_for_game_id(1655056950, game_id)

        now = datetime.now().timestamp()

        twitter_followers = latest_record['twitter_followers']

        chart_records = all

        chart_records.sort(key=lambda x: x['timestamp'])

        last_record = None

        chart = []

        for chart_record in chart_records:
            if "twitter_followers" not in chart_record or not chart_record["twitter_followers"]:
                continue

            if last_record is None:
                last_record = chart_record
                continue

            chart.append({
                "timestamp_ms": chart_record["timestamp"] * 1000,
                "value": chart_record["twitter_followers"] - last_record["twitter_followers"]
            })

            last_record = chart_record

        game_daily_chart_records = []

        change_24h = None
        change_24h_pc = None

        for key in grouped_by_day.keys():
            game_daily_chart_records.append({
                "date_timestamp": key,
                "value": grouped_by_day[key]
            })

        if len(game_daily_chart_records) > 1 and twitter_followers:
            game_daily_chart_records.sort(
                key=lambda x: int(x['date_timestamp'])
            )
            
            today_value = game_daily_chart_records[
                len(game_daily_chart_records) - 1
            ]["value"]
            
            yesterday_value = game_daily_chart_records[
                len(game_daily_chart_records) - 2
            ]["value"]
            
            change_24h = today_value - yesterday_value

            change_24h_pc = round(change_24h * 100 / twitter_followers, 3)

        change_24h_color = "normal"

        twitter_plus = None

        if change_24h is not None:
            if change_24h > 0:
                change_24h_color = "success"
                twitter_plus = True

            if change_24h < 0:
                change_24h_color = "danger"

        document = {
            "id": game_id,
            "updated": now,
            "game_name": game['name'],
            "twitter_followers": twitter_followers,
            "chart": chart,
            "banner_url": game.get('banner_url', None),
            "change_24h": change_24h,
            "change_24h_pc": change_24h_pc,
            "change_24h_color": change_24h_color,
            "twitter_plus": twitter_plus,
        }
        
        return document


    def get_chains(self, game):
        chains = []

        if "tokens" not in game:
            return chains

        tokens = game['tokens']

        chain_names = ['bsc', 'eth', 'polygon']

        for chain_name in chain_names:
            if chain_name in tokens and len(tokens[chain_name]) and tokens[chain_name][0]:
                chains.append(chain_name)

        return chains
