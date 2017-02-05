import pygame as pg
import numpy as np

from systems import RenderSystem, MechanicsSolver
from mechanical_parts import Motor, GearWheel

SCREEN_SIZE = (1400, 900)

def main_loop(screen, systems):
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
        for system in systems:
            system.update()
        pg.display.flip()

def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    render_system = RenderSystem(screen)
    mechanical_solver = MechanicsSolver()
    wheel = Motor(0.001, 100, np.array([200, 200]))
    gear = GearWheel(25, np.array([400, 200]))
    render_system.register(wheel)
    render_system.register(gear)
    mechanical_solver.register(wheel)
    main_loop(screen, [render_system, mechanical_solver])

if __name__ == '__main__':
    main()
