import time
import random
from utils import Semaphore, Thread


def delay():
    time.sleep(random.random())


def no_starve_mutex(i):

    global room1, room2

    # Morri's Algorithm
    while True:
        mutex.wait()
        room1 += 1
        mutex.signal()

        turnstile1.wait()
        room2 += 1
        mutex.wait()
        room1 -= 1

        if room1 == 0:
            mutex.signal()
            turnstile2.signal()
        else:
            mutex.signal()
            turnstile1.signal()

        turnstile2.wait()
        room2 -= 1

        # Critical Section
        delay()
        print('Thread #{} is being executed'.format(i))

        if room2 == 0:
            turnstile1.signal()
        else:
            turnstile2.signal()


room1 = room2 = 0
mutex = Semaphore(1)
turnstile1 = Semaphore(1)
turnstile2 = Semaphore(0)

num_threads = 5
[Thread(no_starve_mutex, i) for i in range(num_threads)]
