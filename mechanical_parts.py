import pygame as pg

import numpy as np


class InvalidAttributeError(Exception):
    pass


class Part(object):
    watch_attributes = []

    def __init__(self):
        self.updated = {attribute: True for attribute in self.watch_attributes}

    def is_solved(self):
        return all(self.updated.values())

    def set(self, attribute, value):
        if not (attribute in self.__dict__ and attribute in self.updated):
            raise InvalidAttributeError()
        self.updated[attribute] = True
        self.__dict__[attribute] = value

    def reset(self):
        self.updated = {attribute: False for attribute in self.watch_attributes}


class Wheel(Part):
    resolution = 128
    color = (255, 255, 255)
    contrast_color = (0, 0, 0)

    def __init__(self, radius, position):
        super().__init__()
        self.radius = radius
        self.postion = position
        self.rotation = 0
        self._init_polygons()

    def _init_polygons(self):
        circle = [
            np.array([
                np.sin(i / self.resolution * np.pi * 2) * self.radius,
                np.cos(i / self.resolution * np.pi * 2) * self.radius,
                1
            ]) for i in range(self.resolution)
        ]
        indicator = [
            np.array([0, 0, 1]),
            np.array([0, self.radius * 0.95, 1]),
            np.array([np.sin(0.05) * self.radius * 0.95, np.cos(0.05) * self.radius * 0.95, 1]),
        ]
        self.polygons = [(self.color, circle), (self.contrast_color, indicator)]

    def solve_constraints(self):
        pass


class Motor(Wheel):
    watch_attributes = ['rotation']

    def __init__(self, speed, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = speed

    def solve_constraints(self):
        rotation = pg.time.get_ticks() * self.speed % (2 * np.pi)
        self.set('rotation', rotation)
