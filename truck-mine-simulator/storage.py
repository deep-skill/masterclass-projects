import simpy
from truck import Truck


class Storage:
    def __init__(self, env: simpy.Environment, capacity, data, working_time=None):
        self.env = env
        self.queue = simpy.Resource(env, capacity=capacity)
        self.working_time = working_time
        self.data = data

        if not self.data: self.data = {}

        self.data['waiting_time'] = 0
        self.data['using_time'] = 0
        self.data['number_of_server_trucks'] = 0
        self.data['number_of_server_trucks_without_waiting'] = 0

    def get_time(self):
        if self.working_time == None:
            return 0
        else:
            return self.working_time()


