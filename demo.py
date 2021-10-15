import math

import bpy
from utils import *

from mathutils import *
import random

frame_start = 1
total_frames = 150
bpy.context.scene.render.fps = 30
bpy.context.scene.frame_start = frame_start
bpy.context.scene.frame_end = total_frames

random.seed(1)

"""
Cube fractal
"""


def get_or_create_collection(name) -> bpy.types.Collection:
    col = bpy.data.collections.get(name)
    if not col:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def get_or_create_object(
        name: str,
        data,
        collection: bpy.types.Collection = None
) -> bpy.types.Object:
    obj = bpy.data.objects.get(name)
    if not obj:
        obj = bpy.data.objects.new(name, data)
        if not collection:
            collection = bpy.data.collections['Collection']
        collection.objects.link(obj)
    return obj


levels = 3


def get_num_objects(levels) -> int:
    return sum([6 ** i for i in range(levels)])


num_objects = get_num_objects(levels)

def world_matrix(pos: Vector, scale: float) -> Matrix:
    return (
        scale_matrix(scale, scale, scale) @
        Matrix.Translation(pos)
    )


def get_child_transforms(matrix: Matrix, t: float) -> [Matrix]:
    d = mix(1.0, 2.0, t)
    # scale = pow (1.3, t)
    scale = 1/3
    return [
        matrix @ world_matrix((d, 0, 0), scale),
        matrix @ world_matrix((0, d, 0), scale),
        matrix @ world_matrix((-d, 0, 0), scale),
        matrix @ world_matrix((0, -d, 0), scale),
        matrix @ world_matrix((0, 0, -d), scale),
        matrix @ world_matrix((0, 0, d), scale),
    ]


def build_object_transforms(t: float) -> [Matrix]:
    transforms = []

    def helper(current_transform: Matrix, level: int):
        if level == levels:
            return
        transforms.append(current_transform)

        time_factor = t if level == levels - 2 else 1.0
        new_transforms = get_child_transforms(current_transform, time_factor)
        for new_transform in new_transforms:
            helper(new_transform, level + 1)
    # helper(scale_matrix(t, t, t), 0)
    helper(Matrix.Identity(4), 0)

    return transforms


def setup():
    collection = get_or_create_collection('generated')
    mesh = bpy.data.meshes['Cube']

    for i in range(num_objects):
        get_or_create_object(f'obj-{i}', mesh, collection)


def frame_update(scene):
    frame = scene.frame_current
    t = frame / float(total_frames)

    transforms = build_object_transforms(t)
    print(len(transforms))
    for i in range(num_objects):
        obj = bpy.data.objects[f"obj-{i}"]
        obj.matrix_world = transforms[i]


setup()
bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(frame_update)
