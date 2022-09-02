from datetime import datetime

from dateutil import parser
from shared.get_midnight_utc import get_midnight_utc


class VolumeAnalyticsService:
    def get_last_period_chart(self, days, volume_records, rate):
        results = self.__get_chart(days * 2, days, volume_records, rate)

        if results is None:
            return None

        while len(results) < (days - 1):
            results.insert(
                0,
                {
                    "timestamp_ms": 0,
                    "volume_usd": None
                }
            )

        return results

    def get_period_total(self, days, volume_records):
        total_usd = 0

        start = int(datetime.now().timestamp()) - days * 86400

        for record in volume_records:
            if record['timestamp'] < start:
                continue

            total_usd += record['volume_usd']

        return total_usd

    def get_period_chart(self, days, volume_records, rate):
        return self.__get_chart(days, 0, volume_records, rate)

    def __get_chart(self, start_days_ago, end_days_ago, volume_records, rate):

        start = int(datetime.now().timestamp()) - start_days_ago * 86400
        end = int(datetime.now().timestamp()) - end_days_ago * 86400

        if not len(volume_records):
            return None

        chart = []

        for record in volume_records:
            if record['timestamp'] < start or record['timestamp'] > end:
                continue

            chart_record = {}
            chart_record["timestamp_ms"] = record['timestamp'] * 1000
            chart_record["volume_usd"] = record["volume_usd"] * rate
            chart.append(chart_record)

        return chart
