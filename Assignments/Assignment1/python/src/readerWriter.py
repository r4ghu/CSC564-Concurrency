from utils import Semaphore, Thread, execution_manager
import time
import os
import signal
import sys
import random


class LightSwitch:
    def __init__(self):
        self.counter = 0
        self.mutex = Semaphore(1)

    def lock(self, semaphore):
        self.mutex.wait()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.signal()

    def unlock(self, semaphore):
        self.mutex.wait()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.signal()

score = 0
num_writers = 5
num_readers = 5
readSwitch = LightSwitch()
roomEmpty = Semaphore(1)
turnstile = Semaphore(1)  # Turnstile for readers and mutex for writers


def writer(i):
    global score
    while True:
        time.sleep(random.random())
        turnstile.wait()
        roomEmpty.wait()

        # Critical Section for writers
        score += 1
        print("Writer {} is writing {}".format(i, score))
        time.sleep(random.random() * 5)

        turnstile.signal()
        roomEmpty.signal()


def reader(i):
    global score, readSwitch
    while True:
        turnstile.wait()
        turnstile.signal()
        readSwitch.lock(roomEmpty)

        # Critical section for readers
        print("Reader {} is reading {}".format(i, score))
        time.sleep(random.random() * 5)

        readSwitch.unlock(roomEmpty)
        time.sleep(random.random() * 10)

execution_manager()
[Thread(writer, i) for i in range(num_writers)]
[Thread(reader, i) for i in range(num_readers)]





