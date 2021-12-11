import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Callable, Dict
from app.apis.hackernews import get_best_stories_ids, get_item_by_id
from app.models.item import Item
from requests.models import Response
from textwrap import TextWrapper
from app.models.item_tree_node import ItemTreeNode
from app.consts import hm_utils_consts as hm


def fetch_multiple_data(ids: List, fetch_data: Callable) -> List[Response]:
    with ThreadPoolExecutor(max_workers=10) as pool:
        response_list = list(pool.map(fetch_data, ids))

    return response_list


def parse_item(res: dict) -> Item:
    if res:
        return Item.parse_obj(res)


def get_top_rated_articles() -> List[Item]:
    print(hm.LOADING_ARTICLES_MSG)
    logging.info(hm.LOADING_ARTICLES_LOG)

    ids: List[int] = _fetch_story_ids()
    items: List[Item] = _fetch_stories_data(ids)

    logging.info(hm.DONE_FETCHING_ARTICLES)
    return items


def _fetch_story_ids() -> List[int]:
    ids: List[int] = get_best_stories_ids(hm.DEFAULT_LIMIT)
    if not ids:
        logging.exception(hm.GENERAL_EXCEPTION_MSG)
        raise SystemExit(
            hm.FAILED_LOADING_ARTICLES_LOG)
    return ids


def _fetch_stories_data(ids) -> List[Item]:
    responses = fetch_multiple_data(ids, get_item_by_id)
    items: List[Item] = []
    for index, res in enumerate(responses):
        story = parse_item(res)
        if story:
            items.append(story)
            print(f"{index + 1}. {story.title} | Comments: {story.descendants}")

    if not len(items):
        logging.exception(hm.GENERAL_EXCEPTION_MSG)
        raise SystemExit(
            hm.FAILED_LOADING_ARTICLES_MSG)

    return items


def get_article_comments(story: Item):
    comments: Dict[int, ItemTreeNode] = {}

    logging.info(f"Fetching story {story.id} comments.")
    print(hm.LOADING_COMMENTS_MSG)

    _save_all_item_kids(story, comments, 0)
    if not comments:
        logging.exception(hm.GENERAL_EXCEPTION_MSG)
        raise SystemExit(
            hm.FAILED_LOADING_COMMENTS_MSG)

    print(f'Displaying "{story.title}" comments:')

    _print_all_item_kids(story, comments)
    logging.info(f"Done fetching story {story.id} comments.")


def _save_all_item_kids(item: Item, comments: Dict[int, ItemTreeNode], depth: int):
    if not item.kids:
        return
    responses = fetch_multiple_data(item.kids, get_item_by_id)
    for res in responses:
        if not res:
            continue
        story = parse_item(res)
        comments[story.id] = ItemTreeNode(item=story, depth=depth)
        _save_all_item_kids(story, comments, depth + 1)


def _print_all_item_kids(item: Item, comments: Dict[int, ItemTreeNode]):
    prefix = hm.LINE_PREFIX
    if not item.kids:
        return
    for kid in item.kids:
        comment = comments[kid]
        if comment.item.deleted:
            continue
        wrapper = TextWrapper(initial_indent=prefix*comment.depth +
                              hm.BEGIN_LINE_PREFIX,
                              subsequent_indent=prefix*comment.depth +
                              hm.END_LINE_PREFIX)
        print(wrapper.fill(comment.item.text))
        _print_all_item_kids(comment.item, comments)
