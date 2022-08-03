from app.features.info.components.analytics.analytics_price import analytics_price
from app.features.info.components.analytics.analytics_users import analytics_users
from app.features.info.components.analytics.analytics_volume import analytics_volume
from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Hr, Icon, Image, Link, Paragraphs, Row, Span,
                        Tabs, commify, ekp_map, format_currency, sum, Tab,
                        format_mask_address, format_percent, format_template,
                        is_busy, json_array, navigate, sort_by, navigate_back, format_age, Avatar, Form, Select)


def analytics_section(USERS_CHART_NAME, VOLUME_CHART_NAME, PRICE_CHART_NAME):
    return Div(
        when="$.analytics_available",
        children=[
            Span("Analytics", "font-medium-5 mt-3 d-block"),
            Hr(),
            Div(class_name="mt-2"),
            Tabs(
                children=[
                    Tab(
                        label="User Activity",
                        children=[
                            Div(
                                children=[
                                    analytics_users(
                                        USERS_CHART_NAME
                                    )
                                ]
                            )
                        ]
                    ),
                    Tab(
                        label="Volume",
                        children=[
                            Div(
                                children=[
                                    analytics_volume(
                                        VOLUME_CHART_NAME
                                    )
                                ]
                            )
                        ]
                    ),
                    Tab(
                        label="Price",
                        children=[
                            Div(
                                children=[
                                    analytics_price(
                                        PRICE_CHART_NAME
                                    )
                                ]
                            )
                        ]
                    )

                ]
            )
        ]
    )
