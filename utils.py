import math
import numpy as np
import pygame

class object:
    def __init__(self, faces, corners):   
        self.faces = faces
        self.corners = corners
    def rotate_x(self, angle):
        mcosangle = math.cos(angle)
        msinangle = math.sin(angle)
        rotation_x = [[1, 0, 0],
                      [0, mcosangle, -msinangle],
                      [0, msinangle, mcosangle]]
        self.corners = [tuple(np.matmul(rotation_x, point)) for point in self.corners]

    def rotate_y(self, angle):
        mcosangle = math.cos(angle)
        msinangle = math.sin(angle)
        rotation_y = [[mcosangle, 0, -msinangle],
                      [0, 1, 0],
                      [msinangle, 0, mcosangle]]
        self.corners = [tuple(np.matmul(rotation_y, point)) for point in self.corners]

    def rotate_z(self, angle):
        mcosangle = math.cos(angle)
        msinangle = math.sin(angle)
        rotation_z = [[mcosangle, -msinangle, 0],
                      [msinangle, mcosangle, 0],
                      [0, 0, 1]]
        self.corners = [tuple(np.matmul(rotation_z, point)) for point in self.corners]

    def projected_points(self, cam_distance):
        return [lower_dimension(point, cam_distance) for point in self.corners]


    def draw(self, scene, cam_pos, color, position: tuple, scale, light_pos):
        light_pos = normalize(light_pos)
        cam_distance = distance(position, cam_pos) / 100

        self.reorder_faces_painter(cam_pos)
        projected_points = list(scalar_mult(self.projected_points(cam_distance), scale))
        transformed_points = [tuple(np.add(point, position[:2])) for point in projected_points]

        face_colors = [lighten_color(color, [self.corners[i] for i in face], light_pos) for face in self.faces]

        for ind, face in enumerate(self.faces):
            face_points = [transformed_points[index] for index in face]
            pygame.draw.polygon(scene, face_colors[ind], face_points)

    def rank_distances(self, cam_pos):
        face_distance_sums = []
        for face in self.faces:
            this_face_dist = 0
            for point_index in face:
                #this_face_dist += distance(cam_pos, self.corners[point_index])
                this_face_dist += self.corners[point_index][2]
            face_distance_sums.append(this_face_dist)
        return face_distance_sums

    def reorder_faces_painter(self, cam_pos):
        ranking = self.rank_distances(cam_pos)

        self.faces = [face for _, face in sorted(zip(ranking, self.faces))]

"""
class cube(object):
    def __init__(self):
        self.faces = [plane([(-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1)]),
                      plane([(-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1)]),
                      plane([(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1)]),
                      plane([(-1, -1, 1), (1, -1, 1), (1, -1, -1), (-1, -1, -1)]),
                      plane([(1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1)]),
                      plane([(-1, 1, 1), (1, 1, 1), (1, 1, -1), (-1, 1, -1)])]

"""

class cube(object):
    def __init__(self):
        self.corners = [(-1, 1, 1),
                        (-1, 1, -1),
                        (-1, -1, -1),
                        (-1, -1, 1),
                        (1, 1, 1),
                        (1, 1, -1),
                        (1, -1, -1),
                        (1, -1, 1)]
        self.faces = [(0, 3, 2, 1),
                      (4, 5, 6, 7),
                      (2, 3, 7, 6),
                      (0, 1, 5, 4),
                      (6, 5, 1, 2),
                      (3, 0, 4, 7)]

class pyramid(object):
    def __init__(self):
        self.corners = [(-1, -1, -1),
                        (-1, -1, 1),
                        (1, -1, 1),
                        (1, -1, -1),
                        (0, 1, 0)]
        self.faces = [(0, 1, 2, 3),
                      (0, 4, 1),
                      (1, 4, 2),
                      (2, 4, 3),
                      (3, 4, 0)]

class diamond(object):
    def __init__(self):
        self.corners = [(-1, 0, -1),
                        (-1, 0, 1),
                        (1, 0, 1),
                        (1, 0, -1),
                        (0, 2, 0),
                        (0, -2, 0)]
        self.faces = [(0, 4, 1),
                      (1, 4, 2),
                      (2, 4, 3),
                      (3, 4, 0),
                      (1, 5, 0),
                      (2, 5, 1),
                      (3, 5, 2),
                      (0, 5, 3)]

class custom(object):
    def __init__(self, in_file_str):
        self.corners = []
        self.faces = []
        scale_mult = 10
        if in_file_str == "cat.obj":
            scale_mult = 0.007
        with open(in_file_str, "r") as f:
            f_arr = f.read().splitlines()
        for line in f_arr:
            if line.startswith("v "):
                self.corners.append(tuple(map(lambda x: float(x) * scale_mult, line.split(' ')[1:]))[::-1])
            elif line.startswith("f"):
                line_cleanup = line[2:-1].split(" ")
                #print(line_cleanup)
                c_face = []
                for point in line_cleanup:
                    c_face.append((int(point.split("/")[0]) - 1))
                self.faces.append(tuple(c_face))


def magnitude(mat):
    return np.sqrt(np.dot(mat))

def distance(pa, pb):
    return np.linalg.norm(np.subtract(pa, pb))

def scalar_mult(mat, s):
    return tuple(np.array(mat) * s)

def normal_to_plane(points):
    v1 = np.subtract(points[1], points[0])
    v2 = np.subtract(points[2], points[0])
    vcross = np.cross(v1, v2)
    return tuple(vcross)

def normalize(vect):
    return tuple(np.divide(vect, np.sqrt(np.dot(vect, vect))))

def lower_dimension(point, cam_distance):
    z = 1/(cam_distance - point[2])
    projection_mat = [[z, 0, 0],
                      [0, z, 0]]
    return tuple(np.matmul(projection_mat, point))

def keep_color_bounded(color):
    res = []
    for channel in color:
        if channel > 255:
            res.append(255)
        elif channel < 0:
            res.append(0)
        else:
            res.append(channel)

    return tuple(res)

def lighten_color(color, face, light_pos):
    face_normal = normal_to_plane(face)
    inc = max(0.01, np.dot(light_pos, normalize(face_normal)))
    #print(np.dot(light_pos, face_normal))

    res = tuple(np.add(color, inc * 20))
    res = keep_color_bounded(res)

    return res