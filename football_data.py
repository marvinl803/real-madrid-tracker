import requests


class FootballDataClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.football-data.org/v2"

    def get_matches(self, team_id):
        url = f"{self.base_url}/teams/{team_id}/matches"
        headers = {"X-Auth-Token": self.api_key}
        response = requests.get(url, headers=headers)
        data = response.json()
        return data["matches"]
