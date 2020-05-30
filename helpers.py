import os
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]
