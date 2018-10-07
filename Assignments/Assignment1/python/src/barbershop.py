# Link: https://github.com/nicolas3470/Python-synchronization/blob/master/q05.py
from utils import execution_manager, Semaphore, Thread
import time
import random


def delay():
    time.sleep(random.randint(0, 2))


class BarberShop:
    def __init__(self, num_seats):
        self.available_seats = num_seats
        self.seats_mutex = Semaphore(1)
        self.customers = Semaphore(0)
        self.barbers = Semaphore(0)

    def barber_ready(self):
        # Barber is ready
        # Signal one of the waiting customers
        self.customers.wait()
        self.seats_mutex.wait()
        self.available_seats += 1
        self.barbers.signal()
        self.seats_mutex.signal()

    def customer_enter(self):
        # Return True, if customer sat
        # Else, return false, customer left
        self.seats_mutex.wait()
        if self.available_seats > 0:
            self.available_seats -= 1
            return True
        else:
            self.seats_mutex.signal()
            return False

    def customer_sit(self):
        # Sit until Barber is ready
        self.customers.signal()
        self.seats_mutex.signal()
        self.barbers.wait()


def Barber(i):
    global barbershop
    while True:
        print("Barber {}: Ready".format(i))
        barbershop.barber_ready()
        print("Barber {}: Started cutting hair".format(i))
        delay()
        print("Barber {}: DONE".format(i))


def Customer(i):
    global barbershop
    while True:
        print("Customer {}: Arrived to barber shop".format(i))
        if barbershop.customer_enter():
            print("Customer {}: Entered and Sat".format(i))
            barbershop.customer_sit()
            print("Customer {}: Successful Haircut!".format(i))
        else:
            print("Customer {}: Turned away from the door".format(i))
        delay()


num_barbers = 3
num_customers = 6
num_seats = 3
barbershop = BarberShop(num_seats)

#execution_manager()
[Thread(Barber, i) for i in range(num_barbers)]
[Thread(Customer, i) for i in range(num_customers)]