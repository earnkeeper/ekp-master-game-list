from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Icon, Image, Link, Paragraphs, Row, Span, commify,
                        ekp_map, format_currency, format_mask_address,
                        format_percent, format_template, is_busy, json_array,
                        navigate, sort_by, switch_case)
from ekp_sdk.util import collection, documents


def activity_tab(ACTIVITY_COLLECTION_NAME):
    return Container(
        children=[
            Paragraphs([
                "Gamefi projects rely on a steady stream of new users to keep a healthy economy.",
                "Use this list to find the games with most number of new users today, and the highest increase in new users."
            ]),
            __table_row(ACTIVITY_COLLECTION_NAME)
        ]
    )


def __table_row(ACTIVITY_COLLECTION_NAME):
    return Datatable(
        class_name="mt-1",
        data=documents(ACTIVITY_COLLECTION_NAME),
        busy_when=is_busy(collection(ACTIVITY_COLLECTION_NAME)),
        default_sort_field_id="newUsersDelta",
        default_sort_asc=False,
        on_row_clicked=navigate(
            format_template("info/{{ id }}", {
                "id": "$.gameId"
            })
        ),
        columns=[
            Column(
                id="chains",
                searchable=True,
                width="120px",
                omit=True,
            ),
            Column(
                id="gameName",
                title="Game",
                min_width="300px",
                sortable=True,
                searchable=True,
                cell=__name_cell
            ),
            Column(
                id="newUsers24h",
                title="New Users 24h",
                sortable=True,
                width="120px",
                format=commify("$.newUsers24h")
            ),
            Column(
                id="newUsersDelta",
                title="Change 24h",
                sortable=True,
                width="120px",
                cell=Span(
                    format_percent("$.newUsersDelta", True),
                    format_template("text-{{ color }}", {
                        "color": "$.deltaColor"
                    })
                )
            ),
            Column(
                id="newUsers7d",
                title="New Users 7d",
                sortable=True,
                format=commify("$.newUsers7d"),
                width="120px"
            ),
            # Column(
            #     id="newUsers14d",
            #     title="New Users 14d",
            #     sortable=True,
            #     format=commify("$.newUsers14d"),
            #     width="120px"
            # ),
            Column(
                id="newUsers7dDelta",
                title="Change 7d",
                sortable=True,
                cell=Span(
                    format_percent("$.newUsers7dDelta", True),
                    format_template("text-{{ color }}", {
                        "color": "$.delta7dColor"
                    })
                ),
                width="100px"
            ),
            Column(
                id="chart7d",
                title="7d History",
                width="120px",
                cell=__chart_cell('$.chart7d.*')
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


def __chain_image(index):
    return Image(
        when=f"$.chains[{index}]",
        src=switch_case(f"$.chains[{index}]", CHAIN_IMAGE),
        style={"height": "12px", "marginLeft": "12px", "marginTop": "-4px"}
    )


__name_cell = Row([

    Col(
        "col-auto my-auto pr-0",
        [
            Div([
                Span("$.gameName", "font-medium-1"),
                __chain_image(0),
                __chain_image(1),
                __chain_image(2),
            ])
        ]
    ),
    Col(
        "col-12",

    ),
    Col(
        "col-12",
        [
            Row(
                class_name="ml-0",
                children=[
                    __icon_link_col("$.website", "cil-globe-alt"),
                    __icon_link_col("$.twitter", "cib-twitter"),
                    __icon_link_col("$.discord", "cib-discord"),
                    __icon_link_col("$.telegram", "cib-telegram"),
                ])
        ]
    )
])
