from __future__ import print_function

import sys
import json

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import urlopen
    from urllib import urlencode

TG_URI = 'https://api.telegram.org/bot{token}/sendMessage'


class Reader(object):
    def __init__(self, tg_token, chat_id, also_print):
        self.uri = TG_URI.format(token=tg_token)
        self.chat_id = chat_id
        self.also_print = also_print

        self.__lines = []
        self.request_results = []

    def write(self, data):
        self.__lines.append(data)
        if self.__lines[-1] == '\n':
            line = ''.join(self.__lines)
            if self.also_print:
                print(line, file=sys.__stdout__, end='')
            self.send_message(line)
            self.lines = []

    def send_message(self, data):
        args = {
            'chat_id': self.chat_id,
            'text': data,
        }
        args = urlencode(args).encode("utf-8")
        data = urlopen(self.uri, args)
        data = json.loads(data.read().decode("utf-8"))
        self.request_results.append(data)


class P2TG(object):
    def __init__(self, tg_token, chat_id, also_print=True):
        self.__fixed_stdout = Reader(tg_token, chat_id, also_print)

    @property
    def request_results(self):
        return self.__fixed_stdout.request_results

    def __enter__(self):
        sys.stdout = self.__fixed_stdout

    def __exit__(self, *args):
        sys.stdout = sys.__stdout__

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            with self:
                result = function(*args, **kwargs)
            return result

        return wrapper
