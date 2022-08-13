from app.features.info.ui.components.analytics.analytics_volume import analytics_volume
from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Hr, Icon, Image, Link, Paragraphs, Row, Span,
                        Tabs, commify, ekp_map, format_currency, sum, Tab,
                        format_mask_address, format_percent, format_template,
                        is_busy, json_array, navigate, sort_by, navigate_back, format_age, Avatar, Form, Select)

def analytics_users(USERS_CHART_NAME):
    return Card(
        children=[
            Div(
                context="$.analytics_users",
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
                        name=USERS_CHART_NAME,
                        height=350,
                        type="line",
                        data="$.users_period_chart.*",
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
                                        "$.users_period_chart.*"
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
                                "name": "Active Users",
                                "type": "line",
                                "data": ekp_map(
                                    sort_by(
                                        json_array(
                                            "$.users_period_chart.*"),
                                        "$.timestamp_ms"
                                    ),
                                    "$.active_users"
                                ),
                            },
                            {
                                "name": "Active Users (Last Period)",
                                "type": "line",
                                "data": ekp_map(
                                    sort_by(
                                        json_array(
                                            "$.users_last_period_chart.*"
                                        ),
                                        "$.timestamp_ms"
                                    ),
                                    "$.active_users"
                                ),
                            },
                        ],
                    )
                ]
            ),
        ]
    )