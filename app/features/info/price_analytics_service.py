from datetime import datetime

from dateutil import parser
from shared.get_midnight_utc import get_midnight_utc


class PriceAnalyticsService:
    def get_last_period_chart(self, days, price_records, rate):
        results = self.__get_chart(days * 2, days, price_records, rate)

        if results is None:
            return None

        while len(results) < (days - 1):
            results.insert(
                0,
                {
                    "timestamp_ms": 0,
                    "price_usd": None,
                }
            )

        return results

    def get_period_chart(self, days, price_records, rate):
        return self.__get_chart(days, 0, price_records, rate)

    def __get_chart(self, start_days_ago, end_days_ago, price_records, rate):

        start = int(datetime.now().timestamp()) - start_days_ago * 86400
        end = int(datetime.now().timestamp()) - end_days_ago * 86400

        if not len(price_records):
            return None

        chart = []

        for record in price_records:
            if record['timestamp'] < start or record['timestamp'] > end:
                continue

            chart_record = {}
            chart_record["timestamp_ms"] = record['timestamp'] * 1000
            chart_record["price_usd"] = record["price_usd"] * rate
            chart.append(chart_record)

        return chart
