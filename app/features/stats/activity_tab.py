from app.features.stats.shared import change_cell, name_cell
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
        default_sort_field_id="newUsers24h",
        default_sort_asc=False,
        row_height="70px",
        show_last_updated=False,
        columns=[
            Column(
                id="gameName",
                title="Game",
                min_width="400px",
                sortable=True,
                searchable=True,
                cell=name_cell("$.gameName")
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
                id="newUsersDelta",
                title="New Users 24h %",
                sortable=True,
                omit=True,
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
