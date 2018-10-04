"""
Writer-priority Readers Writers
In this solution, we give priority to writer.
i.e., If one writer enters the critical section, no orther reader will
be allowed.
"""

from readerWriter import LightSwitch
from utils import Semaphore, Thread, execution_manager
import time
import random

score = 0
num_writers = 5
num_readers = 5
readSwitch = LightSwitch()
writeSwitch = LightSwitch()
noReaders = Semaphore(1)
noWriters = Semaphore(1)


def writer(i):
    global score
    while True:
        time.sleep(random.random())
        writeSwitch.lock(noReaders)
        noWriters.wait()

        # Critical Section for writers
        score += 1
        print("Writer {} is writing {}".format(i, score))
        time.sleep(random.random() * 5)

        writeSwitch.unlock(noReaders)


def reader(i):
    global score, readSwitch
    while True:
        noReaders.wait()
        readSwitch.lock(noWriters)
        noReaders.signal()

        # Critical section for readers
        print("Reader {} is reading {}".format(i, score))
        time.sleep(random.random() * 5)

        readSwitch.unlock(noWriters)
        time.sleep(random.random() * 10)

#execution_manager()
[Thread(writer, i) for i in range(num_writers)]
[Thread(reader, i) for i in range(num_readers)]

# TODO: Improve by applying No-starve Mutex


# # Reader
# noReaders.wait()
# readSwitch.lock(noWriters)
# noReaders.signal()
# # Critical section for readers
# readSwitch.unlock(noWriters)


# # Writer
# writeSwitch.lock(noReaders)
# noWriters.wait()
# # Critical section for writers
# writeSwitch.unlock(noReaders)