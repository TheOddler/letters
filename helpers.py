import os


def file_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]
