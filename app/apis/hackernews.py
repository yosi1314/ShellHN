from typing import List
from requests import get
from requests.models import Response
from app.consts.hm_api_consts import BASE_URL

from app.decorators.api_wrapper import parse_api_call


@parse_api_call
def get_best_stories_ids(limit: int) -> List[int]:
    url = f"{BASE_URL}/beststories.json"
    params = {
        "limitToFirst": limit,
        "orderBy": '"$key"'
    }

    return get(url=url, params=params)


@parse_api_call
def get_item_by_id(id: int) -> Response:
    url = f"{BASE_URL}/item/{id}.json"

    return get(url=url)
