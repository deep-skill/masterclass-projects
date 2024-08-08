import simpy
from storage import Storage
from truck import Truck


class Dump(Storage):
    def __init__(self, env: simpy.Environment, capacity, data, working_time=None):
        super().__init__(env, capacity, data, working_time)
        self.data['reserved_tons'] = 0

    def work(self, truck: Truck, time=None):
        arrival_time = self.env.now

        # Mark arrival time
        truck.add_position(self.data['name'], self.env.now)

        with self.queue.request() as request:
            yield request

            # Mark start time
            truck.add_position(self.data['name'], self.env.now)

            start_time = self.env.now
            self.data['waiting_time'] += start_time - arrival_time
            self.data['number_of_server_trucks'] += 1
            if arrival_time == start_time: self.data['number_of_server_trucks_without_waiting'] += 1

            if not time: time = self.get_time()

            yield self.env.timeout(time)

            self.data['reserved_tons'] += truck.get_tons()
            truck.assign_tons(0)

            finish_time = self.env.now

            # Mark finish time
            truck.add_position(self.data['name'], self.env.now)

            self.data['using_time'] += finish_time - start_time

    def work_process(self, truck: Truck, time=None):
        return self.env.process(self.work(truck, time))

    def report(self):
        print(f"REPORTE botadero {self.data['name']}:")
        print(f"Desmonte (en toneladas): {self.data['reserved_tons']}")
        print("")
