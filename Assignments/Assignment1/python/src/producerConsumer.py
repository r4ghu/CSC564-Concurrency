from utils import Semaphore, Thread, Buffer, execution_manager
import random
import time


class WaitForEvent:
    def __init__(self, data):
        self.data = data

    def process(self):
        print("Finished consuming event {}".format(self.data))

mutex = Semaphore(1)
items = Semaphore(0)
buffer = Buffer()


def delay(n=1):
    return time.sleep(random.random() * n)


def Producer():
    global buffer
    data = 0
    while True:
        delay(2)
        event = WaitForEvent(data)
        print("Producing event {}".format(event.data))
        mutex.wait()
        buffer.add(event)
        mutex.signal()
        items.signal()
        data += 1


def Consumer():
    global buffer
    while True:
        items.wait()
        mutex.wait()
        event = buffer.get()
        mutex.signal()
        print("Consuming event {}".format(event.data))
        delay()
        event.process()


#execution_manager() # Forces a global parent thread
Thread(Producer)
Thread(Consumer)
