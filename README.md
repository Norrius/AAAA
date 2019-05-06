# AAAA

Python obfuscator that makes your code scream.

## Before

````python
import sys

from decimal import Decimal
from itertools import accumulate

LIMIT = 100

def fibonacci():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

def main(args):
    for number in fibonacci():
        if number > LIMIT:
            break
        print(Decimal(number))

if __name__ == '__main__':
    main(sys.argv[1:])
````

## After

````python
import sys as АAAA
from decimal import Decimal as АAAА
from itertools import accumulate as АAАA
АAАА = 100


def АААA():
    ААAA, ААAА = 1, 1
    while True:
        yield ААAA
        ААAA, ААAА = ААAА, ААAA + ААAА


def АAAAA(АAAAА):
    for АААА in АААA():
        if АААА > АAАА:
            break
        print(АAAА(АААА))


if __name__ == '__main__':
    АAAAA(АAAA.argv[1:])
````

## Options

* `--minlen n` — specifies the minimal amount of screaming
* `--inplace` — overwrites the original source (careful!)
