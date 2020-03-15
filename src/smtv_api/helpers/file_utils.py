from functools import wraps
import os
import tempfile
import tarfile


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


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
