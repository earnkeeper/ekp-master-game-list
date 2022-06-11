from ekp_sdk.ui import (Container, Tabs)

from app.features.stats.activity_tab import activity_tab
from app.features.stats.social_tab import social_tab
from app.features.stats.volume_tab import volume_tab

def stats_page(ACTIVITY_COLLECTION_NAME, VOLUME_COLLECTION_NAME, SOCIAL_TABLE_COLLECTION_NAME):
    return Container(
        children=[
            Tabs(
                children=[
                    {
                        "label": "Social Activity",
                        "children": [social_tab(SOCIAL_TABLE_COLLECTION_NAME)]
                    },
                    {
                        "label": "User Activity",
                        "children": [activity_tab(ACTIVITY_COLLECTION_NAME)]
                    },
                    {
                        "label": "Token Volume",
                        "children": [volume_tab(VOLUME_COLLECTION_NAME)]
                    }
                ]
            )
        ]
    )

