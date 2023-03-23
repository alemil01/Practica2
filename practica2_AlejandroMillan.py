import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value, Manager

NCAR_N = 20 #Number of cars heading North
NCAR_S = 20 #Number of cars heading South
NPED = 10 #Number of pedestrian

TIME_CARS_NORTH = 0.5 #A new car enters each 0.5s
TIME_CARS_SOUTH = 0.5 #A new car enters each 0.5s
TIME_PED = 5 #A new pedestrian enters each 5s
TIME_IN_BRIDGE_CARS = (1.5, 1) #A car takes 1s crossing
TIME_IN_BRIDGE_PEDESTRIAN = (2.5, 2) #A pedestrian takes 10s crossing

class Monitor():
	def __init__(self):
		self.mutex = Lock()
		self.patata = Value('i', 0) #Number of calls to the monitor made by the processes
		
		manager = Manager()
		self.puente = manager.list() #List to see who is crossing at every moment
		
		self.n_north = Value('i', 0) #Number of cars heading North crossing 
		self.n_south = Value('i', 0) #Number of cars heading South crossing 
		self.n_ped = Value('i', 0) #Number of pedestrians crossing 
		
		self.waiting_N = Value('i', 0) #Number of cars heading North waiting to cross 
		self.waiting_S = Value('i', 0) #Number of cars heading South waiting to cross 
		self.waiting_P = Value('i', 0) #Number of pedestrians waiting to cross
		
		self.wait_N = Condition(self.mutex) #Condition variable for cars heading North to wait for crossing the bridge
		self.wait_S = Condition(self.mutex) #Condition variable for cars heading South to wait for crossing the bridge
		self.wait_P = Condition(self.mutex) #Condition variable for pedestrians to wait for crossing the bridge
		
		
		self.n_north = Value('i', 0) #Number of cars heading North crossing 
		self.n_south = Value('i', 0) #Number of cars heading South crossing 
		self.n_ped = Value('i', 0) #Number of pedestrians crossing 
		
		self.pass_N = Condition(self.mutex) #Condition variable for cars heading North to cross the bridge
		self.pass_S = Condition(self.mutex) #Condition variable for cars heading South to cross the bridge
		self.pass_P = Condition(self.mutex) #Condition variable for pedestrians to cross the bridge
		

		
	#To be more realistic, taking into account the size of the bridge, we only allow one car at the bridge. Obviously, cars and pedestrians cannot cross at the same time. Idem for cars in different directions
	
	
#Como el proceso de cada coche no tiene acciones atómicas podría ocurrir que se añaden a la lista en orden distinto el append y el delay, por lo que el primer coche que sale del puente no tiene por que ser el primero que entró.
	
	def can_N(self) -> bool:
		return self.n_south.value == 0 and self.n_ped.value == 0 
		
	def can_wait_N(self) -> bool:
		return self.n_north.value == 0 or self.waiting_S.value+self.waiting_P.value == 0
		
	def can_S(self) -> bool:
		return self.n_north.value == 0 and self.n_ped.value == 0 
		
	def can_wait_S(self) -> bool:
		return self.n_south.value == 0 or self.waiting_N.value+self.waiting_P.value == 0
		
	def can_P(self) -> bool:
		return self.n_north.value == 0 and self.n_south.value == 0 
	
	def can_wait_P(self) -> bool:
		return self.n_ped.value == 0 or self.waiting_N.value+self.waiting_S.value == 0
		
	def wants_enter_car_N(self, cid) -> None:
		self.mutex.acquire()
		self.patata.value += 1
		self.wait_N.wait_for(self.can_wait_N)
		self.waiting_N.value += 1
		self.pass_N.wait_for(self.can_N)
		self.waiting_N.value -= 1
		self.n_north.value += 1
		self.wait_S.notify_all()
		self.wait_P.notify_all()
		self.puente.append(f'{cid}_N')
		self.mutex.release()
		
	def leaves_car_N(self, cid) -> None:
		self.mutex.acquire()
		self.patata.value += 1
		self.puente.remove(f'{cid}_N')
		self.n_north.value -= 1
		if self.n_north.value == 0:
			self.pass_P.notify_all()
			self.pass_S.notify_all()
		self.mutex.release()
		
	def wants_enter_car_S(self, cid) -> None:
		self.mutex.acquire()
		self.patata.value += 1
		self.wait_S.wait_for(self.can_wait_S)
		self.waiting_S.value += 1
		self.pass_S.wait_for(self.can_S)
		self.waiting_S.value -= 1
		self.n_south.value += 1
		self.wait_P.notify_all()
		self.wait_S.notify_all()
		self.puente.append(f'{cid}_S')
		self.mutex.release()
		
	def leaves_car_S(self, cid) -> None:
		self.mutex.acquire()
		self.patata.value += 1
		self.puente.remove(f'{cid}_S')
		self.n_south.value -= 1
		if self.n_south.value == 0:
			self.pass_N.notify_all()
			self.pass_P.notify_all()
		self.mutex.release()
		
	def wants_enter_pedestrian(self, pid) -> None:
		self.mutex.acquire()
		self.patata.value += 1
		self.wait_P.wait_for(self.can_wait_P)
		self.waiting_P.value += 1
		self.pass_P.wait_for(self.can_P)
		self.waiting_P.value -= 1
		self.n_ped.value += 1
		self.wait_N.notify_all()
		self.wait_S.notify_all()
		self.puente.append(f'{pid}')
		self.mutex.release()
		
	def leaves_pedestrian(self, pid) -> None:
		self.mutex.acquire()
		self.patata.value += 1
		self.puente.remove(f'{pid}')
		self.n_ped.value -= 1
		if self.n_ped.value == 0:
			self.pass_N.notify_all()
			self.pass_S.notify_all()
		self.mutex.release()
	
	
	def __repr__(self) -> str:
		return f'Monitor: {self.patata.value}. Crossing the bridge: {self.puente}'
		
def delay_car_north(factor = random.uniform(TIME_IN_BRIDGE_CARS[0], TIME_IN_BRIDGE_CARS[1])) -> None:
    time.sleep(factor)

def delay_car_south(factor = random.uniform(TIME_IN_BRIDGE_CARS[0], TIME_IN_BRIDGE_CARS[1])) -> None:
    time.sleep(factor)

def delay_pedestrian(factor = random.uniform(TIME_IN_BRIDGE_PEDESTRIAN[0], TIME_IN_BRIDGE_PEDESTRIAN[1])) -> None:
    time.sleep(factor)
		
def car_N(cid: int, monitor: Monitor) -> None:
	print(f'car {cid}_N wants to cross. {monitor}')
	monitor.wants_enter_car_N(cid)
	print(f'car {cid}_N enters the bridge. {monitor}')
	delay_car_north()
	print(f'car {cid}_N leaving the bridge. {monitor}')
	monitor.leaves_car_N(cid)
	print(f'car {cid}_N out of the bridge. {monitor}')
	
def car_S(cid: int, monitor: Monitor) -> None:
	print(f'car {cid}_S wants to cross. {monitor}')
	monitor.wants_enter_car_S(cid)
	print(f'car {cid}_S enters the bridge. {monitor}')
	delay_car_south(cid)
	print(f'car {cid}_S leaving th bridge. {monitor}')
	monitor.leaves_car_S(cid)
	print(f'car {cid}_S out of the bridge. {monitor}')
	
def pedestrian(pid: int, monitor: Monitor) -> None:
	print(f'pedestrian {pid} wants to enter. {monitor}')
	monitor.wants_enter_pedestrian(pid)
	print(f'pedestrian {pid} enters the bridge. {monitor}')
	delay_pedestrian()
	print(f'pedestrian {pid} leaving the bridge. {monitor}')
	monitor.leaves_pedestrian(pid)
	print(f'pedestrian {pid} out of the bridge. {monitor}')
	
	
def gen_car_N(monitor: Monitor) -> None:
	cid = 0
	plst = []
	for _ in range(NCAR_N):
		cid += 1
		p = Process(target = car_N, args=(cid, monitor))
		p.start()
		plst.append(p)
		time.sleep(random.expovariate(1/TIME_CARS_NORTH))
	for p in plst:
		p.join()
	print(f'There is no more cars heading North')
		
def gen_car_S(monitor: Monitor) -> None:
	cid = 0
	plst = []
	for _ in range(NCAR_S):
		cid += 1
		p = Process(target = car_S, args=(cid, monitor))
		p.start()
		plst.append(p)
		time.sleep(random.expovariate(1/TIME_CARS_SOUTH))
	for p in plst:
		p.join()
	print(f'There is no more cars heading South')
		
def gen_pedestrian(monitor: Monitor) -> None:
	pid = 0
	plst = []
	for _ in range(NPED):
		pid += 1
		p = Process(target = pedestrian, args=(pid, monitor))
		p.start()
		plst.append(p)
		time.sleep(random.expovariate(1/TIME_PED))
	for p in plst:
		p.join()
	print(f'There is no more pedestrians')
		
def main():
    monitor = Monitor()
    gcars_N = Process(target = gen_car_N, args = (monitor,))
    gcars_S = Process(target = gen_car_S, args = (monitor,))
    gped = Process(target=gen_pedestrian, args=(monitor,))
    gcars_N.start()
    gcars_S.start()
    gped.start()
    gcars_N.join()
    gcars_S.join()
    gped.join()
    print('Bridge is closed until the next execution')

if __name__ == '__main__':
    main()
