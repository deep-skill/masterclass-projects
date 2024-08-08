from storage import Storage
from truck import Truck


class Shovel(Storage):
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

            truck.fill_tons()

            finish_time = self.env.now

            # Mark finish time
            truck.add_position(self.data['name'], self.env.now)

            self.data['using_time'] += finish_time - start_time

    def work_process(self, truck: Truck, time=None):
        return self.env.process(self.work(truck, time))

    def report(self):
        total_time = self.env.now
        name = self.data['name']

        print(f"REPORTE Pala {self.data['name']}:")
        print("Tiempo de uso en la pala {0}: {1:.3f}".format(name, self.data['using_time']))
        print("Eficiencia de la pala {0}: {1:.3f}%".format(name, self.data['using_time'] / total_time * 100))
        print("Tiempo de espera en la pala {0}: {1:.3f}".format(name, self.data['waiting_time']))
        print(f"Cantidad de camiones atendidos: {self.data['number_of_server_trucks']}")
        print(f"Cantidad de camiones atendidos sin espera: {self.data['number_of_server_trucks_without_waiting']}")
        print("")