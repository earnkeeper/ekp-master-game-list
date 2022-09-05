from app.features.stats.shared import name_cell, change_cell, social_followers
from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Icon, Image, Link, Paragraphs, Row, Span, commify,
                        ekp_map, format_currency, format_mask_address,
                        format_percent, format_template, is_busy, json_array,
                        navigate, sort_by, switch_case, Hr, Tabs, Tab)
from ekp_sdk.util import collection, documents


def activity_tab(
        COLLECTION_NAME,
        VOLUME_CHART_COLLECTION_NAME,
        PRICE_CHART_COLLECTION_NAME,
        USERS_CHART_COLLECTION_NAME
):
    return Container(
        children=[
            page_title("activity", "Games"),
            analytics_section(
                VOLUME_CHART_COLLECTION_NAME,
                PRICE_CHART_COLLECTION_NAME,
                USERS_CHART_COLLECTION_NAME
            ),
            # __volumes_section(VOLUME_CHART_COLLECTION_NAME),
            # Hr(),
            Div(style={"height": "50px"}),
            __table_section(COLLECTION_NAME)
            # __table_row(COLLECTION_NAME)
        ]
    )


def analytics_section(VOLUME_CHART_COLLECTION_NAME, PRICE_CHART_COLLECTION_NAME, USERS_CHART_COLLECTION_NAME):
    return Div(
        children=[
            Div(
                # when="$.analytics_volume",
                when=f"$.{VOLUME_CHART_COLLECTION_NAME}",
                children=[
                    Span("Analytics", "font-medium-5 mt-3 d-block"),
                    Hr(),
                    Div(class_name="mt-2"),
                    Tabs(
                        children=[
                            Tab(
                                label="Users",
                                children=[
                                    Div(
                                        context=f"$.{USERS_CHART_COLLECTION_NAME}.*",
                                        children=[
                                            analytics_users(
                                                USERS_CHART_COLLECTION_NAME
                                            )
                                        ]
                                    )
                                ]
                            ),
                            Tab(
                                label="Volume",
                                children=[
                                    Div(
                                        context=f"$.{VOLUME_CHART_COLLECTION_NAME}.*",
                                        children=[
                                            analytics_volume(
                                                VOLUME_CHART_COLLECTION_NAME
                                            )
                                        ]
                                    )
                                ]
                            ),
                        ]
                    )
                ]
            )
        ]
    )

def analytics_users(USERS_CHART_COLLECTION_NAME):
    return Div(
        when="$",
        children=[
            Card(
                children=[
                    Div(
                        when="$.is_subscribed",
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
                                name=USERS_CHART_COLLECTION_NAME,
                                height=350,
                                type="line",
                                data=f"$.users_period_chart.*",
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
                                        "name": "Users",
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
                                        "name": "Users (Last Period)",
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
                    Div(
                        when={"not": "$.is_subscribed"},
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
                                name=USERS_CHART_COLLECTION_NAME,
                                height=350,
                                type="line",
                                data=f"$.users_period_chart.*",
                                card=False,
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
                                        "name": "Users",
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
                                        "name": "Users (Last Period)",
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
                            ),
                            Span(
                                "By default you can see historical data for the past 7 days. Want to see more deep historical data?"),
                            Div(class_name="pt-1"),
                            Link(content="Subscribe here", href="/account")
                        ]
                    ),

                ]
            )
        ]
    )

def analytics_volume(VOLUME_CHART_COLLECTION_NAME):
    return Div(
        when="$",
        children=[
            Card(
                children=[
                    Div(
                        when="$.is_subscribed",
                        context="$.analytics_volume",
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
                                name=VOLUME_CHART_COLLECTION_NAME,
                                height=350,
                                type="line",
                                data=f"$.volume_period_chart.*",
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
                                                "$.volume_period_chart.*"
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
                                        "name": "Volume",
                                        "type": "line",
                                        "data": ekp_map(
                                            sort_by(
                                                json_array(
                                                    "$.volume_period_chart.*"),
                                                "$.timestamp_ms"
                                            ),
                                            "$.volume_usd"
                                        ),
                                    },
                                    {
                                        "name": "Volume (Last Period)",
                                        "type": "line",
                                        "data": ekp_map(
                                            sort_by(
                                                json_array(
                                                    "$.volume_last_period_chart.*"
                                                ),
                                                "$.timestamp_ms"
                                            ),
                                            "$.volume_usd"
                                        ),
                                    },
                                ],
                            )
                        ]
                    ),
                    Div(
                        when={"not": "$.is_subscribed"},
                        context="$.analytics_volume",
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
                                name=VOLUME_CHART_COLLECTION_NAME,
                                height=350,
                                type="line",
                                data=f"$.volume_period_chart.*",
                                card=False,
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
                                                "$.volume_period_chart.*"
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
                                        "name": "Volume",
                                        "type": "line",
                                        "data": ekp_map(
                                            sort_by(
                                                json_array(
                                                    "$.volume_period_chart.*"),
                                                "$.timestamp_ms"
                                            ),
                                            "$.volume_usd"
                                        ),
                                    },
                                    {
                                        "name": "Volume (Last Period)",
                                        "type": "line",
                                        "data": ekp_map(
                                            sort_by(
                                                json_array(
                                                    "$.volume_last_period_chart.*"
                                                ),
                                                "$.timestamp_ms"
                                            ),
                                            "$.volume_usd"
                                        ),
                                    },
                                ],
                            ),
                            Span(
                                "By default you can see historical data for the past 7 days. Want to see more deep historical data?"),
                            Div(class_name="pt-1"),
                            Link(content="Subscribe here", href="/account")
                        ]
                    ),
                ]
            )
        ]
    )

def analytics_price(PRICE_CHART_COLLECTION_NAME):
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
                        name=PRICE_CHART_COLLECTION_NAME,
                        height=350,
                        type="line",
                        data=f"$.price_period_chart.*",
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

# def __volumes_section(VOLUME_CHART_COLLECTION_NAME):
#     return Div([
#         Span("Volumes of all games", "font-medium-5 mt-3 d-block"),
#         Hr(),
#         Div(
#             when=f"$.{VOLUME_CHART_COLLECTION_NAME}",
#             children=[
#                 Span(
#                     "Here is the graph of all games volume according to each day for the past 7 days.",
#                 ),
#                 Div(style={"height": "20px"}),
#                 __volume_chart(VOLUME_CHART_COLLECTION_NAME)
#             ]
#         ),
#     ])


def __table_section(COLLECTION_NAME):
    return Div([
        Span("Stats of all games", "font-medium-5 mt-3 d-block"),
        Hr(),
        Div(
            children=[
                Span(
                    "Price, social and volume data for hundreds of games. Sort by any metric, search for your game, subscribe if you want more flexibility and alerts on any metric changes.",
                ),
                Div(style={"height": "20px"}),
                __table_row(COLLECTION_NAME)
            ]
        ),
    ])

# def __volume_chart(VOLUME_CHART_COLLECTION_NAME):
#     return Div(
#         style={
#             "marginRight": "-10px",
#             "marginLeft": "-22px",
#             "marginBottom": "-14px",
#             "marginTop": "-20px"
#         },
#         class_name="mx-1 my-2",
#         children=[
#             Chart(
#                 title="",
#                 height=220,
#                 type="line",
#                 data=f"$.{VOLUME_CHART_COLLECTION_NAME}.*",
#                 card=False,
#                 options={
#                     "legend": {
#                         "show": False
#                     },
#                     "chart": {
#                         "zoom": {
#                             "enabled": False,
#                         },
#                         "toolbar": {
#                             "show": False,
#                         },
#                         "stacked": False,
#                         "type": "line"
#                     },
#                     "xaxis": {
#                         "type": "datetime",
#                         "labels": {"show": True}
#                     },
#                     "yaxis": [
#                         {
#                             "labels": {
#                                 "show": False,
#                                 "formatter": commify("$")
#                             },
#                         },
#                     ],
#                     "colors": ["#F76D00"],
#                     "labels": ekp_map(
#                         sort_by(
#                             json_array(
#                                 f"$.{VOLUME_CHART_COLLECTION_NAME}.*"
#                             ),
#                             "$.timestamp_ms"
#                         ), "$.timestamp_ms"
#                     ),
#                     "stroke": {
#                         "width": [4, 4],
#                         # "curve": 'smooth',
#                         "dashArray": [0, [3, 2]],
#                         "colors": ["#F76D00"]
#                     }
#                 },
#                 series=[
#                     {
#                         "name": "Volume",
#                         "type": "line",
#                         "data": ekp_map(
#                             sort_by(
#                                 json_array(f"$.{VOLUME_CHART_COLLECTION_NAME}.*"),
#                                 "$.timestamp_ms"
#                             ),
#                             "$.volume"
#                         ),
#                     },
#                 ],
#             )
#         ]
#     )

def __table_row(COLLECTION_NAME):
    return Datatable(
        alert_config={
            "formId": "game_alerts"
        },
        class_name="mt-1",
        data=documents(COLLECTION_NAME),
        busy_when=is_busy(collection(COLLECTION_NAME)),
        default_sort_field_id="price_delta_pc",
        default_sort_asc=False,
        show_export=False,
        show_last_updated=True,
        columns=[
            Column(
                id="game_name",
                title="Game",
                min_width="240px",
                cell=name_cell("$.game_name"),
                searchable=True,
                sortable=True,
                # right=True
            ),
            Column(
                id="genre",
                title="Genre",
                min_width="120px",
                value="$.genre",
                # cell=name_cell("$.genre"),
                searchable=True,
                sortable=True,
                # right=True
            ),
            Column(
                id="platform",
                title="Platform",
                min_width="80px",
                value="$.platform",
                # cell=name_cell("$.genre"),
                searchable=True,
                sortable=True,
                # right=True
            ),
            Column(
                id="price24h",
                title="Price",
                sortable=True,
                width="100px",
                cell=change_cell(format_currency("$.price", "$.fiat_symbol", False), "$.price_delta_pc", "$.price_delta_color"),
                right=True
            ),
            Column(
                id="discord_members",
                title="Discord",
                sortable=True,
                width="160px",
                cell=social_followers("$.discord_members", "$.change_24h_discord", "$.change_24h_discord_color",
                                      "$.discord_plus", "$.change_24h_pc_discord"),
                right=True
            ),
            Column(
                id="twitter_followers",
                title="Twitter",
                sortable=True,
                width="160px",
                cell=social_followers("$.twitter_followers", "$.change_24h", "$.change_24h_color", "$.twitter_plus",
                                      "$.change_24h_pc"),
                right=True
            ),
            Column(
                id="newUsers24h",
                title="New Users",
                sortable=True,
                width="130px",
                cell=change_cell(
                    commify("$.newUsers24h"),
                    "$.newUsersDelta",
                    "$.activity_deltaColor"
                ),
                right=True
            ),
            # Column(
            #     id="newUsers7d",
            #     title="New Users 7d",
            #     sortable=True,
            #     format=commify("$.newUsers7d"),
            #     width="120px",
            #     cell=change_cell(
            #         commify("$.newUsers7d"),
            #         "$.newUsers7dDelta",
            #         "$.delta7dColor"
            #
            #     ),
            #     right=True
            # ),
            # Column(
            #     id="newUsers7dDelta",
            #     title="New Users 7d %",
            #     sortable=True,
            #     omit=True,
            # ),
            Column(
                id="newUsersDelta",
                title="New Users 24h %",
                sortable=True,
                omit=True,
            ),
            Column(
                id="price_delta_pc",
                title="Price 24h %",
                sortable=True,
                omit=True,
            ),
            Column(
                id="volume24h",
                title="Volume",
                sortable=True,
                width="150px",
                cell=change_cell(format_currency("$.volume24h", None), "$.volumeDelta", "$.deltaColor"),
                right=True
            ),
            Column(
                id="volumeDelta",
                title="Volume 24h %",
                sortable=True,
                omit=True,
            ),
            # Column(
            #     id="volume7d",
            #     title="Volume 7d",
            #     sortable=True,
            #     width="150px",
            #     cell=change_cell(format_currency("$.volume7d", None), "$.volume7dDelta", "$.delta7dColor"),
            #     right=True
            # ),
            # Column(
            #     id="volume7dDelta",
            #     title="Volume 7d %",
            #     sortable=True,
            #     omit=True,
            # ),
            # Column(
            #     id="chart7d",
            #     title="",
            #     width="120px",
            #     cell=__chart_cell('$.chart7d.*')
            # ),
            Column(
                id="change_24h",
                title="Twitter Change",
                sortable=True,
                omit=True
            ),
            Column(
                id="change_24h_pc",
                title="Twitter Change %",
                sortable=True,
                omit=True
            ),
            Column(
                id="change_24h_discord",
                title="Discord Change",
                sortable=True,
                omit=True
            ),
            Column(
                id="change_24h_pc_discord",
                title="Discord Change %",
                sortable=True,
                omit=True
            ),
        ]
    )


def __chart_cell(path):
    return Div(
        style={
            "marginLeft": "-32px",
            "marginRight": "-16px",
            "marginBottom": "-8px",
        },
        children=[
            Chart(
                title="",
                card=False,
                type='area',
                height=90,
                series=[
                    {
                        "name": 'All',
                        "type": "area",
                        "data": ekp_map(
                            sort_by(
                                json_array(path),
                                '$.timestamp',
                            ),
                            ['$.timestamp_ms', '$.newUsers'],
                        ),
                    },
                ],
                data=path,
                options={
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
                    "fill": {
                        "colors": ["#F76D00"]
                    },
                    "stroke": {
                        "width": 3,
                        "curve": "smooth",
                        "colors": ["#F76D00"]
                    },
                    "grid": {
                        "show": False,
                    },
                    "dataLabels": {
                        "enabled": False
                    },
                    "xaxis": {
                        "axisBorder": {"show": False},
                        "axisTicks": {"show": False},
                        "type": "datetime",
                        "labels": {
                            "show": False
                        },
                    },
                    "yaxis": {
                        "labels": {
                            "show": False
                        },
                    },
                }
            )
        ])