from notebook.settings import UNIVERSAL_SET


def test_universal_set():
    class Singleton:
        pass

    # made-up class that couldn't possibly be there
    assert Singleton in UNIVERSAL_SET
