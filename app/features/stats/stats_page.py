from ekp_sdk.ui import (Container, Tabs)

from app.features.stats.activity_tab import activity_tab

def stats_page(ACTIVITY_COLLECTION_NAME):
    return Container(
        children=[
            Tabs(
                children=[
                    {
                        "label": "User Activity",
                        "children": [activity_tab(ACTIVITY_COLLECTION_NAME)]
                    },
                    {
                        "label": "Token Volume",
                        "children": []
                    }
                ]
            )
        ]
    )

