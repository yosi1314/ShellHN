from pytest_mock import MockerFixture
from app.shell.runner import run, style, questions


def test_run(mocker: MockerFixture, mock_items):
    get_top_rated_articles_mock = mocker.patch(
        "app.shell.runner.get_top_rated_articles", return_value=mock_items)
    prompt_mock = mocker.patch("app.shell.runner.prompt", return_value="2")
    validate_user_input_mock = mocker.patch(
        "app.shell.runner.validate_user_input", return_value=2)
    get_article_comments_mock = mocker.patch(
        "app.shell.runner.get_article_comments")

    run()

    get_top_rated_articles_mock.assert_called_once()
    prompt_mock.assert_called_once_with(questions, style=style)
    validate_user_input_mock.assert_called_once()
    get_article_comments_mock.assert_called_once()

