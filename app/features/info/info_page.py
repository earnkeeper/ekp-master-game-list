from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Hr, Icon, Image, Link, Paragraphs, Row, Span,
                        Tabs, commify, ekp_map, format_currency,
                        format_mask_address, format_percent, format_template,
                        is_busy, json_array, navigate, sort_by, navigate_back)


def page(GAME_INFO_COLLECTION_NAME):
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
                                        Icon('chevron-left', size='lg', on_click=navigate_back())
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
                            __volumes_section(),
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
                style={"width": "70%"}
            ),
            Image(
                when="$.banner",
                src="$.banner",
                style={"width": "70%"}
            ),
            Div([], "mb-2"),

            Span("$.description", "new-line d-block"),
        ])
    ]


def __volumes_section():
    return Div([
        Span("Volumes and Stats", "font-medium-5 mt-3 d-block"),
        Hr(),
        Div(
            when="$.statsAvailable",
            children=[
                Span(
                    "We collect volume statistics for hundreds of games to show you were users are spending their time."),
                Div(style={"height": "8px"}),
                Span(format_template("The stats we have for {{ name }} are below.", {
                    "name": "$.name"
                })),
                Div(style={"height": "16px"}),
                Row([
                    Col(
                        "col-12 col-md-6 col-lg-4",
                        [
                            __activity_card()
                        ]
                    ),
                    Col(
                        "col-12 col-md-6 col-lg-4",
                        [
                            __volume_card()
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
    return Div([
        Span("Deep Dives", "font-medium-5 mt-3 d-block"),
        Hr(),
        Span("Want to see an earnings deep dive on this game like we have already done on "),
        Link(content="Metabomb", href="/game/metabomb"),
        Span(", "),
        Link(content="Thetan Arena", href="/game/thetan-arena"),
        Span(" and more?"),
        Div(style={"height": "8px"}),
        Span("Add a feedback item "),
        Link(content="here", href="https://feedback.earnkeeper.io", external=True),
        Span(", then ping us on "),
        Link(content="discord", href="https://discord.gg/RHnnWBAkes", external=True),
        Span(" to talk it through."),
        Div(style={"height": "24px"}),
        {
            "_type": "DeepDives",
            "props": {
                "gameId": "$.id"
            }
        }
    ])


def __activity_card():
    return Div(
        context="$.activity",
        when="$",
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
                                "formatter": commify("$")
                            },
                        },
                    ],
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


def __volume_card():
    return Div(
        context="$.volume",
        when="$",
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


def __volume_stats():
    return Row(
        class_name="my-1 mx-0",
        children=[
            Col(
                "col-6",
                [
                    Span("Token Volume (24h)", "d-block font-small-3"),
                    Span(
                        commify("$.volume24h"),
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


def __socials_section():
    return Row(
        class_name="mb-2",
        children=[
            __image_link_col(
                "$.coingecko",
                "https://static.coingecko.com/s/thumbnail-007177f3eca19695592f0b8b0eabbdae282b54154e1be912285c9034ea6cbaf2.png",
                "$.price",
                "$.price_color"
            ),
            __icon_link_col("$.website", "cil-globe-alt", "Website"),
            __icon_link_col("$.twitter", "cib-twitter",
                            commify("$.twitter_followers")),
            __icon_link_col("$.telegram", "cib-telegram",
                            commify("$.telegram_members")),
            __icon_link_col("$.discord", "cib-discord", "Discord"),
        ]
    )


def __image_link_col(href, image_url, content, color):
    return Col(
        when=href,
        class_name="col-auto my-auto pr-2",
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


def __icon_link_col(href, icon_name, content):
    return Col(
        when=href,
        class_name="col-auto my-auto pr-2",
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
