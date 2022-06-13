from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Icon, Image, Link, Paragraphs, Row, Span, commify,
                        ekp_map, format_currency, format_mask_address,
                        format_percent, format_template, is_busy, json_array,
                        navigate, sort_by, switch_case)


def change_cell(value, delta, deltaColor, icon=None):
    cols = []

    if icon is not None:
        cols.append(
            Col(
                "col-auto pr-0",
                [
                    Icon(icon)
                ]
            )
        )
    cols.append(
        Col(
            "col-auto pr-0",
            [
                Span(
                    value,
                    format_template("font-medium-1 d-block text-{{ color }}", {
                        "color": "normal"
                    })
                ),

            ]
        )
    )
    return Div(
        class_name="mt-2",
        children=[
            Row(cols),
            Div(
                when=delta,
                children=[

                    Span(
                        format_percent(
                            delta,
                            showPlus=True,
                        ),
                        format_template("font-small-2 text-{{ color }}", {
                            "color": deltaColor
                        })
                    ),
                ]),

        ])


CHAIN_IMAGE = {
    "bsc": "https://cryptologos.cc/logos/history/bnb-bnb-logo.svg?v=001",
    "eth": "https://cryptologos.cc/logos/ethereum-eth-logo.svg?v=022",
    "polygon": "https://cryptologos.cc/logos/polygon-matic-logo.svg?v=022",
}


def chain_image(index, height):
    return Image(
        when=f"$.chains[{index}]",
        src=switch_case(f"$.chains[{index}]", CHAIN_IMAGE),
        style={"height": height, "marginRight": "12px", "marginTop": "-2px"}
    )


def name_cell(name):
    return Div(
        children=[
            Div(style={"height": "24px"}),
            Link(
                href=format_template("/game/all/info/{{ id }}", {
                    "id": "$.id"
                }),
                content=name,
                class_name="font-medium-2 d-block"
            ),
            Div(
                style={"marginTop": "0px",
                       "paddingLeft": "0px"},
                children=[
                    chain_image(0, "14px"),
                    chain_image(1, "14px"),
                    chain_image(2, "14px"),

                ]
            ),
            Div(style={"height": "8px"}),
        ])


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


__links_cell = Row(
    class_name="ml-0",
    children=[
        __icon_link_col("$.website", "cil-globe-alt"),
        __icon_link_col("$.twitter", "cib-twitter"),
        __icon_link_col("$.discord", "cib-discord"),
        __icon_link_col("$.telegram", "cib-telegram"),
    ])
