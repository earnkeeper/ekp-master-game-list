from app.features.stats.shared import change_cell, name_cell
from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Icon, Image, Link, Paragraphs, Row, Span, commify,
                        ekp_map, format_currency, format_mask_address,
                        format_percent, format_template, is_busy, json_array,
                        navigate, sort_by, switch_case)
from ekp_sdk.util import collection, documents


def volume_tab(COLLECTION_NAME):
    return Container(
        children=[
            Paragraphs([
                "Active tokens indicate an active economy, checking token volume rather than token price gives you better insight.",
            ]),
            __table_row(COLLECTION_NAME)
        ]
    )


def __table_row(COLLECTION_NAME):
    return Datatable(
        class_name="mt-1",
        data=documents(COLLECTION_NAME),
        busy_when=is_busy(collection(COLLECTION_NAME)),
        default_sort_field_id="volume24h",
        default_sort_asc=False,
        show_last_updated=False,
        row_height="70px",
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
                min_width="400px",
                sortable=True,
                searchable=True,
                cell=name_cell("$.gameName")
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
                            ['$.timestamp_ms', '$.volume'],
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


