import pygame as pg

import numpy as np


class InvalidAttributeError(Exception):
    pass


class Part(object):
    watch_attributes = []
    color = (255, 255, 255)
    contrast_color = (0, 0, 0)

    def __init__(self):
        self.updated = {attribute: True for attribute in self.watch_attributes}
        self.connected_parts = []
        self.overdetermined = False

    def is_solved(self):
        return all(self.updated.values())

    def is_reset(self):
        return not (any(self.updated.values()) or self.overdetermined)

    def set(self, attribute, value):
        if not (attribute in self.__dict__ and attribute in self.updated):
            raise InvalidAttributeError()
        if self.updated[attribute]:
            self.overdetermined = True
        else:
            self.updated[attribute] = True
        self.__dict__[attribute] = value

    def reset(self):
        if self.is_reset():
            return
        self.overdetermined = True
        self.updated = {attribute: False for attribute in self.watch_attributes}
        for connected_part in self.connected_parts:
            connected_part.reset()

    def solve_constraints(self):
        raise NotImplementedError()

    def solve_constraints_recursive(self):
        self.solve_constraints()
        for connected_part in self.connected_parts:
            if connected_part.is_solved():
                connected_part.solve_constraints()
            connected_part.solve_constraints_recursive()


class Wheel(Part):
    watch_attributes = ['rotation']
    resolution = 256

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


class GearWheel(Part):
    watch_attributes = ['rotation']
    tooth_width = 16
    tooth_height = 8

    def __init__(self, teeth, position):
        super().__init__()
        self.teeth = teeth
        self.postion = position
        self.rotation = 0
        self.circumference = self.teeth * self.tooth_width
        self.radius = self.circumference / (2 * np.pi)
        self._init_polygons()

    def _init_polygons(self):
        lower_radius = self.radius - self.tooth_height / 2
        upper_radius = self.radius + self.tooth_height / 2
        radial_tooth_width = 2 * np.pi * (self.tooth_width / self.circumference)
        point_radi = [lower_radius, lower_radius, upper_radius, upper_radius]
        point_offsets = [radial_tooth_width * s for s in [0, 0.4, 0.5, 0.9]]
        teeth = []
        for i in range(self.teeth):
            for r, offset in zip(point_radi, point_offsets):
                teeth.append(
                    np.array([
                        np.sin(i / self.teeth * np.pi * 2 + offset) * r,
                        np.cos(i / self.teeth * np.pi * 2 + offset) * r,
                        1
                    ])
                )
        self.polygons = [(self.color, teeth)]

    def solve_constraints(self):
        pass


class Motor(Wheel):

    def __init__(self, speed, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = speed

    def solve_constraints(self):
        rotation = pg.time.get_ticks() * self.speed
        self.set('rotation', rotation)
