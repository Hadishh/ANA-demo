from config.settings.base import MPT_URL
import requests
class MPT:
    def __init__(self) -> None:
        pass

    def query(self, query, conversation=[]):
        response = requests.post(MPT_URL, json={"query": query, "conversation": conversation})
        return response.json()["response"]