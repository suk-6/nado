import os
from dotenv import load_dotenv

load_dotenv()


def getENV(key):
    return os.getenv(key)
