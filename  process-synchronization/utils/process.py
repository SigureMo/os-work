from threading import Event, Thread

from utils.common import get_version
from utils.primitive import MUTEX


class Process(Thread):
    """伪进程类
    为了在 Python 中更容易地实现并发操作，故使用多线程来模拟（大概可以？）
    """

    def __init__(self):
        super().__init__()
        self.setDaemon(True)
        self.__flag = Event()
        self.__flag.set()

    def pause(self):
        self.__flag.clear()
        MUTEX.release()
        self.__flag.wait()
        MUTEX.acquire()

    def restart(self):
        self.__flag.set()

    @property
    def is_alive(self):
        if get_version() >= (3, 9, 0):
            is_alive = super().is_alive
        else:
            is_alive = super().isAlive
        return is_alive


def all_start(*pros):
    for pro in pros:
        pro.start()

    try:
        for pro in pros:
            while True:
                pro.join(2)
                if not pro.is_alive:
                    break
    except (SystemExit, KeyboardInterrupt):
        print("Ctrl-C pressed")
