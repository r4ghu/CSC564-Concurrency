# Link: https://github.com/nicolas3470/Python-synchronization/blob/master/q06.py

# from __future__ import with_statement
# from threading import Thread, Lock, Condition, Semaphore
# from os import _exit as quit
# import time, random 

# # a. Use monitors and condition variables to simulate a 
# #    (sleepy) barbershop.
# #
# #    A barbershop holds N customers, and M sleepy barbers 
# #    work on the customers. Correctness criteria are:
# #
# #    (a) no customers should enter the barbershop unless
# #        there is room for them inside
# #    (b) the barber should cut hair if there is a waiting
# #        customer
# #    (c) customers should enter the barbershop if there is 
# #        room inside
# #
# #    This is a sleepy town with laid back people, so strict 
# #    FIFO ordering of waiting customers is not a requirement.
# #

# def delay():
#     time.sleep(random.randint(0, 2))

# class BarberShop:
#     def __init__(self, numchairs):
#         self.barbers_ready = False
#         self.numchairs = numchairs
#         self.open_seats = numchairs
#         self.shop_lock = Lock()
#         self.barber_condition = Condition(self.shop_lock)
#         self.customer_condition = Condition(self.shop_lock)

#     def __sanitycheck(self):
#         if self.open_seats > self.numchairs:
#             print ("sync error: more customers than seats!")
#             exit(1)
        
#     # check for waiting customers
#     # if there are none, wait
#     # if there are waiting customers, signal one 
#     def barber_readytocut(self):
#         with self.shop_lock:
#             while self.open_seats == self.numchairs:
#                 self.barbers_ready = False
#                 self.customer_condition.wait()
#             self.barbers_ready = True
#             self.open_seats += 1
#             self.barber_condition.notify()
#             self.__sanitycheck()

#     # enter the barbershop if all numchairs are not occupied
#     # returns true if the customer entered successfully, and
#     # false if he was turned away at the door
#     def customer_enter(self):
#         with self.shop_lock:
#             if self.open_seats > 0:
#                 self.open_seats -= 1
#                 self.__sanitycheck()
#                 return True
#             else:
#                 self.__sanitycheck()
#                 return False

#     # take a seat and wait until the barber is ready to cut hair
#     def customer_takeaseat(self):
#         with self.shop_lock:
#             self.customer_condition.notify()
#             while not self.barbers_ready:
#                 self.barber_condition.wait()
#             self.barbers_ready = False
#             self.__sanitycheck()

# class Barber(Thread):
#     def __init__(self, id):
#         Thread.__init__(self)
#         self.id = id

#     def run(self):
#         global barbershop

#         while True:
#             print ("Barber #%d: ready to cut hair" % self.id)
#             barbershop.barber_readytocut()
#             print ("Barber #%d: cutting hair" % self.id)
#             delay()
#             print ("Barber #%d: done cutting hair" % self.id)

# class Customer(Thread):
#     def __init__(self, id):
#         Thread.__init__(self)
#         self.id = id

#     def run(self):
#         global barbershop

#         while True:
#             print ("Customer #%d: has long hair" % self.id)
#             if barbershop.customer_enter():
#                 print ("Customer #%d: entered, taking a seat" % self.id)
#                 barbershop.customer_takeaseat()
#                 print ("Customer #%d: got a haircut!" % self.id)
#             else:
#                 print ("Customer #%d: turned away from the door" % self.id)
#             delay()

# NUMCUSTOMERS=3
# barbershop = BarberShop(3)
# b = Barber(1)
# b.start()
# for i in range(0, NUMCUSTOMERS):
#     c = Customer(i)
#     c.start()    