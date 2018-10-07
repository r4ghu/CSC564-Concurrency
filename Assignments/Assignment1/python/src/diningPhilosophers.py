# Source - https://rosettacode.org/wiki/Dining_philosophers#Python

import threading
import random
import time
from utils import Philosopher
 
# Dining philosophers, 5 Phillies with 5 forks. Must have two forks to eat.
#
# Deadlock is avoided by never waiting for a fork while holding a fork (locked)
# Procedure is to do block while waiting to get first fork, and a nonblocking
# acquire of second fork.  If failed to get second fork, release first fork,
# swap which fork is first and which is second and retry until getting both.
#  
# See discussion page note about 'live lock'.

num_forks = 5
num_philosophers = 5
forks = [threading.Lock() for i in range(num_forks)]
philosopher_names = ('A', 'B', 'C', 'D', 'E')
philosophers = [Philosopher(philosopher_names[i], forks[i % 5], forks[(i+1) % 5])
                for i in range(num_philosophers)]
Philosopher.running = True
for p in philosophers:
    p.start()
time.sleep(50)
Philosopher.running = False
print("DONE!!!")
