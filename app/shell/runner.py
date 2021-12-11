from PyInquirer import style_from_dict, Token, prompt
from app.apis.hackernews import get_item_by_id
from app.utils.hackernews import get_top_rated_articles, get_article_comments, parse_item

from app.validators.shell_validator import validate_user_input

from app.consts import cmd_consts


style = style_from_dict({
    Token.QuestionMark: cmd_consts.TOKEN_QUESTION_MARK,
    Token.Answer: cmd_consts.TOKEN_ANSWER,
    Token.Question: cmd_consts.TOKEN_QUESTION,
})

questions = [
    {
        "type": cmd_consts.QUESTION_TYPE_INPUT,
        "name": cmd_consts.SELECTED_ARTICLE,
        "message": cmd_consts.QUESTION_SELECT_ARTICLE_MSG
    }
]


def run():
    items = get_top_rated_articles()

    answers = prompt(questions, style=style)
    selected_article = validate_user_input(
        answers, cmd_consts.SELECTED_ARTICLE, prompt, questions, style=style)

    story = items[selected_article - 1]

    get_article_comments(story)
