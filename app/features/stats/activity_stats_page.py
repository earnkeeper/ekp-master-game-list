from app.features.stats.shared import name_cell, change_cell, social_followers
from app.utils.page_title import page_title
from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Icon, Image, Link, Paragraphs, Row, Span, commify,
                        ekp_map, format_currency, format_mask_address,
                        format_percent, format_template, is_busy, json_array,
                        navigate, sort_by, switch_case)
from ekp_sdk.util import collection, documents


def activity_tab(COLLECTION_NAME, VOLUME_CHART_COLLECTION_NAME):
    return Container(
        children=[
            page_title("activity", "Games"),
            __volume_chart(VOLUME_CHART_COLLECTION_NAME),
            __table_row(COLLECTION_NAME)
        ]
    )

# def __volume_card(VOLUME_CHART_COLLECTION_NAME):
#     return Div(
#         context=f"{VOLUME_CHART_COLLECTION_NAME}",
#         children=[
#             Card(
#                 children=[
#                     __volume_chart(VOLUME_CHART_COLLECTION_NAME),
#                 ]
#             )
#         ]
#     )

def __volume_chart(VOLUME_CHART_COLLECTION_NAME):
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
                data=f"$.{VOLUME_CHART_COLLECTION_NAME}.*",
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
                                f"$.{VOLUME_CHART_COLLECTION_NAME}.*"
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
                                json_array(f"$.{VOLUME_CHART_COLLECTION_NAME}.*"),
                                "$.timestamp_ms"
                            ),
                            "$.volume"
                        ),
                    },
                ],
            )
        ]
    )

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
                id="price24h",
                title="Price",
                sortable=True,
                width="150px",
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