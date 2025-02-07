from threading import Thread, Semaphore
import time
from enum import Enum
import random

############## INITIALIZATION BEGIN ##############

n = 5 # number of philosophers
names = ['Philosofer 1', 'Philosofer 2', 'Philosofer 3', 'Philosofer 4', 'Philosofer 5']

#states
hungry = 0
eating = 1
thinking = 2

# lock
semaphore = []

# chopsticks = [] # { True: chopsticks are on the thable, False: chopsticks are'mt on the thable }
# for i in range(0, n, 1): # set all chopsticks in the table
    # chopsticks.append(True)

dishes_is_full = [] # { True: philosopher already ate the food in this place, False: There is food on the dish }
for i in range(0, n, 1): # set all dishes as full
    dishes_is_full.append(True)

philosophers_state = [] # hangry,  eating or thinking
for i in range(0, n, 1): # set all philosophers' stats as thinking
    philosophers_state.append(hungry)

############## INITIALIZATION END ##############

############### FUNCTIONS BEGIN ###############

def right (num): # get the right philosophers index
    return (num + 1) % n

def left (num): # get the left philosophers index
    return num #(num + n - 1) % n

def eat (pos): # the philosophers start to eat
    global philosophers_state
    global dishes_is_full

    philosophers_state[pos] = eating # set the philosopher's state as 'eating'
    time.sleep(random.randint(3, 5)) # each philosophers takes something between 3 and 5 seconds to eat
    dishes_is_full[pos] = False # set the philosophers dish as empty

def think (pos):
    global philosophers_state

    philosophers_state[pos] = thinking # set the philosopher's state as 'eating'
    time.sleep(random.randint(5, 7)) # each philosophers takes something between 5 and 7 seconds to think

def philosopher (pos):
    global semaphore

    semaphore.append(Semaphore(1))

    time.sleep(5) # wait a time for all threads to be running

    while dishes_is_full[pos]: # while there is food in the dish
        semaphore[left(pos)].acquire() # wait for the left chopstick

        if semaphore[right(pos)].acquire(False): # try to get the right chopstick
            print(str(pos) + ' is eating')
            eat(pos) # the philosopher gonna stop to eat
            print(str(pos) + ' already eat')
            semaphore[left(pos)].release() # free the left chopstick before back to think
            semaphore[right(pos)].release() # free the right chopstick
            dishes_is_full[pos] = False
            think(pos)

        else:
            semaphore[left(pos)].release() # free the left chopstick
            print(str(pos) + ' could not eat, right chopstick was unvliable')
            think(pos)

############### FUNCTIONS END ################

pos = 0
threads = []
for i in names: # initialize all threads/philosophers
    t = Thread(target=philosopher, args=(pos,))
    threads.append(t) # save the thread in a list
    time.sleep(0.5)
    t.start()
    pos += 1

for x in threads: # wait until all threads finish them work
    x.join()
