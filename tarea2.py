import trimesh as tm
import os
import sys
from pathlib import Path
import numpy as np
import pyglet
import pyglet.gl as GL
import trimesh as tm
from pyglet.window import key

#Import clases propias
import aux_functions.transformations as tr
from classes.controller import *
from classes.models import *
from grafica.utils import load_pipeline

PERSPECTIVE_VIEW = 0
ORTOGRAPHIC_VIEW = 1


if __name__ == "__main__":
    width = 960
    height = 960
    window = pyglet.window.Window(width, height)
    
    
    #Scene pipeline
    scene_pipeline = load_pipeline(
        Path(os.path.dirname(__file__)) / "vertex_program.glsl",
        Path(os.path.dirname(__file__)) / "fragment_program.glsl",
    )
    
    vertex_lists = {}

    @window.event
    def on_draw():
        GL.glClearColor(0, 0, 0, 1.0)
        window.clear()

    pyglet.app.run()