from functools import wraps
from pathlib import Path
import os
import tempfile


def TemporaryDirectory(func):
    '''This decorator creates temporary directory and wraps given fuction'''

    @wraps(func)
    def wrapper(*args, **kwargs):
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp_path:
            os.chdir(tmp_path)
            result = func(*args, **kwargs)
            os.chdir(cwd)
            return result

    return wrapper
