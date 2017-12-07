import pytest

from p2tg import P2TG

TOKEN = "299946604:AAFrOtdjPctLoR7HxSY0ailtqxHP9UCMtbc"
CHAT_ID = 116509348
SAMPLE_MESSAGE = "Text_{}"


@pytest.fixture
def logger():
    return P2TG(TOKEN, CHAT_ID, also_print=False)


def test_ctx_send_messages(logger):
    loggr = logger.messages_send
    with loggr:
        for i in range(2):
            print(SAMPLE_MESSAGE.format(i))
    compare_strings(loggr)


def test_decorator_send_messages(logger):
    loggr = logger.messages_send
    @loggr
    def sample_func(x):
        for i in range(2):
            print(x.format(i))

    sample_func(SAMPLE_MESSAGE)
    compare_strings(loggr)


def test_ctx_update_messages(logger):
    loggr = logger.messages_update
    with loggr:
        for i in range(2):
            print(SAMPLE_MESSAGE.format(i))
    compare_strings(loggr)


def test_decorator_update_messages(logger):
    loggr = logger.messages_update
    @loggr
    def sample_func(x):
        for i in range(2):
            print(x.format(i))

    sample_func(SAMPLE_MESSAGE)
    compare_strings(loggr)


def compare_strings(logger):
    assert all(
        SAMPLE_MESSAGE.format(i) == res["result"]["text"]
        for res, i in zip(logger.request_results, range(2)))
