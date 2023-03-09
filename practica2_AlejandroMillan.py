import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 100
NPED = 10
TIME_CARS = 0.5 #A new car enters each 0.5s
TIME_PED = 5 #A new pedestrian enters each 5s
TIME_IN_BRIDGE_CARS = (1, 0.5) #normal 1s, 0.5s
TIME_IN_BRIDGE_PEDESTRIAN = (30, 10) #norml 1s, 0.5s

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.patata = Value('i', 0)

    def wants_enter_car(self, direction: int) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        #Code
        self.mutex.release()

    def leaves_car(self, direction: int) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        #Code
        self.mutex.release()

    def wants_enter_pedestrian(self) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        #Code
        self.mutex.release()

    def leaves_pedestrian(self) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        #Code
        self.mutex.release()

    def __repr__(self) -> str:
        return f'Monitor: {self.patata.value}'

def delay_car_north() -> None:
    pass

def delay_car_south() -> None:
    pass

def delay_pedestrian() -> None:
    pass

def car(cid: int, direction: int, monitor = Monitor) -> None:
    print(f'car {cid} heading {direction} wants to enter. {monitor}')
    monitor. wants_enter_car_(direction)
    print(f'car {cid} heading {direction} enters the bridge. {monitor}')
    if direction==NORTH:
        delay_car_north()
    else:
        delay_car_south()
    print(f'car {cid} heading {direction} leaving the bridge. {monitor}')
    monitor.leaves_car(direction)
    print(f'car {cid} heading {direction} out of the bridge. {monitor}')

def pedestrian(pid: int, monitor: Monitor) -> None:
    print(f'pedestrian {pid} wants to eneter. {monitor}')
    monitor.wants_enter_pedestrian()
    print(f'pedestrian {pid} enters the bridge. {monitor}')
    delay_pedestrian()
    print(f'pedestrian {pid} leaving the bridge. {monitor}')
    monitor.leaves_pedestrian()
    print(f'pedestrian {pid} out of the bridge. {monitor}')

def gen_pedestrian(monitor: Monitor) -> None:
    pid = 0
    plst = []
    for v in range(NPED):
        pid += 1
        p = Process(target = pedestrian, args = (pid, monitor))
        p.satart()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_PED))

    for p in plst:
        p.join()

def gen_cara(monitor: Monitor) -> None:
    cid = 0
    plst = []
    for w in range(NCARS):
        directoin = NORTH if random.randint(0,1) == 1 else SOUTH
        cid += 1
        p = Process(target = car, args=(cid, directoin, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_CARS))

    for p in plst:
        p.join()

def main():
    monitor = Monitor()
    gcars = Process(target = gen_cats, args = (monitor),))
    gped = Process(target=gen_pedestrian, args=(monitor,))
    gcars.start()
    gped.start()
    gcars.join()
    gped.join()

if __name__ == '__main__':
    main()
