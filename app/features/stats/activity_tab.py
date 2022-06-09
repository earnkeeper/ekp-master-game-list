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
        columns=[
            Column(
                id="chain",
                title="",
                sortable=True,
                searchable=True,
                width="38px",
                cell=Div(
                    class_name="text-center",
                    style={"width": "20px"},
                    children=[
                        Image(
                            src=switch_case("$.chain", CHAIN_IMAGE),
                            style={"height": "16px"}
                        )
                    ]
                )

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
                title="New Users (24h)",
                right=True,
                sortable=True,
                format={
                    "method": "commify",
                    "params": ["$.newUsers24h"]
                },
                width="160px"
            ),
            Column(
                id="newUsersDelta",
                title="Change (24h)",
                right=True,
                sortable=True,
                format=format_percent("$.newUsersDelta"),
                width="160px"
            ),
            Column(
                id="newUsers7d",
                title="New Users (7d)",
                right=True,
                sortable=True,
                format={
                    "method": "commify",
                    "params": ["$.newUsers7d"]
                },
                width="160px"
            ),
            Column(
                id="chart7d",
                title="",
                width="180px",
                cell=chart_cell('$.chart7d.*')
            ),
        ]
    )


def chart_cell(path):
    return Chart(
        title="",
        card=False,
        type='line',
        height=90,
        series=[
            {
                "name": 'All',
                "type": "line",
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
            "stroke": {
                "width": 3,
                "curve": "smooth"
            },
            "grid": {
                "show": False,
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


CHAIN_IMAGE = {
    "bsc": "https://cryptologos.cc/logos/history/bnb-bnb-logo.svg?v=001",
    "eth": "https://cryptologos.cc/logos/ethereum-eth-logo.svg?v=022",
    "polygon": "https://cryptologos.cc/logos/polygon-matic-logo.svg?v=022",
}


def __icon_link_col(href, icon_name):
    return Col(
        "col-auto my-auto pl-0",
        [
            Div(
                when=href,
                children=[
                    Link(
                        href=href,
                        external=True,
                        content=Icon(
                            icon_name,
                        )
                    )
                ]
            )
        ]
    )


__name_cell = Row([
    Col(
        "col-auto my-auto",
        [
            Link(
                href=format_template("/game/all/info/{{ id }}", {
                    "id": "$.gameId"
                }),
                content="$.gameName"
            )
        ]
    ),
    __icon_link_col("$.website", "cil-globe-alt"),
    __icon_link_col("$.twitter", "cib-twitter"),
])
