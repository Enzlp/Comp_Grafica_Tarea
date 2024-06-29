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
import pymunk

PERSPECTIVE_VIEW = 0
ORTOGRAPHIC_VIEW = 1


if __name__ == "__main__":
    width = 960
    height = 960
    window = pyglet.window.Window(width, height)
    controller = Controller()

    with open(Path(os.path.dirname(__file__)) / 'vertex_program.glsl') as f:
        vertex_source_code = f.read()

    with open(Path(os.path.dirname(__file__)) / 'fragment_program.glsl') as f:
        fragment_source_code = f.read()

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    pipeline =  pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    tablero_obj = tm.load(Path(os.path.dirname(__file__)) /'assets_obj/superficie.obj')
    tablero_obj.apply_translation(-tablero_obj.centroid)
    tablero_obj.apply_scale(2.0 /  tablero_obj.scale)
    tablero_vertex_list = tm.rendering.mesh_to_vertexlist(tablero_obj)
    tablero_gpu = pipeline.vertex_list_indexed(
            len(tablero_vertex_list[4][1]) // 3,
            GL.GL_TRIANGLES,
            tablero_vertex_list[3]
        )
    tablero_gpu.position[:] = tablero_vertex_list[4][1]

    flipper_obj = tm.load(Path(os.path.dirname(__file__))/"assets_obj/flipper_3.obj")
    flipper_obj.apply_scale(1.0/  flipper_obj.scale)
    flipper_vertex_list = tm.rendering.mesh_to_vertexlist(flipper_obj)
    flipper_gpu = pipeline.vertex_list_indexed(
            len(flipper_vertex_list[4][1]) // 3,
            GL.GL_TRIANGLES,
            flipper_vertex_list[3]
        )
    flipper_gpu.position[:] = flipper_vertex_list[4][1]

    #Espacio fisico
    space = pymunk.Space()


    @window.event
    def on_key_press(symbol, modifier):
        if(key.C == symbol):
            controller.change_view()
    @window.event
    def on_draw():
        GL.glClearColor(0, 0, 0, 1.0)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glEnable(GL.GL_DEPTH_TEST)
        window.clear()
        
        #Definimos perspectiva y camara de vista
        if(controller.view == PERSPECTIVE_VIEW):
            projection = tr.perspective(45, window.width/window.height, 0.001, 100).reshape(16, 1, order='F')
            camera_view = tr.lookAt(
                np.array([4,0,3]),
                np.array([0, 0, 0]), 
                np.array([0, 0, 1])
            ).reshape(16, 1, order='F')
        if(controller.view == ORTOGRAPHIC_VIEW): 
            camera_view = tr.lookAt(
                np.array([4,0,3]),
                np.array([0, 0, 0]), 
                np.array([0, 0, 1])
            ).reshape(16, 1, order='F')
            projection = tr.ortho(-2, 2, -2, 2, 0.001, 10.0).reshape(16, 1, order='F')

        pipeline.use()

        pipeline['color'] = [0.5, 0.5, 1]
        pipeline['transform'] = (tr.translate(0, 0, 0.0) @ tr.scale(2,2,2)).reshape(16,1,order='F')
        tablero_gpu.draw(pyglet.gl.GL_TRIANGLES)


    pyglet.app.run()