import pytest

from p2tg import P2TG

TOKEN = "299946604:AAFrOtdjPctLoR7HxSY0ailtqxHP9UCMtbc"
CHAT_ID = 116509348
SAMPLE_MESSAGE = "Text_{}"


@pytest.fixture
def logger():
    return P2TG(TOKEN, CHAT_ID, also_print=False)


def test_ctx_send_messages(logger):
    logger_send = logger.msg_send
    with logger_send:
        for i in range(2):
            print(SAMPLE_MESSAGE.format(i))
    _compare_strings(logger_send)


def test_decorator_send_messages(logger):
    logger_send = logger.msg_send

    @logger_send
    def sample_func(x):
        for i in range(2):
            print(x.format(i))

    sample_func(SAMPLE_MESSAGE)
    _compare_strings(logger_send)


def test_ctx_update_messages(logger):
    logger_upd = logger.msg_update
    with logger_upd:
        for i in range(2):
            print(SAMPLE_MESSAGE.format(i))
    _compare_strings(logger_upd)


def test_decorator_update_messages(logger):
    logger_upd = logger.msg_update

    @logger_upd
    def sample_func(x):
        for i in range(2):
            print(x.format(i))

    sample_func(SAMPLE_MESSAGE)
    _compare_strings(logger_upd)


def _compare_strings(logger):
    assert all(
        SAMPLE_MESSAGE.format(i) == res["result"]["text"]
        for res, i in zip(logger.request_results, range(2)))
