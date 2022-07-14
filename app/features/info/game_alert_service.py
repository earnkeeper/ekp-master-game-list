from pprint import pprint

from db.alert_config_repo import AlertConfigRepo


class GameAlertService:
    def __init__(
            self,
            alert_config_repo: AlertConfigRepo
    ):
        self.alert_config_repo = alert_config_repo

    def save_alert(self, alert_form_values):
        # pprint(alert_form_values)

        document = {
            "id": alert_form_values['id'],
            "created": alert_form_values['created'],
            "updated": alert_form_values['updated'],
            "discord_id": alert_form_values['discord_id'],
            "type": alert_form_values['type']
        }

        if alert_form_values['type'] == 'priceChange':
            document['min_volume'] = alert_form_values['min_volume']
            document['pc_change'] = alert_form_values['pc_change']
        elif alert_form_values['type'] == 'priceChange':
            document['min_new_users'] = alert_form_values['min_new_users']
            document['pc_change'] = alert_form_values['pc_change']

        self.alert_config_repo.save([document])

        return []
