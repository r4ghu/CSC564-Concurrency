import threading
import os
import signal
import sys
import collections


class Semaphore(threading.Semaphore):
    wait = threading.Semaphore.acquire
    signal = threading.Semaphore.release


class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


class Buffer(collections.deque):
    add = collections.deque.append
    get = collections.deque.popleft


def execution_manager():
    child = os.fork()
    if child == 0:
        return
    try:
        os.wait()
    except KeyboardInterrupt:
        print('Keyboard Interrupt: Killing the Program')
        os.kill(child, signal.SIGKILL)
    sys.exit()