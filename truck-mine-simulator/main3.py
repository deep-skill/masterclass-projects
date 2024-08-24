import simpy
import pygame
import numpy as np
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

    pygame.font.init()

    my_font = pygame.font.SysFont('arial', 30)
    small_my_font = pygame.font.SysFont('arial', 20)

    ele_text = my_font.render('Pala L', False, (0, 0, 0))
    ccc_text = my_font.render('Pala C', False, (0, 0, 0))
    dia_text = my_font.render('Pala Diamante', False, (0, 0, 0))
    garaje_text = my_font.render('Garaje', False, (0, 0, 0))
    placas_text = my_font.render('Placas', False, (0, 0, 0))

    hanancocha_text = small_my_font.render('Botadero Hanancocha', False, (0, 0, 0))
    rumiallana_text = small_my_font.render('Botadero Rumiallana', False, (0, 0, 0))

    WIDTH = 900
    HEIGHT = 600

    BG_COLOR = (222, 249, 196)
    CIRCLE_COLOR = (255, 0, 0)

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    running_game = True

    local_positions = { "INIT" : (623, 387),
                        "11" : (683, 370),
                        "Hanancocha" : (718, 546),
                        "DispatchA" : (663, 248),
                        "DispatchB" : (646, 230),
                        "L" : (712, 173),
                        "TacariA" : (318, 279),
                        "TacariB" : (305, 261),
                        "TacariC" : (295, 276),
                        "Rumiallana" : (141, 415),
                        "C" : (249, 72),
                        "Diamante" : (625, 59),
                        "Placas" : (548, 306)
                        }

    edges = [("INIT", "11"),
             ("11", "DispatchA"),
             ("DispatchB", "L"),
             ("DispatchB", "TacariA"),
             ("DispatchA", "Placas"),
             ("11", "Hanancocha"),
             ("TacariB", "C"),
             ("TacariB", "Diamante"),
             ("TacariC", "Rumiallana"),
    ]

    local_circles = { "INIT" : ((623, 387), 15, (230, 131, 105)),
                      "11" : ((683, 370), 5, (230, 131, 105)),
                      "L" : ((712, 173), 15, (150, 201, 244)),
                      "C" : ((249, 72), 15, (150, 201, 244)),
                      "Diamante" : ((625, 59), 15, (150, 201, 244)),
                      "Rumiallana" : ((141, 415), 15, (233, 196, 106)),
                      "Hanancocha" : ((718, 546), 15, (233, 196, 106)),
                      "Placas" : ((548, 306), 15, (255, 177, 177)),
                      "Tacari" : ((305, 271), 18, (247, 249, 242)),
                      "Dispatch" : ((653, 237), 18, (247, 249, 242))
    }

    # print(mine.trucks[0].find_position_at_time(10))

    clock = pygame.time.Clock()
    current_time = 0
    dt = 0.2

    pygame.display.set_caption("Truck mine simulation")

    while running_game:
        current_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)

        WIN.fill(BG_COLOR)

        for name, position in local_positions.items():
            pygame.draw.circle(WIN, CIRCLE_COLOR, position, 4)

        for start, end in edges:
            color = (64, 93, 114)
            pygame.draw.line(WIN, color, local_positions[start], local_positions[end])

        for name, position in local_circles.items():
            pos, radius, color = position
            pygame.draw.circle(WIN, (0, 0, 0), pos, radius * 1.2)
            pygame.draw.circle(WIN, color, pos, radius)

        for truck in mine.trucks:
            #print(current_time, end='')
            start, end, prop = truck.find_position_at_time(current_time)

            p_start = np.array(local_positions[start])
            p_end = np.array(local_positions[end])

            current_pos = p_start + prop * (p_end - p_start)

            color = (19, 24, 66)
            radius = 5

            if truck.data['size'] == mine.BIG:
                color = (169, 29, 58)
                radius *= 1.5

            pygame.draw.circle(WIN, color, current_pos, radius)

        WIN.blit(ele_text, (750, 150))
        WIN.blit(ccc_text, (210, 20))
        WIN.blit(dia_text, (650, 40))

        WIN.blit(hanancocha_text, (518, 560))
        WIN.blit(rumiallana_text, (60, 445))

        WIN.blit(garaje_text, (580, 410))
        WIN.blit(placas_text, (448, 326))

        pygame.display.update()

    pygame.quit()
