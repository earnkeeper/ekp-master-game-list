from app.features.info.ui.components.analytics.analytics_section import analytics_section
from app.features.info.ui.components.analytics.analytics_volume import analytics_volume
from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Hr, Icon, Image, Link, Paragraphs, Row, Span,
                        Tabs, commify, ekp_map, format_currency, sum, Tab,
                        format_mask_address, format_percent, format_template,
                        is_busy, json_array, navigate, sort_by, navigate_back, format_age, Avatar, Form, Select)


def page(GAME_INFO_COLLECTION_NAME, USERS_CHART_NAME, VOLUME_CHART_NAME, PRICE_CHART_NAME):
    return Container(
        children=[
            Div(
                context=format_template(f"$['{GAME_INFO_COLLECTION_NAME}']" + "[?(@.id == '{{ game_id }}')]", {
                    "game_id": "$.location.pathParams[1]"
                }),
                children=[
                    Div(
                        when="$",
                        children=[
                            Row([
                                Col(
                                    "col-auto my-auto pr-0",
                                    [
                                        Icon('chevron-left', size='lg',
                                             on_click=navigate_back())
                                    ]),
                                Col(
                                    "col-auto my-auto",
                                    [
                                        Span('$.name', 'font-large-2 d-block'),
                                    ])
                            ]),
                            Div(style={"marginTop": "-10px"}),
                            Hr(),
                            __socials_section(),
                            __info_section(),
                            __resources_section(),
                            __media_section(),
                            __shared_games_section(),
                            __volumes_section(),
                            analytics_section(
                                USERS_CHART_NAME,
                                VOLUME_CHART_NAME,
                                PRICE_CHART_NAME
                            ),
                            __deep_dives_section(),
                            Div([], style={"height": "300px"})
                        ]
                    ),
                    Div(
                        when={"not": "$"},
                        children=[page_title('loader', 'Loading')]
                    )
                ],
            )
        ]
    )


def __info_section():
    return [
        Div([
            Image(
                when={"not": "$.banner"},
                src="https://pbs.twimg.com/profile_banners/1434504204765339652/1651046414/1500x500",
            ),
            Image(
                when="$.banner",
                src="$.banner",
            ),
            Div([], "mb-2"),

            Span("$.description", "new-line d-block"),
        ])
    ]


def __media_section():
    return Div(
        when="$.media",
        children=[
            Div(
                children=[
                    Span("Media", "font-medium-5 mt-3 d-block"),
                    Hr(),
                    Span(
                        "We search the web for the best content for Play To Earn games, focusing on gameplay, economy health and earning potential.",
                    ),
                ]),
            Div(
                children=[
                    Div(style={"height": "48px"}),
                    {
                        "_type": "Scroller",
                        "props": {
                            "data": json_array("$.media.*"),
                            "tileSchema": __media_card()
                        }
                    },
                ]
            ),
        ])


def __shared_games_section():
    return Div(
        when=f"$.shared_games",
        children=[
            Div(
                children=[
                    Span("Similar Games", "font-medium-5 mt-3 d-block"),
                    Hr(),
                    Span(
                        format_template(
                            "Here are the top 10 games that players of {{ game_name }} are also playing.",
                            {"game_name": "$.name"}
                        ))
                    # Span(
                    #     "Here are the top 10 games that players of Metabomb are also playing.",
                    # ),
                ]),
            Div(
                children=[
                    Div(style={"height": "48px"}),
                    {
                        "_type": "Scroller",
                        "props": {
                            "data": json_array(f"$.shared_games.*"),
                            "tileSchema": __shared_games_card()
                        }
                    },
                ]
            ),
        ])


def __resources_section():
    return Div(
        # when="$",
        # context="$.resources.*",
        children=[
            Span("Earning Resources", "font-medium-5 mt-3 d-block"),
            Hr(),
            Div(
                children=[
                    __resource_description(),
                    __resource_description_if_not_links(),
                    Div(class_name="mt-2"),
                    __single_resource(0),
                    __single_resource(1),
                    __single_resource(2),
                    __single_resource(3),
                    __single_resource(4),
                    __single_resource(5),
                    __single_resource(6),
                    __single_resource(7),
                    __single_resource(8),
                    __single_resource(9),
                    # Div(style={"marginTop": "-10px"}),

                ]
            )
        ])


def __resource_description():
    return Div(
        when="$.resources.*",
        children=[
            Span(
                "We hunt down the best resources for teaching you how to earn in our games. "
                "From tools, to videos to spreadsheets, you will find all the info here you "
                "need to get started earning in this game."
            ),
        ]
    )


def __resource_description_if_not_links():
    return Div(
        when={"not": "$.resources.*"},
        children=[
            Span("Want to see curated resources for calculating earning in this game?"),
            Div(style={"height": "8px"}),
            Span("Add a feedback item "),
            Link(content="here", href="https://feedback.earnkeeper.io", external=True),
            Span(", then ping us on "),
            Link(content="discord",
                 href="https://discord.gg/RHnnWBAkes", external=True),
            Span(" to talk it through."),
        ]
    )


# def __single_resource(rank_id):
#     return Div(
#         # when=f"$.resources[{rank_id}]",
#         context=f"$.resources[{rank_id}]",
#         children=[
#             Row([
#                 # Col(
#                 #     when="$.icon",
#                 #     class_name="col-auto my-auto pr-0",
#                 #     children=[
#                 #         Icon(
#                 #             "$.icon",
#                 #             size='sm',
#                 #             style={
#                 #                 "marginRight": "6px"
#                 #             }
#                 #         ),
#                 #     ]),
#                 Col(
#                     "col-auto my-auto",
#                     [
#                         Link(
#                             class_name="d-block",
#                             content = Div(
#
#                             ) ,
#                             external=True,
#                             external_icon=True,
#                             href="$.link"),
#                     ])
#             ]),
#         ]
#     )

def __single_resource(rank_id):
    return Div(
        when=f"$",
        context=f"$.resources[{rank_id}]",
        class_name="mt-1",
        children=[
            Link(
                class_name="d-block",
                content=Div(
                    class_name="ml-2",
                    children=[
                        Row([
                            Col(
                                when="$.icon",
                                class_name="col-auto my-auto",
                                children=[
                                    Icon(
                                        "$.icon",
                                        size='sm',
                                    ),
                                ]),
                            Col(
                                "col-auto my-auto pl-0",
                                [
                                    Span("$.title")
                                ])
                        ]),
                    ]
                ),
                external=True,
                href="$.link"
            ),
        ]

    )


def __volumes_section():
    return Div([
        Span("Volumes and Stats", "font-medium-5 mt-3 d-block"),
        Hr(),
        Div(
            when="$.statsAvailable",
            children=[
                Span(
                    "We collect volume statistics for hundreds of games to show you were users are spending their time.",
                ),
                Div(style={"height": "8px"}),
                Span(
                    format_template("The stats we have for {{ name }} are below.", {
                        "name": "$.name"
                    }),
                ),
                Div(style={"height": "16px"}),
                Row([
                    Col(
                        class_name="col-12 col-md-6 col-lg-4",
                        when="$.social",
                        children=[
                            __socials_card()
                        ]
                    ),
                    Col(
                        class_name="col-12 col-md-6 col-lg-4",
                        when="$.activity",
                        children=[
                            __activity_card()
                        ]
                    ),
                    Col(
                        class_name="col-12 col-md-6 col-lg-4",
                        when="$.volume",
                        children=[
                            __volume_card()
                        ]
                    ),
                    Col(
                        class_name="col-12 col-md-6 col-lg-4",
                        when="$.price",
                        children=[
                            __price_card()
                        ]
                    ),
                ])
            ]
        ),
        Div(
            when={"not": "$.statsAvailable"},
            children=[
                Span("⚠️ We have not collected any usage stats for this game yet."),
                Div(style={"height": "8px"}),
                Span(
                    "Connect with us on discord if you would like us to dive deeper"
                ),
            ]
        )

    ])


def __deep_dives_section():
    return Div(
        children=[
            Span("Deep Dives", "font-medium-5 mt-3 d-block"),
            Hr(),
            Span(
                "Want to see an earnings deep dive on this game like we have already done on "
            ),
            Link(content="Metabomb", href="/game/metabomb"),
            Span(", "),
            Link(content="Thetan Arena", href="/game/thetan-arena"),
            Span(" and more?"),
            Div(style={"height": "8px"}),
            Span("Add a feedback item "),
            Link(content="here", href="https://feedback.earnkeeper.io", external=True),
            Span(", then ping us on "),
            Link(content="discord",
                 href="https://discord.gg/RHnnWBAkes", external=True),
            Span(" to talk it through."),
            Div(style={"height": "24px"}),
            {
                "_type": "DeepDives",
                "props": {
                    "gameId": "$.id"
                }
            }
        ])


def __media_card():
    return Div(
        style={"width": "320px"},
        children=[
            Div(
                children=[
                    Image(
                        class_name="mb-1",
                        src="$.thumbnail",
                        style={"height": "150px", "width": "100%"}
                    ),
                ]
            ),
            Div(
                style={"height": "52px"},
                class_name="px-1",
                children=[
                    Link(
                        class_name="font-small-3",
                        href="$.link",
                        external=True,
                        content="$.title",
                    ),
                ]
            ),
            Div(
                class_name="ml-1 mr-2 mt-1 mb-2",
                children=[
                    Row(
                        children=[
                            Col(
                                class_name="col-6",
                                children=[
                                    # Icon(
                                    #     "user",
                                    #     size='sm',
                                    #     style={
                                    #         "marginRight": "6px"
                                    #     }
                                    # ),
                                    Span("$.channel_name", "font-small-3")
                                ]
                            ),
                            Col(
                                class_name="col-6",
                                children=[
                                    Icon(
                                        "users",
                                        size='sm',
                                        style={
                                            "marginRight": "6px"
                                        }
                                    ),
                                    Span(
                                        format_template(
                                            "{{ subscribers_count }} subs",
                                            {"subscribers_count": "$.subscribers_count"}
                                        ), "font-small-2")
                                ]
                            )
                        ]
                    )
                ]
            ),
            Div(
                class_name="ml-1 mr-2 mt-1 mb-2",
                children=[
                    Row(
                        children=[
                            Col(
                                class_name="col-6",
                                children=[
                                    Icon(
                                        "calendar",
                                        size='sm',
                                        style={
                                            "marginRight": "6px"
                                        }
                                    ),
                                    Span(format_age("$.publish_time"),
                                         "font-small-2")
                                ]
                            ),
                            Col(
                                class_name="col-6",
                                children=[
                                    Icon(
                                        "eye",
                                        size='sm',
                                        style={
                                            "marginRight": "6px"
                                        }
                                    ),
                                    Span("$.view_count", "font-small-2")
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )


def __shared_games_card():
    return Div(
        style={"width": "320px"},
        children=[
            Div(
                children=[
                    Image(
                        class_name="mb-1",
                        src="$.banner_url",
                        style={"height": "150px", "width": "100%"}
                    ),
                ]
            ),
            Div(
                # style={"height": "52px"},
                class_name="px-1",
                children=[
                    Link(
                        class_name="font-small-3",
                        href=format_template("/game/all/info/{{ id }}", {
                            "id": "$.shared_game_id"
                        }),
                        external=True,
                        content="$.game",
                    ),
                ]
            ),
            Div(
                class_name="ml-1 mr-2 mt-1 mb-2",
                children=[
                    Row(
                        children=[
                            Col(
                                class_name="col-12",
                                children=[
                                    Icon(
                                        "user",
                                        size='sm',
                                        style={
                                            "marginRight": "6px"
                                        }
                                    ),
                                    Span(
                                        format_template(
                                            "{{ shared_players }} shared players",
                                            {"shared_players": "$.players"}
                                        ), "font-small-3")
                                ]
                            ),
                        ]
                    )
                ]
            ),
        ]
    )


def __activity_card():
    return Div(
        context="$.activity",
        children=[
            Card(
                children=[
                    __activity_stats(),
                    Hr(),
                    __activity_chart(),
                ]
            )
        ]
    )


def __socials_card():
    return Div(
        context="$.social",
        children=[
            Card(
                children=[
                    __socials_stats(),
                    Hr(),
                    __socials_chart(),
                ]
            )
        ]
    )


def __activity_chart():
    return Div(
        style={
            "marginRight": "-10px",
            "marginLeft": "-22px",
            "marginBottom": "-14px",
            "marginTop": "-20px"
        },
        children=[
            Chart(
                title="",
                height=220,
                type="line",
                data="$.chart7d.*",
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
                                "formatter": commify("$"),
                            },
                        },
                    ],
                    "colors": ["#F76D00"],
                    "labels": ekp_map(
                        sort_by(
                            json_array(
                                "$.chart7d.*"
                            ),
                            "$.timestamp_ms"
                        ), "$.timestamp_ms"
                    ),
                    "stroke": {
                        "width": [4, 4],
                        "curve": 'smooth',
                        "colors": ["#F76D00"]
                    }
                },
                series=[
                    {
                        "name": "New Users",
                        "type": "line",
                        "data": ekp_map(
                            sort_by(
                                json_array("$.chart7d.*"),
                                "$.timestamp_ms"
                            ),
                            "$.newUsers"
                        ),
                    },
                ],
            )
        ]
    )


def __socials_chart():
    return Div(
        style={
            "marginRight": "-10px",
            "marginLeft": "-22px",
            "marginBottom": "-14px",
            "marginTop": "-20px"
        },
        children=[
            Chart(
                title="",
                height=220,
                type="line",
                data="$.chart.*",
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
                                "formatter": commify("$"),
                            },
                        },
                    ],
                    "colors": ["#F76D00"],
                    "labels": ekp_map(
                        sort_by(
                            json_array(
                                "$.chart.*"
                            ),
                            "$.timestamp_ms"
                        ), "$.timestamp_ms"
                    ),
                    "stroke": {
                        "width": [4, 4],
                        "curve": 'smooth',
                        "colors": ["#F76D00"]
                    }
                },
                series=[
                    {
                        "name": "New Followers",
                        "type": "line",
                        "data": ekp_map(
                            sort_by(
                                json_array("$.chart.*"),
                                "$.timestamp_ms"
                            ),
                            "$.value"
                        ),
                    },
                ],
            )
        ]
    )


def __activity_stats():
    return Row(
        class_name="my-1 mx-0",
        children=[
            Col(
                "col-6",
                [
                    Span("New Users (24h)", "d-block font-small-3"),
                    Span(
                        commify("$.newUsers24h"),
                        format_template(
                            "d-block font-small-2 text-{{ color }}",
                            {
                                "color": "$.deltaColor"
                            }
                        )
                    ),
                ]
            ),
            Col(
                "col-6",
                [
                    Span("Change (24h)", "d-block font-small-3 text-right"),
                    Span(
                        format_percent("$.newUsersDelta"),
                        format_template(
                            "d-block font-small-2 text-right text-{{ color }}",
                            {
                                "color": "$.deltaColor"
                            }
                        )
                    ),
                ]
            ),
        ]
    )


def __socials_stats():
    return Row(
        class_name="my-1 mx-0",
        children=[
            Col(
                "col-6",
                [
                    Span("New Followers (24h)", "d-block font-small-3"),
                    Span(
                        commify("$.change_24h"),
                        format_template(
                            "d-block font-small-2 text-{{ color }}",
                            {
                                "color": "$.change_24h_color"
                            }
                        )
                    ),
                ]
            ),
            Col(
                "col-6",
                [
                    Span("Change (24h)", "d-block font-small-3 text-right"),
                    Span(
                        format_percent("$.change_24h_pc"),
                        format_template(
                            "d-block font-small-2 text-right text-{{ color }}",
                            {
                                "color": "$.change_24h_color"
                            }
                        )
                    ),
                ]
            ),
        ]
    )


def __volume_card():
    return Div(
        context="$.volume",
        children=[
            Card(
                children=[
                    __volume_stats(),
                    Hr(),
                    __volume_chart(),
                ]
            )
        ]
    )


def __price_card():
    return Div(
        children=[
            Card(
                children=[
                    __price_stats(),
                    Hr(),
                    __price_chart(),
                ]
            )
        ]
    )


def __volume_chart():
    return Div(
        style={
            "marginRight": "-10px",
            "marginLeft": "-22px",
            "marginBottom": "-14px",
            "marginTop": "-20px"
        },
        children=[
            Chart(
                title="",
                height=220,
                type="line",
                data="$.chart7d.*",
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
                                "$.chart7d.*"
                            ),
                            "$.timestamp_ms"
                        ), "$.timestamp_ms"
                    ),
                    "stroke": {
                        "width": [4, 4],
                        "curve": 'smooth',
                        "colors": ["#F76D00"]
                    }
                },
                series=[
                    {
                        "name": "Volume",
                        "type": "line",
                        "data": ekp_map(
                            sort_by(
                                json_array("$.chart7d.*"),
                                "$.timestamp_ms"
                            ),
                            "$.volume"
                        ),
                    },
                ],
            )
        ]
    )


def __price_chart():
    return Div(
        style={
            "marginRight": "-10px",
            "marginLeft": "-22px",
            "marginBottom": "-14px",
            "marginTop": "-20px"
        },
        children=[
            Chart(
                title="",
                height=220,
                type="line",
                data="$.price.chart.*",
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
                                "formatter": "$",
                            },
                        },
                    ],
                    "colors": ["#F76D00"],
                    "labels": ekp_map(
                        sort_by(
                            json_array(
                                "$.price.chart.*"
                            ),
                            "$.timestamp_ms"
                        ), "$.timestamp_ms"
                    ),
                    "stroke": {
                        "width": [4, 4],
                        "curve": 'smooth',
                        "colors": ["#F76D00"]
                    }
                },
                series=[
                    {
                        "name": "Price",
                        "type": "line",
                        "data": ekp_map(
                            sort_by(
                                json_array("$.price.chart.*"),
                                "$.timestamp_ms"
                            ),
                            "$.price"
                        ),
                    },
                ],
            )
        ]
    )


def __volume_stats():
    return Row(
        class_name="my-1 mx-0",
        children=[
            Col(
                "col-6",
                [
                    Span("Token Volume (24h)", "d-block font-small-3"),
                    Span(
                        format_currency("$.volume24h", None),
                        format_template(
                            "d-block font-small-2 text-{{ color }}",
                            {
                                "color": "$.deltaColor"
                            }
                        )
                    ),
                ]
            ),
            Col(
                "col-6",
                [
                    Span("Change (24h)", "d-block font-small-3 text-right"),
                    Span(
                        format_percent("$.volumeDelta"),
                        format_template(
                            "d-block font-small-2 text-right text-{{ color }}",
                            {
                                "color": "$.deltaColor"
                            }
                        )
                    ),
                ]
            ),
        ]
    )


def __price_stats():
    return Row(
        class_name="my-1 mx-0",
        children=[
            Col(
                "col-6",
                [
                    Span("Token Price", "d-block font-small-3"),
                    Span(
                        # format_currency("$.volume24h", None),
                        format_template(" {{ fiat_symbol }} {{ price }}", {
                            "price": "$.price.current_price",
                            "fiat_symbol": "$.fiat_symbol"
                        }),
                        format_template(
                            "d-block font-small-2 text-{{ color }}",
                            {
                                "color": "$.price.price_color"
                            }
                        )
                    ),
                ]
            ),
            Col(
                "col-6",
                [
                    Span("Change (24h)", "d-block font-small-3 text-right"),
                    Span(
                        format_percent("$.price.price_delta_pc"),
                        format_template(
                            "d-block font-small-2 text-right text-{{ color }}",
                            {
                                "color": "$.price.price_color"
                            }
                        )
                    ),
                ]
            ),
        ]
    )


def __socials_section():
    return Row(
        class_name="mb-2",
        children=[
            __image_link_col(
                "$.coingecko",
                "https://static.coingecko.com/s/thumbnail-007177f3eca19695592f0b8b0eabbdae282b54154e1be912285c9034ea6cbaf2.png",
                format_template("{{ price }} ( {{ price_delta_pc }} )", {
                    "price": format_currency("$.price.current_price", "$.fiat_symbol", False),
                    "price_delta_pc": format_percent("$.price.price_delta_pc")
                }),
                "$.price.price_color"
            ),
            __icon_link_col("$.website", "cil-globe-alt", "Website"),
            __icon_link_col(
                "$.twitter",
                "cib-twitter",
                commify("$.twitter_followers")
            ),
            __icon_link_col(
                "$.telegram",
                "cib-telegram",
                commify("$.telegram_members")
            ),
            __icon_link_col(
                "$.discord",
                "cib-discord",
                commify("$.discord_members")
            ),
            __icon_text_col("$.genre", "cil-gamepad"),
            __icon_text_col("$.platform", "cil-laptop"),
        ]
    )


def __image_link_col(href, image_url, content, color):
    return Col(
        when=href,
        class_name="col-auto my-auto pr-2 pb-1",
        children=[
            Link(
                href=href,
                external=True,
                content=Row(
                    [
                        Col(
                            "col-auto my-auto pr-0",
                            [
                                Image(
                                    src=image_url,
                                    style={"height": "20px",
                                           "marginTop": "-2px"}
                                )
                            ]
                        ),
                        Col(
                            "col-auto px-0",
                            [Div([], style={"width": "8px"})]
                        ),
                        Col(
                            "col-auto my-auto px-0",
                            [
                                Span(
                                    content,
                                    format_template("font-small-3 font-weight-bold text-{{ color }}", {
                                        "color": color
                                    })
                                )
                            ]
                        )
                    ]
                )
            )
        ]
    )


def __icon_text_col(content, icon):
    return Col(
        when=content,
        class_name="col-auto my-auto pr-2 pb-1",
        children=[
            Row(
                [
                    Col(
                        "col-auto my-auto pr-0",
                        [
                            Icon(
                                icon,
                                size='lg'
                            )
                        ]
                    ),
                    Col(
                        "col-auto px-0",
                        [Div([], style={"width": "8px"})]
                    ),
                    Col(
                        "col-auto my-auto px-0",
                        [
                            Span(
                                content,
                                "font-small-3 font-weight-bold"
                            )
                        ]
                    )
                ]
            )
        ]
    )


def __icon_link_col(href, icon_name, content):
    return Col(
        when=href,
        class_name="col-auto my-auto pr-2 pb-1",
        children=[
            Link(
                href=href,
                external=True,
                content=Row(
                    [
                        Col(
                            "col-auto my-auto pr-0",
                            [
                                Icon(
                                    icon_name,
                                    size='lg'
                                )
                            ]
                        ),
                        Col(
                            "col-auto px-0",
                            [Div([], style={"width": "8px"})]
                        ),
                        Col(
                            "col-auto my-auto px-0",
                            [
                                Span(
                                    content,
                                    "font-small-3 font-weight-bold"
                                )
                            ]
                        )
                    ]
                )
            )
        ]
    )
