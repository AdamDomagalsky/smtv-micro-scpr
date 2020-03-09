import os


def run() -> None:
    os.execv('/usr/local/bin/alembic', ['alembic', 'upgrade', 'head'])


if __name__ == '__main__':
    run()
