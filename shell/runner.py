from PyInquirer import style_from_dict, Token, prompt, Separator
from typing import List, Dict
from apis.hackernews import get_best_stories, get_item_by_id
from models.item import Item
from models.item_tree_node import ItemTreeNode
from utils.hackernews import parse_item,fetch_multiple_data, get_all_item_kids, print_all_item_kids, gen_correlation_plot

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

questions = [
    {
        "type": "input",
        "name": "selected_article",
        "message": "Choose an article rank to view its comments: "
    }
]

def run():
    ids = get_best_stories(40)

    responses = fetch_multiple_data(ids, get_item_by_id)
    items: List[Item] = []
    for index, res in enumerate(responses):
        story = parse_item(res)
        if story:
            items.append(story)
            print(f"{index + 1}. {story.title} | Comments: {story.descendants}")

    answers = prompt(questions, style=style)
    selected_article = int(answers["selected_article"])

    story = parse_item(get_item_by_id(items[selected_article - 1].id))
    comments: Dict[int, ItemTreeNode] = {}
    get_all_item_kids(story, comments, 0)
    print_all_item_kids(story, comments)

    gen_correlation_plot(items)
    bla = 0
