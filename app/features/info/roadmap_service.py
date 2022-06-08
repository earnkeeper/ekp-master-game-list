from db.roadmap_event_repo import RoadmapEventRepo


class RoadmapService:
    def __init__(
        self,
        roadmap_event_repo: RoadmapEventRepo,
    ):
        self.roadmap_event_repo = roadmap_event_repo

    def get_roadmaps_document(self, game):
        events = self.roadmap_event_repo.find_by_game_id(game["id"])
        
        grouped_by_phase = {}
        
        for event in events:
            phase = event["phase"];
            if phase not in grouped_by_phase:
                grouped_by_phase[phase] = {
                    "timestamp": phase["timestamp"],
                    "title": phase,
                    "items": []
                }
                
                grouped_by_phase[phase]["items"].append(event["event"])
        
        events = sorted(
            grouped_by_phase.values(),
            key=lambda x: x["timestamp"]
        )
        
        roadmap_document = {
            "officialLink": None,
            "events": events
        }
        
        return roadmap_document
