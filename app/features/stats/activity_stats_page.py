from app.features.stats.shared import name_cell, change_cell
from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Icon, Image, Link, Paragraphs, Row, Span, commify,
                        ekp_map, format_currency, format_mask_address,
                        format_percent, format_template, is_busy, json_array,
                        navigate, sort_by, switch_case)
from ekp_sdk.util import collection, documents


def activity_tab(COLLECTION_NAME):
    return Container(
        children=[
            page_title("activity", "Games"),
            __table_row(COLLECTION_NAME)
        ]
    )


def __table_row(COLLECTION_NAME):
    return Datatable(
        class_name="mt-1",
        data=documents(COLLECTION_NAME),
        busy_when=is_busy(collection(COLLECTION_NAME)),
        default_sort_field_id="change_24h",
        default_sort_asc=False,
        show_export=False,
        show_last_updated=True,
        columns=[
            Column(
                id="game_name",
                title="Game",
                min_width="270px",
                cell=name_cell("$.game_name"),
                searchable=True,
                sortable=True,
            ),
            Column(
                id="discord_members",
                title="Discord",
                sortable=True,
                width="160px",
                cell=__discord_members_cell
            ),
            Column(
                id="twitter_followers",
                title="Twitter",
                sortable=True,
                width="160px",
                cell=__twitter_followers_cell
            ),
            Column(
                id="newUsers24h",
                title="New Users 24h",
                sortable=True,
                width="120px",
                cell=change_cell(
                    commify("$.newUsers24h"),
                    "$.newUsersDelta",
                    "$.deltaColor"
                )
            ),
            Column(
                id="newUsers7d",
                title="New Users 7d",
                sortable=True,
                format=commify("$.newUsers7d"),
                width="110px",
                cell=change_cell(
                    commify("$.newUsers7d"),
                    "$.newUsers7dDelta",
                    "$.delta7dColor"

                )
            ),
            Column(
                id="newUsers7dDelta",
                title="New Users 7d %",
                sortable=True,
                omit=True,
            ),
            Column(
                id="newUsersDelta",
                title="New Users 24h %",
                sortable=True,
                omit=True,
            ),
            Column(
                id="volume24h",
                title="Volume 24h",
                sortable=True,
                width="150px",
                cell=change_cell(format_currency("$.volume24h", None), "$.volumeDelta", "$.deltaColor")
            ),
            Column(
                id="volumeDelta",
                title="Volume 24h %",
                sortable=True,
                omit=True,
            ),
            Column(
                id="volume7d",
                title="Volume 7d",
                sortable=True,
                width="150px",
                cell=change_cell(format_currency("$.volume7d", None), "$.volume7dDelta", "$.delta7dColor"),
            ),
            Column(
                id="volume7dDelta",
                title="Volume 7d %",
                sortable=True,
                omit=True,
            ),
            Column(
                id="chart7d",
                title="",
                width="120px",
                cell=__chart_cell('$.chart7d.*')
            ),
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


__discord_members_cell = Div(
    when="$.discord_members",
    children=[
        Row([
            Col("col-auto my-auto", [Icon("cib-discord", size='sm')]),
            Col(
                "col-auto pl-0 my-auto",
                [
                    Span(
                        commify(
                            "$.discord_members"
                        ),
                        "font-small-2 d-block"
                    ),

                ]
            )
        ]),
        Div(
            when="$.change_24h_discord",
            children=[
                Span(
                    "+",
                    format_template("font-small-1 text-{{ color }}", {
                        "color": "$.change_24h_discord_color"
                    }),
                    when="$.discord_plus"
                ),
                Span(
                    commify("$.change_24h_discord"),
                    format_template("font-small-1 text-{{ color }}", {
                        "color": "$.change_24h_discord_color"
                    })
                ),
                Span(
                    format_template(" ( {{ pc }} )", {"pc": format_percent(
                        "$.change_24h_pc_discord", showPlus=True, decimals=2)}),
                    format_template("font-small-1 text-{{ color }}", {
                        "color": "$.change_24h_discord_color"
                    })
                ),
            ]),
    ])

__twitter_followers_cell = Div(
    children=[
        Row([
            Col("col-auto my-auto", [Icon("cib-twitter", size='sm')]),
            Col(
                "col-auto pl-0 my-auto",
                [
                    Span(
                        commify(
                            "$.twitter_followers"
                        ),
                        "font-small-2 d-block"
                    ),

                ]
            )
        ]),
        Div(
            when="$.change_24h",
            children=[
                Span(
                    "+",
                    format_template("font-small-1 text-{{ color }}", {
                        "color": "$.change_24h_color"
                    }),
                    when="$.twitter_plus"
                ),
                Span(
                    commify("$.change_24h"),
                    format_template("font-small-1 text-{{ color }}", {
                        "color": "$.change_24h_color"
                    })
                ),
                Span(
                    format_template(" ( {{ pc }} )", {"pc": format_percent(
                        "$.change_24h_pc", showPlus=True, decimals=2)}),
                    format_template("font-small-1 text-{{ color }}", {
                        "color": "$.change_24h_color"
                    })
                ),
            ]),

    ])
