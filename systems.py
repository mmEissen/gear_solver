from pygame import draw
import numpy as np


class RenderSystem(object):

    def __init__(self, surface):
        self.surface = surface
        self.view = np.matrix([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ])
        self.render_objects = []

    def _transformation_matrix(self, render_object):
        rotation = render_object.rotation
        translation = render_object.postion
        rot_matrix = np.matrix([
            [np.cos(rotation), -np.sin(rotation), 0],
            [np.sin(rotation),  np.cos(rotation), 0],
            [               0,                 0, 1]
        ])
        trans_matrix = np.matrix([
            [1, 0, translation[0]],
            [0, 1, translation[1]],
            [0, 0,              1]
        ])
        return trans_matrix * rot_matrix

    def register(self, render_object):
        self.render_objects.append(render_object)

    def update(self):
        self.surface.fill((100, 100, 100))
        for render_object in self.render_objects:
            for color, polygon in render_object.polygons:
                matrix = self._transformation_matrix(render_object)
                transformed_polygon = [np.squeeze(np.asarray(v * matrix.transpose()))
                                       for v in polygon]
                points = [point[:-1] for point in transformed_polygon]
                draw.polygon(self.surface, color, points)


class MechanicsSolver(object):

    def __init__(self):
        self.root_parts = []

    def register(self, mechanical_part):
        self.root_parts.append(mechanical_part)

    def update(self):
        for root_part in self.root_parts:
            root_part.reset()
        for root_part in self.root_parts:
            root_part.solve_constraints()
