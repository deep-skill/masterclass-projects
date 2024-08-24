import simpy
import copy
from typing import List
from truck import Truck
from shovel import Shovel
from dump import Dump
from placa import Placa
from cruce import Cruce
from time_function import obtain_dict_of_time_functions


class Mine:
    def __init__(self, env : simpy.Environment, camiones_chicos_diamante=6, camiones_chicos_ccc=2, camiones_grandes_ele=2, camiones_grandes_diamante=2) -> None:
        self.env: simpy.Environment = env
        self.camiones_chicos_diamante: int = camiones_chicos_diamante
        self.camiones_chicos_ccc: int = camiones_chicos_ccc
        self.camiones_grandes_ele: int = camiones_grandes_ele
        self.camiones_grandes_diamante: int = camiones_grandes_diamante

        self.tf_dict = obtain_dict_of_time_functions('funciones_tiempo_tajo_raul.txt')

        self.cruce_dispatch = Cruce(env, capacity=1, data={'name' : 'Dispatch'})
        self.cruce_tacari = Cruce(env, capacity=1, data={'name' : 'Tacari'})

        self.pala_ele = Shovel(env, capacity=1, data={'name' : 'L'})
        self.pala_ccc = Shovel(env, capacity=1, data={'name' : 'C'})
        self.pala_dia = Shovel(env, capacity=1, data={'name' : 'Diamante'})

        self.botadero_hanancocha = Dump(env, capacity=6, data={'name' : 'Hanancocha'})
        self.botadero_rumiallana = Dump(env, capacity=6, data={'name' : 'Rumiallana'})

        self.placas = Placa(env, capacity=6, data={'name' : 'Placas'})

        self.number_of_trucks = 0
        self.trucks: List[Truck] = []

        self.PLAN_DIA = 0
        self.PLAN_CCC = 1
        self.PLAN_ELE = 2

        self.SMALL = 0
        self.BIG = 1

    def get_time(self, id_function):
        return self.tf_dict[id_function].get_random_time()

    def get_timeout(self, id_function):
        return self.env.timeout(self.get_time(id_function))

    def init_to_crudis_route(self, truck : Truck):
        truck.add_position("INIT", self.env.now)

        yield self.get_timeout('T01B')

        truck.add_position("11", self.env.now)

        yield self.get_timeout('T02B')

        yield self.cruce_dispatch.work_process(truck, start="A", end="B",time=10)

        if truck.data['direction'] == self.PLAN_ELE:
            truck.set_route(self.crudis_to_ele_route)
        else:
            truck.set_route(self.crudis_to_tacari_route)

    def crudis_to_tacari_route(self, truck : Truck):
        yield self.get_timeout('T03B')
        yield self.cruce_tacari.work_process(truck, start="A", end="B", time=10)

        if truck.data['direction'] == self.PLAN_DIA:

            truck.set_route(self.tacari_to_diamante_route)
        else:
            truck.set_route(self.tacari_to_ccc_route)

    def tacari_to_ccc_route(self, truck : Truck):
        yield self.get_timeout('T04B')
        yield self.get_timeout('T13B')

        yield self.pala_ccc.work_process(truck, self.get_time('TCCC'))

        truck.set_route(self.ccc_to_rumiallana_route)

    def ccc_to_rumiallana_route(self, truck : Truck):
        yield self.get_timeout('T13S')

        yield self.get_timeout('T04S')

        yield self.cruce_tacari.work_process(truck, start="B", end="C", time=10)

        yield self.get_timeout('T08S')

        yield self.botadero_rumiallana.work_process(truck, self.get_time('TRUM'))

        truck.set_route(self.rumiallana_to_tacari_route)

    def rumiallana_to_tacari_route(self, truck : Truck):
        yield self.get_timeout('T08B')

        yield self.cruce_tacari.work_process(truck, start="C", end="B", time=10)

        truck.set_route(self.tacari_to_ccc_route)

    def tacari_to_diamante_route(self, truck : Truck):
        yield self.get_timeout('T04B')

        yield self.get_timeout('T05B')
        yield self.get_timeout('T06B')
        yield self.get_timeout('T07B')

        yield self.pala_dia.work_process(truck, self.get_time('TDIA'))

        truck.set_route(self.diamante_to_placa_route)

    def diamante_to_placa_route(self, truck : Truck):
        yield self.get_timeout('T07S')
        yield self.get_timeout('T06S')
        yield self.get_timeout('T05S')

        yield self.get_timeout('T04S')

        yield self.cruce_tacari.work_process(truck, start="B", end="A", time=10)

        yield self.get_timeout('T03S')

        yield self.cruce_dispatch.work_process(truck, start="B", end="A", time=10)

        yield self.get_timeout('T09S')

        yield self.placas.work_process(truck, self.get_time('TSUP'))

        truck.set_route(self.placa_to_crudis_route)

    def placa_to_crudis_route(self, truck : Truck):
        yield self.get_timeout('T09B')

        yield self.cruce_dispatch.work_process(truck, start="A", end="B", time=10)

        truck.set_route(self.crudis_to_tacari_route)

    def crudis_to_ele_route(self, truck : Truck):
        yield self.get_timeout('T10B')

        yield self.pala_ele.work_process(truck, self.get_time('TELE'))

        truck.set_route(self.ele_to_hanancocha_route)

    def ele_to_hanancocha_route(self, truck : Truck):
        yield self.get_timeout('T10S')

        yield self.cruce_dispatch.work_process(truck, start="B", end="A", time=10)

        yield self.get_timeout('T11S')

        yield self.botadero_hanancocha.work_process(truck, self.get_time('THAN'))

        truck.set_route(self.hanancocha_to_crudis_route)

    def hanancocha_to_crudis_route(self, truck : Truck):
        yield self.get_timeout('T11B')

        yield self.cruce_dispatch.work_process(truck, start="A", end="B", time=10)

        truck.set_route(self.crudis_to_ele_route)

    def start_truck(self, truck):
        # Ruta inicial
        truck.set_route(self.init_to_crudis_route)

        # Iniciamos la simulacion
        self.env.process(truck.move())

    def generate_trucks(self, quantity, data, intermediate_time):
        if data['size'] == self.SMALL: capacity_tons = 100
        else: capacity_tons = 120

        for _ in range(quantity):
            self.number_of_trucks += 1
            current_data = copy.deepcopy(data)
            current_data['name'] = self.number_of_trucks

            truck = Truck(self.env, capacity_tons, current_data)
            self.trucks.append(truck)
            self.start_truck(truck)

            yield self.env.timeout(intermediate_time)

    def start_simulation(self):
        # Camiones grandes plan L
        data = {'size' : self.BIG, 'direction' : self.PLAN_ELE}
        self.env.process(self.generate_trucks(self.camiones_grandes_ele, data, 120))

        # Camiones grandes plan Diamante
        data = {'size' : self.BIG, 'direction' : self.PLAN_DIA}
        self.env.process(self.generate_trucks(self.camiones_grandes_diamante, data, 120))

        # Camiones chicos plan Diamante
        data = {'size' : self.SMALL, 'direction' : self.PLAN_DIA}
        self.env.process(self.generate_trucks(self.camiones_chicos_diamante, data, 120))

        # Camiones chicos plan C
        data = {'size' : self.SMALL, 'direction' : self.PLAN_CCC}
        self.env.process(self.generate_trucks(self.camiones_chicos_ccc, data, 120))

