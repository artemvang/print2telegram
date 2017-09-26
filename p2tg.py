from __future__ import print_function

import os
import sys
import json

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError
    from urllib2 import urlopen
    from urllib import urlencode

TG_URI = 'https://api.telegram.org/bot{token}/sendMessage'


class Reader(object):
    def __init__(self, tg_token, chat_id, also_print, old_stdout):
        self.uri = TG_URI.format(token=tg_token)
        self.old_stdout = old_stdout
        self.chat_id = chat_id
        self.also_print = also_print

        self.__lines = []
        self.request_results = []

    def write(self, data):
        self.__lines.append(data)
        if self.__lines[-1] == '\n':
            line = ''.join(self.__lines)
            if self.also_print:
                print(line, file=self.old_stdout, end='')
            self.send_message(line)
            self.__lines = []

    def send_message(self, data):
        args = {
            'chat_id': self.chat_id,
            'text': data,
        }
        args = urlencode(args).encode("utf-8")
        try:
            data = urlopen(self.uri, args)
            data = json.loads(data.read().decode("utf-8"))
            self.request_results.append(data)
        except URLError:
            pass


class P2TG(object):
    def __init__(self, tg_token=None, chat_id=None, also_print=False):
        self.old_stdout = sys.stdout

        if not tg_token:
            tg_token = os.getenv('TG_API_TOKEN', None)
        if not chat_id:
            chat_id = os.getenv('TG_CHAT_ID', None)

        if not tg_token or not chat_id:
            raise ValueError("Find `None` values `tg_token` or `chat_id`")

        self.__fixed_stdout = Reader(tg_token, int(chat_id), also_print, self.old_stdout)

    @property
    def request_results(self):
        return self.__fixed_stdout.request_results

    def __enter__(self):
        sys.stdout = self.__fixed_stdout

    def __exit__(self, *args):
        sys.stdout = self.old_stdout

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            with self:
                result = function(*args, **kwargs)
            return result

        return wrapper
