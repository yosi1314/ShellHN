from concurrent.futures import ThreadPoolExecutor
from typing import List, Callable, Dict
from apis.hackernews import get_item_by_id
from models.item import Item
from json import loads
from requests.models import Response
from textwrap import TextWrapper
from models.item_tree_node import ItemTreeNode
import numpy as np



def fetch_multiple_data(ids: List, fetch_data: Callable) -> List[Response]:
    with ThreadPoolExecutor(max_workers=10) as pool:
        response_list = list(pool.map(fetch_data, ids))

    return response_list


def parse_item(res: dict) -> Item:
    return Item.parse_obj(res)


def get_all_item_kids(item: Item, comments: Dict[int, ItemTreeNode], depth: int):
    if not item.kids:
        return
    responses = fetch_multiple_data(item.kids, get_item_by_id)
    for res in responses:
        story = parse_item(res)
        comments[story.id] = ItemTreeNode(item=story, depth=depth)
        get_all_item_kids(story, comments, depth + 1)


def print_all_item_kids(item: Item, comments: Dict[int, ItemTreeNode]):
    prefix = "      "
    if not item.kids:
        return
    for kid in item.kids:
        comment = comments[kid]
        if comment.item.deleted:
            continue
        wrapper = TextWrapper(initial_indent=prefix*comment.depth +
                              "- ", subsequent_indent=prefix*comment.depth + "  ")
        print(wrapper.fill(comment.item.text))
        print_all_item_kids(comment.item, comments)


def get_direct_children(item: Item, comments: Dict[int, ItemTreeNode], depth):
    if not item.kids:
        return
    responses = fetch_multiple_data(item.kids, get_item_by_id)
    for res in responses:
        story = parse_item(res)
        comments[story.id] = ItemTreeNode(item=story, depth=depth)


def gen_correlation_plot(items: List[Item]):
    mat = gen_time_comment_matrix(items)

    bla = 0

def gen_time_comment_matrix(items: List[Item]):
    return [(item.time, item.descendants) for item in items]


