from typing import List
from requests import get
from json import loads

from requests.models import Response

BASE_URL = "https://hacker-news.firebaseio.com/v0"

def get_best_stories(limit: int) -> List[int]:
    params = {
        "limitToFirst": limit,
        "orderBy": '"$key"'
    }
    
    data = get(url=f"{BASE_URL}/beststories.json", params=params)
    if data.status_code != 200:
        #log
        pass
    return loads(data.content)


def get_item_by_id(id: int) -> Response:
    data = get(url=f"{BASE_URL}/item/{id}.json")
    if data.status_code != 200:
        #log
        pass
    return loads(data.content)

