# print2telegram

[![build status](https://travis-ci.org/vangaa/print2telegram.svg)](https://travis-ci.org/vangaa/print2telegram) [![PyPI version](https://badge.fury.io/py/p2tg.svg)](https://badge.fury.io/py/p2tg)

Library just redirects stdout stream contents to telegram chat line by line.

# Installation

```bash
pip install p2tg
```

# Usage
### Logger setup:
```python
from p2tg import P2TG

logger = P2TG("telegram bot token", 1337)
```

Or you can set logger parameters via environment variables:
```
export TG_CHAT_ID="chat_id"
export TG_API_TOKEN="api_token"
```

And then:
```python
from p2tg import P2TG
# Or
from p2tg import tg_send, tg_update

logger = P2TG()
```

### Use as context manager:
```python
with logger.messages_send: # just send message
# or with tg_send:
    print('Text1') # first message
    print('Text2') # second message
    
with logger.messages_update: # send message and update him in next print calls
# or with tg_update:
    print('Text1') # first message
    print('Text2') # update for first message
```

### And as decorator:
```python
@logger.messages_send
def amazing_function():
    print('Text')
```

## Result:
![result](result.png?raw=true "Result")

### Log to both stdout and telegram bot
```python
logger = P2TG("telegram bot token", 1337, also_print=True)
```

Original idea from [this repo](https://github.com/laike9m/f)
