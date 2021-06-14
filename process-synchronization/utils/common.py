import platform


def get_version():
    return tuple(map(int, platform.python_version_tuple()))
