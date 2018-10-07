import threading
import os
import signal
import sys
import collections
import time
import random


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


class Philosopher(threading.Thread):
    running = True

    def __init__(self, name, leftFork, rightFork):
        # Initialize the thread
        threading.Thread.__init__(self)
        # Initialize the params
        self.name = name
        self.leftFork = leftFork
        self.rightFork = rightFork

    def run(self):
        self.think()

    def think(self):
        while(self.running):
            # Philosopher is thinking
            time.sleep(random.uniform(3, 13))
            print('{} is hungry'.format(self.name))
            self.eat()

    def eat(self):
        # get_forks()
        leftFork, rightFork = self.leftFork, self.rightFork

        while self.running:
            leftFork.acquire(True)
            locked = rightFork.acquire(False)
            if locked:
                break

            leftFork.release()
            print('{} swaps forks'.format(self.name))
            leftFork, rightFork = rightFork, leftFork
        else:
            return

        self.eating()
        rightFork.release()
        leftFork.release()

    def eating(self):
        print('{} starts eating'.format(self.name))
        time.sleep(random.uniform(1, 10))
        print('{} finished eating'.format(self.name))
