# Link: https://github.com/nicolas3470/Python-synchronization/blob/master/q06.py

from threading import Lock, Condition
from utils import Thread, execution_manager
from barbershop import Barber, Customer


def delay():
    time.sleep(random.randint(0, 2))


class BarberShop:
    def __init__(self, num_seats):
        self.barbers_ready = False
        self.num_seats = num_seats
        self.open_seats = num_seats
        self.shop_mutex = Lock()
        self.barber_condition = Condition(self.shop_mutex)
        self.customer_condition = Condition(self.shop_mutex)
        
    def barber_ready(self):
        # Barber is ready
        # Signal one of the waiting customers
        with self.shop_mutex:
            while self.open_seats == self.num_seats:
                self.barbers_ready = False
                self.customer_condition.wait()
            self.barbers_ready = True
            self.open_seats += 1
            self.barber_condition.notify()

    def customer_enter(self):
        # Return True, if customer sat
        # Else, return false, customer left
        with self.shop_mutex:
            if self.open_seats > 0:
                self.open_seats -= 1
                return True
            else:
                return False

    def customer_sit(self):
        # Sit until Barber is ready
        with self.shop_mutex:
            self.customer_condition.notify()
            while not self.barbers_ready:
                self.barber_condition.wait()
            self.barbers_ready = False

num_barbers = 3
num_customers = 6
num_seats = 3
barbershop = BarberShop(num_seats)

execution_manager()
[Thread(Barber, i) for i in range(num_barbers)]
[Thread(Customer, i) for i in range(num_customers)] 