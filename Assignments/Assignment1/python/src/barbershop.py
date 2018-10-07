from utils import execution_manager, Semaphore, Thread
import time, random 

# a. Use semaphores to simulate a (sleepy) barbershop.
#
#    A barbershop holds N customers, and M sleepy barbers 
#    work on the customers. Correctness criteria are:
#
#    (a) no customers should enter the barbershop unless
#        there is room for them inside
#    (b) the barber should cut hair if there is a waiting
#        customer
#    (c) customers should enter the barbershop if there is 
#        room inside
#
#    This is a sleepy town with laid back people, so strict 
#    FIFO ordering of waiting customers is not a requirement.
#

def delay():
    time.sleep(random.randint(0, 2))

class BarberShop:
    def __init__(self, numchairs):
        self.open_seats = numchairs
        self.seats_mutex = Semaphore(1)
        self.customers = Semaphore(0)
        self.barbers = Semaphore(0)
        
    # check for waiting customers
    # if there are none, wait
    # if there are waiting customers, signal one 
    def barber_readytocut(self):
        self.customers.wait()
        self.seats_mutex.wait()
        self.open_seats += 1
        self.barbers.signal()
        self.seats_mutex.signal()

    # enter the barbershop if all numchairs are not occupied
    # returns true if the customer entered successfully, and
    # false if he was turned away at the door
    def customer_enter(self):
        self.seats_mutex.wait()
        if self.open_seats > 0:
            self.open_seats -= 1
            return True
        else:
            self.seats_mutex.signal()
            return False

    # take a seat and wait until the barber is ready to cut hair
    def customer_takeaseat(self):
        self.customers.signal()
        self.seats_mutex.signal()
        self.barbers.wait()


def Barber(i):
    global barbershop
    while True:
        print("Barber {}: ready to cut hair".format(i))
        barbershop.barber_readytocut()
        print("Barber {}: cutting hair".format(i))
        delay()
        print("Barber {}: done cutting hair".format(i))


def Customer(i):
    global barbershop
    while True:
        print ("Customer #%d: has long hair" % i)
        if barbershop.customer_enter():
            print ("Customer #%d: entered, taking a seat" % i)
            barbershop.customer_takeaseat()
            print ("Customer #%d: got a haircut!" % i)
        else:
            print ("Customer #%d: turned away from the door" % i)
        delay()


num_barbers = 3
num_customers = 6
num_seats = 3
barbershop = BarberShop(num_seats)

execution_manager()
[Thread(Barber, i) for i in range(num_barbers)]
[Thread(Customer, i) for i in range(num_customers)]