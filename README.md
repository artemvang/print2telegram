# print2telegram

![build status](https://travis-ci.org/vangaa/print2telegram.svg?branch=master)

Redirect stdout stream contents to telegram chat.

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

### Use as context manager:
```python
with logger:
    print('Text')
```

### And as decorator:
```python
@logger
def amazing_function():
    print('Text')
```

## Result:
![result](result.png?raw=true "Result")

### Log to both stdout and telegram chat
```python
logger = P2TG("telegram bot token", 1337, also_print=True)
```

Original idea here [this repo](https://github.com/laike9m/f)
