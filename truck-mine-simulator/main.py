import simpy
import matplotlib.pyplot as plt
from mine import Mine


if __name__ == "__main__":
    env = simpy.Environment()
    
    mine = Mine(env,
                camiones_chicos_diamante=6, 
                camiones_chicos_ccc=2, 
                camiones_grandes_ele=2, 
                camiones_grandes_diamante=2)
    
    mine.start_simulation()

    total_time = 8 * 60 * 60
    env.run(until=total_time)

    print("")
    print("")
    mine.botadero_hanancocha.report()
    mine.botadero_rumiallana.report()
    mine.placas.report()
    mine.pala_ccc.report()
    mine.pala_ele.report()
    mine.pala_dia.report()

