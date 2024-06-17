import os


def getenv(key: str):
    return os.environ.get(key, None)
