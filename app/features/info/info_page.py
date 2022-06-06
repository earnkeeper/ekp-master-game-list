from app.utils.page_title import page_title
from ekp_sdk.ui import (Card, Chart, Col, Column, Container, Datatable, Div,
                        Image, Link, Paragraphs, Row, Span, collection,
                        commify, documents, ekp_map, format_currency,
                        format_mask_address, format_percent, format_template, Hr,
                        is_busy, json_array, navigate, sort_by, Button, Icon, Tabs)


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
                            Span('$.name', 'font-large-1 d-block'),
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
                src="https://pbs.twimg.com/profile_banners/1434504204765339652/1651046414/1500x500",
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
                Row([
                    Col(
                        "col-12 col-md-6 col-lg-4",
                        [
                            __activity_card()
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
        Paragraphs(
            [
                "Want to see an earnings deep dive on this game like we have already done on Metabomb, Splinterlands and more?",
                "Add a feedback item here, then ping us on discord to talk it through."
            ],
        ),
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


def __socials_section():
    return Row(
        class_name="my-1",
        children=[
            __icon_link_col("$.website", "cil-globe-alt", "Website"),
            __icon_link_col("$.twitter", "cib-twitter", "Twitter"),
            __icon_link_col("$.discord", "cib-discord", "Discord"),
            __icon_link_col("$.telegram", "cib-telegram", "Telegram"),
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
                                    "font-small-2 font-weight-bold"
                                )
                            ]
                        )
                    ]
                )
            )
        ]
    )
