from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Icon, Image, Link, Paragraphs, Row, Span, commify,
                        ekp_map, format_currency, format_mask_address,
                        format_percent, format_template, is_busy, json_array,
                        navigate, sort_by, switch_case)
from ekp_sdk.util import collection, documents


def social_tab(COLLECTION_NAME):
    return Container(
        children=[
            Paragraphs([
                "Gamefi projects rely on a steady stream of new users to keep a healthy economy.",
                "Use this list to watch changes in the social following of games."
            ]),
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
        show_last_updated=False,
        row_height="70px",
        columns=[
            Column(
                id="game_name",
                title="Game",
                cell=__name_cell,
                compact=True,
                searchable=True,
                sortable=True,
                min_width="220px"
            ),
            Column(
                id="twitter_followers",
                title="Followers",
                sortable=True,
                width="160px",
                cell=__twitter_followers_cell
            ),
            Column(
                id="chart",
                title="",
                width="120px",
                cell=__chart_cell('$.chart.*')
            ),
            Column(
                id="change_24h",
                title="New Followers",
                sortable=True,
                omit=True
            ),
            Column(
                id="change_24h_pc",
                title="New Followers %",
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
                            ['$.timestamp_ms', '$.value'],
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


CHAIN_IMAGE = {
    "bsc": "https://cryptologos.cc/logos/history/bnb-bnb-logo.svg?v=001",
    "eth": "https://cryptologos.cc/logos/ethereum-eth-logo.svg?v=022",
    "polygon": "https://cryptologos.cc/logos/polygon-matic-logo.svg?v=022",
}


def __icon_link_col(href, icon_name):
    return Col(
        "col-auto my-auto px-0",
        [
            Div(
                when=href,
                class_name="mr-1",
                children=[
                    Link(
                        href=href,
                        external=True,
                        content=Icon(
                            icon_name,
                            size='sm'
                        )
                    )
                ]
            )
        ]
    )


def __chain_image(index, height="14px"):
    return Image(
        when=f"$.chains[{index}]",
        src=switch_case(f"$.chains[{index}]", CHAIN_IMAGE),
        style={"height": height, "marginRight": "12px", "marginTop": "-2px"}
    )


__twitter_followers_cell = Div(
    class_name="mt-2",
    children=[
        Row([
            Col("col-auto my-auto", [Icon("cib-twitter")]),
            Col(
                "col-auto pl-0 my-auto",
                [
                    Span(
                        commify(
                            "$.twitter_followers"
                        ),
                        "font-medium-1 d-block"
                    ),

                ]
            )
        ]),
        Div(
            when="$.change_24h",
            children=[
                Span(
                    "+",
                    format_template("font-small-2 text-{{ color }}", {
                        "color": "$.change_24h_color"
                    }),
                    when="$.twitter_plus"
                ),
                Span(
                    commify("$.change_24h"),
                    format_template("font-small-2 text-{{ color }}", {
                        "color": "$.change_24h_color"
                    })
                ),
                Span(
                    format_template(" ( {{ pc }} )", {"pc": format_percent(
                        "$.change_24h_pc", showPlus=True, decimals=2)}),
                    format_template("font-small-2 text-{{ color }}", {
                        "color": "$.change_24h_color"
                    })
                ),
            ]),

    ])

__name_cell = Row(
    children=[
        Col(
            "col-auto pr-0 my-auto",
            [
                Image(src="$.profile_image_url", style={"height": "32px", "width": "32px", "marginTop": "18px"}, rounded=True)
            ]
        ),
        Col(
            "",
            [
                Div(style={"height": "24px"}),
                Link(
                    href=format_template("/game/all/info/{{ id }}", {
                        "id": "$.id"
                    }),
                    content="$.game_name",
                    class_name="font-medium-2 d-block"
                ),
                Div(
                    style={"marginTop": "0px",
                           "paddingLeft": "0px"},
                    children=[
                        __chain_image(0, "14px"),
                        __chain_image(1, "14px"),
                        __chain_image(2, "14px"),

                    ]
                ),
                Div(style={"height": "8px"}),

            ]
        )
    ])
