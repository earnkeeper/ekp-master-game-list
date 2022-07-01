from ekp_sdk.ui import (Button, Card, Chart, Col, Column, Container, Datatable,
                        Div, Icon, Image, Link, Paragraphs, Row, Span, commify,
                        ekp_map, format_currency, format_mask_address,
                        format_percent, format_template, is_busy, json_array,
                        navigate, sort_by, switch_case)


def change_cell(value, delta, deltaColor, icon=None):
    return Div(
        class_name="text-right",
        children=[
            Span(
                value,
                format_template("font-small-3 d-block text-{{ color }}", {
                    "color": "normal"
                })
            ),
            Span(
                format_percent(
                    delta,
                    showPlus=True,
                ),
                format_template("font-small-1 text-{{ color }}", {
                    "color": deltaColor
                }),
                when=delta
            ),
        ])


def social_followers(value, delta_24h, delta_color_24h, plus, delta_24h_pc):
    return Div(
        when=value,
        children=[
            Div(
                class_name="text-right",
                when=delta_24h,
                children=[
                    Span(
                        commify(
                            value
                        ),
                        "font-small-3 d-block"
                    ),
                    Span(
                        "+",
                        format_template("font-small-1 text-{{ color }}", {
                            "color": delta_color_24h
                        }),
                        when=plus
                    ),
                    Span(
                        commify(delta_24h),
                        format_template("font-small-1 text-{{ color }}", {
                            "color": delta_color_24h
                        })
                    ),
                    Span(
                        format_template(" ( {{ pc }} )", {"pc": format_percent(
                            delta_24h_pc, showPlus=True, decimals=2)}),
                        format_template("font-small-1 text-{{ color }}", {
                            "color": delta_color_24h
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
    return Row(
        children=[
            Col(
                "col-auto pr-0 my-auto",
                [
                    Image(
                        when="$.profile_image_url",
                        src="$.profile_image_url",
                        style={
                            "height": "24px",
                            "width": "24px",
                        },
                        rounded=True)
                ]
            ),
            Col(
                "col-auto pr-0 my-auto",
                [
                    Image(
                        when={"not": "$.profile_image_url"},
                        src="https://earnkeeper.io/logos/earnkeeper_logo.png",
                        style={
                            "height": "24px",
                            "width": "24px",
                        },
                        rounded=True)
                ]
            ),
            Col(
                "my-auto",
                [
                    Link(
                        href=format_template("/game/all/info/{{ id }}", {
                            "id": "$.id"
                        }),
                        content=name,
                        class_name="d-block",
                        external_icon=True
                    ),
                    Div(
                        style={"marginTop": "-4px",
                               "paddingLeft": "0px"},
                        children=[
                            chain_image(0, "10px"),
                            chain_image(1, "10px"),
                            chain_image(2, "10px"),
                        ]
                    ),
                ]
            ),
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
