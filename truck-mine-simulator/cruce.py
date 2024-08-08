from storage import Storage
from truck import Truck


class Cruce(Storage):
    def work(self, truck: Truck, start: str = "", end: str = "", time: float = None):
        arrival_time = self.env.now

        # Mark arrival time
        truck.add_position(self.data['name'] + start, self.env.now)

        with self.queue.request() as request:
            yield request

            start_time = self.env.now

            # Mark start time
            truck.add_position(self.data['name'] + start, self.env.now)

            self.data['waiting_time'] += start_time - arrival_time
            self.data['number_of_server_trucks'] += 1
            if arrival_time == start_time: self.data['number_of_server_trucks_without_waiting'] += 1

            if not time: time = self.get_time()

            yield self.env.timeout(time)

            finish_time = self.env.now

            # Mark finish time
            truck.add_position(self.data['name'] + end, self.env.now)

            self.data['using_time'] += finish_time - start_time

    def work_process(self, truck: Truck, start: str = "", end: str = "", time: float = None):
        return self.env.process(self.work(truck, start, end, time))

    def report(self):
        print(f"REPORTE cruce {self.data['name']}:")
        print("Tiempo de espera en el cruce {0}: {1:.3f}".format(self.data['name'], self.data['waiting_time']))
        print(f"Cantidad de camiones atendidos: {self.data['number_of_server_trucks']}")
        print(f"Cantidad de camiones atendidos sin espera: {self.data['number_of_server_trucks_without_waiting']}")
        print("")