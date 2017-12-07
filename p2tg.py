from __future__ import print_function

import enum
import os
import sys
from io import TextIOWrapper
import json

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError
    from urllib2 import urlopen
    from urllib import urlencode


TG_URI_SEND_MSG = 'https://api.telegram.org/bot{token}/sendMessage'
TG_URI_UPDATE_MSG = 'https://api.telegram.org/bot{token}/editMessageText'


class Reader:

    def __init__(self, tg_token: str, chat_id: int,
                 also_print: bool, old_stdout: TextIOWrapper,
                 is_msg_update: bool):
        self.uri_send = TG_URI_SEND_MSG.format(token=tg_token)
        self.uri_update = TG_URI_UPDATE_MSG.format(token=tg_token)
        self.old_stdout = old_stdout
        self.chat_id = chat_id
        self.is_msg_update = is_msg_update
        self.also_print = also_print
        self._last_message_id = None

        self._lines = []
        self.request_results = []

    def write(self, data: str):
        self._lines.append(data)
        if self._lines[-1] == '\n':
            line = ''.join(self._lines)
            if self.also_print:
                print(line, file=self.old_stdout, end='')

            if self.is_msg_update:
                if not self._last_message_id:
                    response = self.send_message(line)
                else:
                    response = self.update_last_message(line)
            else:
                response = self.send_message(line)
            self._lines = []
            self.request_results.append(response)

    def send_message(self, data: str):
        args = {
            'chat_id': self.chat_id,
            'text': data,
        }
        args = urlencode(args).encode("utf-8")
        try:
            resp = urlopen(self.uri_send, args)
            resp = json.loads(resp.read().decode("utf-8"))
            self._last_message_id = resp['result']['message_id']
            return resp
        except URLError:
            pass


    def update_last_message(self, data: str):
        args = {
            'chat_id': self.chat_id,
            'text': data,
            'message_id': self._last_message_id
        }
        args = urlencode(args).encode("utf-8")
        try:
            resp = urlopen(self.uri_update, args)
            resp = json.loads(resp.read().decode("utf-8"))
            return resp
        except URLError:
            pass


class _P2TG:

    def __init__(self, tg_token: str, chat_id: int,
                 also_print: bool, msg_update: bool=False):
        self.old_stdout = sys.stdout

        self._fixed_stdout = Reader(tg_token, chat_id,
                                    also_print, self.old_stdout, msg_update)

    @property
    def request_results(self):
        return self._fixed_stdout.request_results

    def __enter__(self):
        sys.stdout = self._fixed_stdout

    def __exit__(self, *args):
        sys.stdout = self.old_stdout

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            with self:
                result = function(*args, **kwargs)
            return result

        return wrapper


class P2TG:

    def __init__(self, tg_token: str=None, chat_id: int=None,
                 also_print: bool=False):
        if not tg_token:
            tg_token = os.getenv('TG_API_TOKEN', None)
        if not chat_id:
            chat_id = os.getenv('TG_CHAT_ID', None)

        if not tg_token or not chat_id:
            raise ValueError("Find `None` values `tg_token` or `chat_id`")

        self.tg_token = tg_token
        self.chat_id = int(chat_id)
        self.also_print = also_print

    @property
    def messages_update(self):
        return _P2TG(self.tg_token, self.chat_id, self.also_print,
                     msg_update=True)

    @property
    def messages_send(self):
        return _P2TG(self.tg_token, self.chat_id, self.also_print)
