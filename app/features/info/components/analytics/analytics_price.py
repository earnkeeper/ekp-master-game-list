from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Hr, Icon, Image, Link, Paragraphs, Row, Span,
                        Tabs, commify, ekp_map, format_currency, sum, Tab,
                        format_mask_address, format_percent, format_template,
                        is_busy, json_array, navigate, sort_by, navigate_back, format_age, Avatar, Form, Select)

def analytics_price(CHART_NAME):
    return Card(
        children=[
            Div(
                context="$.analytics_price",
                when="$",
                class_name="mx-1 my-2",
                style={
                    "marginRight": "-10px",
                    "marginLeft": "-22px",
                    "marginBottom": "-14px",
                    "marginTop": "-20px"
                },
                children=[
                    Chart(
                        title="",
                        name=CHART_NAME,
                        height=350,
                        type="line",
                        data="$.price_period_chart.*",
                        card=False,
                        period_days_select=[7, 28, 90, 365, None],
                        options={
                            "legend": {
                                "show": False
                            },
                            "chart": {
                                "zoom": {
                                    "enabled": False,
                                },
                                "toolbar": {
                                    "show": False,
                                },
                                "stacked": False,
                                "type": "line"
                            },
                            "xaxis": {
                                "type": "datetime",
                                "labels": {"show": True}
                            },
                            "yaxis": [
                                {
                                    "labels": {
                                        "show": False,
                                        "formatter": commify("$")
                                    },
                                },
                            ],
                            "colors": ["#F76D00"],
                            "labels": ekp_map(
                                sort_by(
                                    json_array(
                                        "$.price_period_chart.*"
                                    ),
                                    "$.timestamp_ms"
                                ), "$.timestamp_ms"
                            ),
                            "stroke": {
                                "width": [4, 2],
                                "colors": ["#F76D00"],
                                "dashArray": [0, [3, 2]]
                            }
                        },
                        series=[
                            {
                                "name": "Price",
                                "type": "line",
                                "data": ekp_map(
                                    sort_by(
                                        json_array(
                                            "$.price_period_chart.*"),
                                        "$.timestamp_ms"
                                    ),
                                    "$.price_usd"
                                ),
                            },
                            {
                                "name": "Price (Last Period)",
                                "type": "line",
                                "data": ekp_map(
                                    sort_by(
                                        json_array(
                                            "$.price_last_period_chart.*"
                                        ),
                                        "$.timestamp_ms"
                                    ),
                                    "$.price_usd"
                                ),
                            },
                        ],
                    )
                ]
            ),
        ]
    )