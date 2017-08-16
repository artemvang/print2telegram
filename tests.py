import pytest

from p2tg import P2TG

TOKEN = "299946604:AAFrOtdjPctLoR7HxSY0ailtqxHP9UCMtbc"
CHAT_ID = 116509348
SAMPLE_MESSAGE = "Text_{}"


@pytest.fixture
def logger():
    return P2TG(TOKEN, CHAT_ID, also_print=False)


def test_posting_context(logger):
    with logger:
        for i in range(2):
            print(SAMPLE_MESSAGE.format(i))
    compare_strings(logger)


def test_posting_decorator(logger):
    @logger
    def sample_func(x):
        for i in range(2):
            print(x.format(i))

    sample_func(SAMPLE_MESSAGE)
    compare_strings(logger)

def compare_strings(logger):
    assert all(
        SAMPLE_MESSAGE.format(i) == res["result"]["text"]
        for res, i in zip(logger.request_results, range(2)))
