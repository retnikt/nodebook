"""
Copyright © retnikt <_@retnikt.uk> 2020
This software is licensed under the MIT Licence: https://opensource.org/licenses/MIT
"""
from notebook.settings import UNIVERSAL_SET


def test_universal_set():
    class Singleton:
        pass

    # made-up class that couldn't possibly be there
    assert Singleton in UNIVERSAL_SET
