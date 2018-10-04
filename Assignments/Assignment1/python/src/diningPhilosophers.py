# Source - https://rosettacode.org/wiki/Dining_philosophers#Python

import threading
import random
import time
 
# Dining philosophers, 5 Phillies with 5 forks. Must have two forks to eat.
#
# Deadlock is avoided by never waiting for a fork while holding a fork (locked)
# Procedure is to do block while waiting to get first fork, and a nonblocking
# acquire of second fork.  If failed to get second fork, release first fork,
# swap which fork is first and which is second and retry until getting both.
#  
# See discussion page note about 'live lock'.
 
class Philosopher(threading.Thread):
 
    running = True
 
    def __init__(self, xname, forkOnLeft, forkOnRight):
        threading.Thread.__init__(self)
        self.name = xname
        self.forkOnLeft = forkOnLeft
        self.forkOnRight = forkOnRight
 
    def run(self):
        while(self.running):
            #  Philosopher is thinking (but really is sleeping).
            time.sleep(random.uniform(3, 13))
            print ('%s is hungry.' % self.name)
            self.dine()
 
    def dine(self):
        fork1, fork2 = self.forkOnLeft, self.forkOnRight
 
        while self.running:
            fork1.acquire(True)
            locked = fork2.acquire(False)
            if locked: 
                break
            fork1.release()
            print('%s swaps forks' % self.name)
            fork1, fork2 = fork2, fork1
        else:
            return
 
        self.dining()
        fork2.release()
        fork1.release()
 
    def dining(self):			
        print ('%s starts eating '% self.name)
        time.sleep(random.uniform(1,10))
        print ('%s finishes eating and leaves to think.' % self.name)

num_forks = 5
num_philosophers = 5
forks = [threading.Lock() for i in range(num_forks)]
philosopher_names = ('A', 'B', 'C', 'D', 'E')
philosophers = [Philosopher(philosopher_names[i], forks[i%5], forks[(i+1)%5])
                for i in range(num_philosophers)]
Philosopher.running = True
for p in philosophers:
    p.start()
time.sleep(50)
Philosopher.running = False
print("Now we're finishing.")
