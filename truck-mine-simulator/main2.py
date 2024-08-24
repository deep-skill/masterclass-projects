import simpy
import matplotlib.pyplot as plt
from mine import Mine


if __name__ == "__main__":
    env = simpy.Environment()
    mine = Mine(env)
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


    # 2 Camiones grandes diamante
    print('2 camiones grandes hacia diamante')

    camiones = []
    tonelaje = []
    eficiencia = []

    print('# Camiones chicos, Tonelaje, Eficiencia')

    for i in range(11):
        env = simpy.Environment()
        mine = Mine(env, camiones_chicos_diamante=i, camiones_grandes_diamante=2)
        mine.start_simulation()

        total_time = 8 * 60 * 60
        env.run(until=total_time)

        using_time = mine.pala_dia.data['using_time']

        camiones.append(i)
        tonelaje.append(mine.placas.data['reserved_tons'])
        eficiencia.append(mine.pala_dia.data['using_time'] / total_time * 100)

        print(i, mine.placas.data['reserved_tons'], using_time / total_time * 100)

    plt.xlabel('Numero de camiones chicos')
    plt.ylabel('Tonelaje')
    plt.title('Tonelaje vs Numero de camiones chicos (2 camiones grandes)')
    plt.xticks([i for i in range(11)])
    plt.plot(camiones, tonelaje, color='orange')
    plt.scatter(camiones, tonelaje, color='orange')
    plt.show()

    print('')

    plt.xlabel('Numero de camiones chicos')
    plt.ylabel('Eficiencia')
    plt.title('Eficiencia vs Numero de camiones chicos (2 camiones grandes)')
    plt.xticks([i for i in range(11)])
    plt.plot(camiones, eficiencia, color='orange')
    plt.scatter(camiones, eficiencia, color='orange')
    plt.show()

    print('')

    #1 Camion grandes diamante

    print('1 camion grande hacia diamante')

    camiones = []
    tonelaje = []
    eficiencia = []

    print('# Camiones chicos, Tonelaje, Eficiencia')

    for i in range(11):
      env = simpy.Environment()
      mine = Mine(env, camiones_chicos_diamante=i, camiones_grandes_diamante=1)
      mine.start_simulation()

      total_time = 8 * 60 * 60
      env.run(until=total_time)

      camiones.append(i)
      tonelaje.append(mine.placas.data['reserved_tons'])
      eficiencia.append(mine.pala_dia.data['using_time'] / total_time * 100)

      using_time = mine.pala_dia.data['using_time']
      print(i, mine.placas.data['reserved_tons'], using_time / total_time * 100)


    plt.xlabel('Numero de camiones chicos')
    plt.ylabel('Tonelaje')
    plt.title('Tonelaje vs Numero de camiones chicos (1 camion grande)')
    plt.xticks([i for i in range(11)])
    plt.plot(camiones, tonelaje, color='orange')
    plt.scatter(camiones, tonelaje, color='orange')
    plt.show()

    print('')

    plt.xlabel('Numero de camiones chicos')
    plt.ylabel('Eficiencia')
    plt.title('Eficiencia vs Numero de camiones chicos (1 camion grande)')
    plt.xticks([i for i in range(11)])
    plt.plot(camiones, eficiencia, color='orange')
    plt.scatter(camiones, eficiencia, color='orange')
    plt.show()
