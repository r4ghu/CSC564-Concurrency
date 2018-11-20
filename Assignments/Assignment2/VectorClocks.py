from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime

def get_local_time(counter):
    '''
    Method to compare and log local time and lamport time.
    '''
    return '(LAMPORT TIME = {}, LOCAL TIME = {})'.format(counter, datetime.now())


def calculate_receiver_timestamp(receiver_time_stamp, counter):
    '''
    Method to calculate the receiver timestamp
    '''
    for id in range(len(counter)):
        counter[id] = max(receiver_time_stamp[id], counter[id])
    return counter


def event(pid, counter, message = None):
    '''
    Method to process event and increment counter.
    '''
    counter[pid] += 1
    if message is None: message = 'Something'
    print('{} happened in {} '.format(message, pid + 1) + get_local_time(counter))
    return counter


def send_message(pipe, pid, counter):
    '''
    Method to send message and increment counter.
    '''
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from ' + str(pid) + get_local_time(counter))
    return counter


def recv_message(pipe, pid, counter):
    '''
    Method to receive message
    '''
    message, timestamp = pipe.recv()
    counter = calculate_receiver_timestamp(timestamp, counter)
    print('Message received at ' + str(pid)  + get_local_time(counter))
    return counter

# Process 1, 2 and 3: Please check figure in the report for clear understanding
def process_one(pipe12):
    pid = 0
    counter = [0, 0, 0]
    counter = event(pid, counter, 'Process 1: Event 1')
    counter = send_message(pipe12, pid, counter)
    counter  = event(pid, counter, 'Process 1: Event 2')
    counter  = event(pid, counter, 'Process 1: Event 3')
    counter = recv_message(pipe12, pid, counter)
    counter  = event(pid, counter, 'Process 1: Event 4')
    counter = event(pid, counter, 'Process 1: Event 5')

def process_two(pipe21, pipe23):
    pid = 1
    counter = [0, 0, 0]
    counter = event(pid, counter, 'Process 2: Event 1')
    counter = send_message(pipe23, pid, counter)
    counter = recv_message(pipe21, pid, counter)
    counter = event(pid, counter, 'Process 2: Event 2')
    counter = event(pid, counter, 'Process 2: Event 3')
    counter = send_message(pipe21, pid, counter)
    counter = recv_message(pipe23, pid, counter)
    counter = event(pid, counter, 'Process 2: Event 4')

def process_three(pipe32):
    pid = 2
    counter = [0, 0, 0]
    counter = event(pid, counter, 'Process 3: Event 1')
    counter = send_message(pipe32, pid, counter)
    counter = recv_message(pipe32, pid, counter)
    counter = event(pid, counter, 'Process 3: Event 2')
    counter = event(pid, counter, 'Process 3: Event 3')
    counter = send_message(pipe32, pid, counter)
    counter = event(pid, counter, 'Process 3: Event 4')


def main():
    '''
    The main method runs here.
    For this problem, we use pipes instead of sockets 
    '''
    pipe_1_2, pipe_2_1 = Pipe()
    pipe_2_3, pipe_3_2 = Pipe()

    process_1 = Process(target=process_one, 
                       args=(pipe_1_2,))
    process_2 = Process(target=process_two, 
                       args=(pipe_2_1, pipe_2_3))
    process_3 = Process(target=process_three, 
                       args=(pipe_3_2,))

    process_1.start()
    process_2.start()
    process_3.start()

    process_1.join()
    process_2.join()
    process_3.join()


if __name__ == '__main__':
    main()