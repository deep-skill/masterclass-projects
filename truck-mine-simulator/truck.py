import simpy
from typing import Tuple


class Truck:
    def __init__(self, env : simpy.Environment, capacity_tons, data):
        self.env: simpy.Environment = env
        self.capacity_tons: float = capacity_tons
        self.data: dict = data

        self.tons: float = 0
        self.route = None

        self.positions: list[Tuple] = []

    def get_tons(self) -> float:
        return self.tons

    def assign_tons(self, tons: float) -> None:
        self.tons: float = tons

    def fill_tons(self) -> None:
        self.tons: float = self.capacity_tons

    def set_route(self, route) -> None:
        self.route = route

    def move(self):
        self.report_position()

        while self.route:
            yield self.env.process(self.route(self))
            self.report_position()

    def report_position(self) -> None:
        pass

    def add_position(self, place: str, current_time: float) -> None:
        self.positions.append((place, current_time))

    def find_position_at_time(self, time: float):
        k = len(self.positions)

        if time < self.positions[0][1]:
            return self.positions[0][0], self.positions[0][0], 0

        for i in range(1, k):
            if time >= self.positions[i - 1][1] and time <= self.positions[i][1]:
                prop = (time - self.positions[i-1][1]) / (self.positions[i][1] - self.positions[i-1][1])
                return (self.positions[i-1][0], self.positions[i][0], prop)

        return self.positions[-1][0], self.positions[-1][0], 0