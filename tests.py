import pytest

from p2tg import P2TG

TOKEN = "299946604:AAFrOtdjPctLoR7HxSY0ailtqxHP9UCMtbc"
CHAT_ID = 116509348
SAMPLE_MESSAGE = "Text"

@pytest.fixture
def logger():
    return P2TG(TOKEN, CHAT_ID, also_print=False)


def test_posting_context(logger):
    with logger:
        print(SAMPLE_MESSAGE)
    assert logger.request_results[-1]["result"]["text"] == SAMPLE_MESSAGE


def test_posting_decorator(logger):
    @logger
    def sample_func(x):
        print(x + "+++")

    sample_func(SAMPLE_MESSAGE)
    assert logger.request_results[-1]["result"]["text"] == SAMPLE_MESSAGE + "+++"
