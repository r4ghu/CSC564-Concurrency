import threading
import random
import sys
import getopt
import time
import copy
from functools import reduce

verbose = False
generals = []
MESSAGE = 50


class General(threading.Thread):
    
    N = 7 # Generals
    M = 2 # Traitors
    
    def __init__(self, isCommander, isTraitor, ID, max_recursion=None) :
        threading.Thread.__init__(self)
        self.isCommander = isCommander
        self.isTraitor = isTraitor
        self.ID = ID
        self.queue = []
        self.messages = []
        self.finish = False
        self.finalVote = 0
        self.mutex = threading.Lock()
        self.max_recursion = General.N-1 if max_recursion is None else max_recursion
	   
    def run(self) :
        # Start running the thread
        self.thread_log(self, 'Starting [Commander : {}, Traitor : {}]'.format(self.isCommander, self.isTraitor))
        # Sleep for sometime to start other threads
        time.sleep(0.5)

        # If commander, then send command to all generals
        if self.isCommander :
            self.send_message(":%d" % (MESSAGE))
            self.finish = True
        # If general, receive command from commander and exchange the message.
        else :
            # Compute total number of messages to be received
            num_messages = reduce(lambda x, y: x + y, [reduce(lambda x, y: x * y, i)
                                  for i in [[General.N-2-n for n in range(0, m+1)]
                                  for m in range(General.M)]]) + 1
                            
            # Run a while loop until you receive all the messages from other generals
            while num_messages > len(self.messages):
                message = self.recv_message()
                self.messages.append(message)
                self.send_message(message)
            
            self.thread_log(self,"TOTAL MESSAGES = %d, RECEIVED MESSAGES = %d" % (num_messages, len(self.messages)))
            
            # OM(m) algorithm
            for message in self.messages :
                temp_path, temp_message = message.split(':')
                path = list(map(int, temp_path.split('->')))
                current_message = int(temp_message)
                if len(path) == 1 :
                    self.finalVote = self.vote(path, current_message, General.M)
                    break
            
            # Print the vote
            if self.finalVote == 0:
                self.thread_log(self, "Voted: NO ACTION")
            elif self.finalVote > 0:
                self.thread_log(self, "Voted: ATTACK")
            elif self.finalVote < 0:
                self.thread_log(self, "Voted: RETREAT")
			   
    def vote(self, path, msg, m, recursive_step = 0):
        '''
        Recursive method to vote the general's final decision
        '''
        # Get the list of generals
        gens = [ x for x in range(0,General.N) if x not in path and x != self.ID]
        # And their corresponding messages
        results = [msg]
        if m == 0:
            return self.get_message(path)
        else:
            for g in gens :
                temp_path = copy.copy(path)
                temp_path.append(g)
                msg = self.get_message(temp_path)
                if recursive_step < self.max_recursion:
                    result = self.vote(temp_path, msg, m-1, recursive_step=recursive_step+1)
                    results.append(result)
            # Voting phase
            if results.count(MESSAGE) > len(results)/2 : 
                return MESSAGE
            else : return -1		   
	   
    def get_message(self, path) :
        '''
        Method to get message for voting
        '''
        path = "->".join(map(str, path))

        for message in self.messages:
            p, m = message.split(':')
            if p == path :
                return int(m)
        # Sanity check: TAKE NO ACTION
        return 0
			   
    def send_message(self, message) :
        '''
        Method to send message to other generals
        '''
        path, command = message.split(":")
        
        # Trace the path and do sanity check
        if path=='':
            path = [self.ID]
        else:
            path = list(map(int, path.split('->')))
            path.append(self.ID)
        # Sanity Check
        if len(path) == General.M + 2 : 
            return False

        for g in generals :
            if g.ID not in path :
                message = '->'.join(map(str,path))
                command = command if not self.isTraitor else str(random.randint(-1,100))
                if verbose : 
                    self.thread_log(self,'Send: ' + message + ':' + command)
                if  g.mutex.acquire():
                    g.queue.append(message + ':' + command)
                    g.mutex.release()
        return True
					   
    def recv_message(self):
        '''
        Method to receive message from other generals
        '''
        message = None
        while message is None:
            # Wait for some time before acquiring messages
            time.sleep(0.01)

            # Start acquiring messages
            if self.mutex.acquire():
                if len(self.queue) > 0:
                    message = self.queue.pop(0)
                self.mutex.release()
        # Log for debugging
        if verbose : self.thread_log(self,'Received: ' + message)
        return message
    
    def thread_log(self, general, message):
        '''
        Method to debug log inside threads.
        '''
        if self.mutex.acquire():
            print("General {} : {}".format(general.ID, message))
            self.mutex.release()


def main(N=7, M=2):
    General.N = N
    General.M = M

    print('Starting Byzantine Generals: N = {}, M = {}'.format(General.N,General.M))

    m = 0
    for i in range(General.N) :
        # Set G_0 as Commander and randomize the traitors
        if m >= General.M :
            istraitor = False
        else :
            istraitor = True if random.randint(0,1) == 0 else False
            if istraitor :
                m +=1
        # G_0 is always the commander
        g = General(i == 0, istraitor, i, 2)
        generals.append(g)
        g.start()
    
    for g in generals :
        g.join()


if __name__ == '__main__':
	main(3,1)
