'''
A simple airport simulation to test the simulation framework
We have three stages for each passenger
1. Gate: getting past security
2. Check-in: getting luggage checked in
3. Boarding: boarding the plane itself
'''

import environment
import process
import resource
import random

class PassengerArrival(environment.Event):
    def __init__(self, trigger_time:float, env:environment.Environment, guard: resource.Resource,
                 check_in_agent: resource.Resource,
                 boarding_agent: resource.Resource):
        super().__init__(trigger_time)
        self._env = env
        self.guard = guard
        self.check_in_agent = check_in_agent
        self.boarding_agent = boarding_agent
    
    def process(self, currTime):
        #make a new passenger right now
        super().process(currTime)
        passenger = Passenger(self._env, self.guard, self.check_in_agent, self.boarding_agent)

class Passenger(process.Process):

    def __init__(self, env: environment.Environment, guard: resource.Resource,
                 check_in_agent: resource.Resource,
                 boarding_agent: resource.Resource):
        super().__init__(env)
        self.arrival_time = self._env.curr_time()
        self.guard = guard
        self.check_in_agent = check_in_agent
        self.boarding_agent = boarding_agent


    def run(self):
        # print(f"passenger with id {id(self)} arrived at {self._env.curr_time():2.2f}")
        #find a guard
        self.st = self._env.curr_time()
        yield self.guard.request(self.step)
        self.en = self._env.curr_time()
        self.guard_wait = self.en - self.st
        #found a guard
        # print(f"passenger with id {id(self)} found a guard at {self._env.curr_time():2.2f}")
        yield self._env.add_event(environment.Event(self._env.curr_time() + 3, [self.step]))
        self.guard.release()
        #passed gate
        self.st = self._env.curr_time()
        # print(f"passenger with id {id(self)} now in check in queue at {self._env.curr_time():2.2f}")
        yield self.check_in_agent.request(self.step)
        self.en = self._env.curr_time()
        self.checkin_q_wait_time = self.en - self.st
        # print(f"passenger with id {id(self)} now checking in at {self._env.curr_time():2.2f}")
        yield self._env.add_event(environment.Event(self._env.curr_time() + 4, [self.step]))
        self.check_in_agent.release()
        # print(f"passenger with id {id(self)} now in boarding queue at {self._env.curr_time():2.2f}")
        self.st = self._env.curr_time()
        yield self.boarding_agent.request(self.step)
        self.en = self._env.curr_time()
        self.boarding_q_wait_time = self.en - self.st
        # print(f"passenger with id {id(self)} now boarding at {self._env.curr_time():2.2f}")
        yield self._env.add_event(environment.Event(self._env.curr_time() + 2, [self.step]))
        # print(f"passenger with id {id(self)} boarded, finished at {self._env.curr_time():2.2f}")
        self.boarding_agent.release()
        self.en = self._env.curr_time()
        self.turnaround_time = self.en - self.arrival_time
        self.printStats()
    
    def printStats(self):
        print("\n----------------\n")
        print(f"stats for passenger {id(self)}: ")
        print(f"arrived at {self.arrival_time:2.2f}")
        print(f"waited at gate for: {self.guard_wait:2.2f}")
        print(f"waited in check in queue for: {self.checkin_q_wait_time:2.2f}")
        print(f"waited in boarding queue for: {self.boarding_q_wait_time:2.2f}")
        print(f"turnaround time: {self.turnaround_time:2.2f}")
        print("\n----------------\n")


env = environment.Environment(0, 100, is_real_time=False)
guard = resource.Resource(env, 4)
check_in_agent = resource.Resource(env, 5)
boarding_agent = resource.Resource(env, 10)
passenger_times = [random.uniform(0, 100) for i in range(500)]
for i in passenger_times:
    env.add_event(PassengerArrival(i, env, guard, check_in_agent, boarding_agent))
env.run()
