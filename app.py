
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
import aux_functions.scene_graphs as sg

PERSPECTIVE_VIEW = 0
ORTOGRAPHIC_VIEW = 1


if __name__ == "__main__":

    window = pyglet.window.Window(960, 960)

    controller = Controller()

    @window.event
    def on_key_press(symbol, modifier):
        # print(symbol)
        if(key.C == symbol):
            controller.change_view()
        if(key.SPACE == symbol):
            controller.change_view()


   #Generamos el tablero
    tablero = tm.load("assets/superficie.obj")
    tablero.apply_translation(-tablero.centroid)
    tablero.apply_scale(2.0 / tablero.scale)


    with open(Path(os.path.dirname(__file__)) / "vertex_program.glsl") as f:
        vertex_source_code = f.read()

    with open(Path(os.path.dirname(__file__)) / "fragment_program.glsl") as f:
        fragment_source_code = f.read()

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    tablero_pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    tablero_vertex_list = tm.rendering.mesh_to_vertexlist(tablero)

    tablero_gpu = tablero_pipeline.vertex_list_indexed(
        len(tablero_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        tablero_vertex_list[3]
    )
    tablero_gpu.position[:] = tablero_vertex_list[4][1]

    #Generamos las paredes
    paredes = tm.load("assets/paredes.obj")
    paredes.apply_translation(-paredes.centroid)
    paredes.apply_scale(2.0 /  paredes.scale)

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    paredes_pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    paredes_vertex_list = tm.rendering.mesh_to_vertexlist(paredes)

    paredes_gpu = paredes_pipeline.vertex_list_indexed(
        len(paredes_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        paredes_vertex_list[3]
    )
    paredes_gpu.position[:] = paredes_vertex_list[4][1]

        #Generamos los obstaculos en el tablero
    #Primer Bumper
    bumper_1 = tm.load("assets/bumper.obj")
    bumper_1.apply_translation(-bumper_1.centroid)
    bumper_1.apply_scale(1.0 /  bumper_1.scale)

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    bumper_1_pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    bumper_1_vertex_list = tm.rendering.mesh_to_vertexlist(bumper_1)

    bumper_1_gpu = bumper_1_pipeline.vertex_list_indexed(
        len(bumper_1_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        bumper_1_vertex_list[3]
    )
    bumper_1_gpu.position[:] = bumper_1_vertex_list[4][1]

    #Segundo Bumper
    bumper_2 = tm.load("assets/bumper.obj")
    bumper_2.apply_translation(-bumper_2.centroid)
    bumper_2.apply_scale(1.0 /  bumper_2.scale)

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    bumper_2_pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    bumper_2_vertex_list = tm.rendering.mesh_to_vertexlist(bumper_2)

    bumper_2_gpu = bumper_2_pipeline.vertex_list_indexed(
        len(bumper_2_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        bumper_2_vertex_list[3]
    )
    bumper_2_gpu.position[:] = bumper_2_vertex_list[4][1]

    #flipper_1
    flipper_1 = tm.load("assets/flipper.obj")
    flipper_1.apply_translation(-flipper_1.centroid)
    flipper_1.apply_scale(1.0 /  flipper_1.scale)

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    flipper_1_pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    flipper_1_vertex_list = tm.rendering.mesh_to_vertexlist(flipper_1)
    flipper_1_gpu = flipper_1_pipeline.vertex_list_indexed(
            len(flipper_1_vertex_list[4][1]) // 3,
            GL.GL_TRIANGLES,
            flipper_1_vertex_list[3]
        )
    flipper_1_gpu.position[:] = flipper_1_vertex_list[4][1]

    #flipper_2
    flipper_2 = tm.load("assets/flipper.obj")
    flipper_2.apply_translation(-flipper_2.centroid)
    flipper_2.apply_scale(1.0 /  flipper_2.scale)

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    flipper_2_pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    flipper_2_vertex_list = tm.rendering.mesh_to_vertexlist(flipper_2)
    flipper_2_gpu = flipper_2_pipeline.vertex_list_indexed(
            len(flipper_2_vertex_list[4][1]) // 3,
            GL.GL_TRIANGLES,
            flipper_2_vertex_list[3]
        )
    flipper_2_gpu.position[:] = flipper_2_vertex_list[4][1]

    # GAME LOOP
    @window.event
    def on_draw():
        GL.glClearColor(0, 0, 0, 1.0)
        window.clear()
        
        #Definimos perspectiva y camara de vista
        if(controller.view == PERSPECTIVE_VIEW):
            projection = tr.perspective(45, window.width/window.height, 0.001, 100).reshape(16, 1, order='F')
            camera_view = tr.lookAt(
                np.array([3,3,3]),
                np.array([0, 0, 0]), 
                np.array([0, 0, 1])
            ).reshape(16, 1, order='F')
        if(controller.view == ORTOGRAPHIC_VIEW): 
            camera_view = tr.lookAt(
                np.array([3,3,3]),
                np.array([0, 0, 0]), 
                np.array([0, 0, 1])
            ).reshape(16, 1, order='F')
            projection = tr.ortho(-2, 2, -2, 2, 0.001, 10.0).reshape(16, 1, order='F')

        #Dibujamos el tablero
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        tablero_pipeline.use()
        tablero_gpu.draw(GL.GL_TRIANGLES)

        tablero_pipeline['translate'] = tr.translate(0, 0, 0).reshape(16, 1, order='F')
        #Matriz de rotation final
        rotation_X = tr.rotationX(np.pi/2)
        rotation_Z = tr.rotationY(np.pi/4)
        tablero_pipeline['rotation'] = np.dot(rotation_X, rotation_Z).reshape(16, 1, order='F')
        tablero_pipeline['scale'] = tr.scale(2, 2, 2).reshape(16, 1, order='F')

        tablero_pipeline['view'] = camera_view
        tablero_pipeline['projection'] = projection
        tablero_pipeline['color'] = [0.5, 0.5, 1]

        #Dibujamos las paredes
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        paredes_pipeline.use()
        paredes_gpu.draw(GL.GL_TRIANGLES)

        paredes_pipeline['translate'] = tr.translate(-0.145, 0, -0.08).reshape(16, 1, order='F')
        paredes_pipeline['rotation'] = np.dot(rotation_X, rotation_Z).reshape(16, 1, order='F')
        paredes_pipeline['scale'] = tr.scale(2.1, 2.1, 2.1).reshape(16, 1, order='F')
        paredes_pipeline['view'] = camera_view
        paredes_pipeline['projection'] = projection
        paredes_pipeline['color'] = [0.5, 0.5, 0.5]
        #Dibujamos los obstaculos
        #Dibujamos el primer bumper
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        bumper_1_pipeline.use()
        bumper_1_gpu.draw(GL.GL_TRIANGLES)

        bumper_1_pipeline['translate'] = tr.translate(-1.5, 0, 1).reshape(16, 1, order='F')
        bumper_1_pipeline['rotation'] = np.dot(rotation_X, rotation_Z).reshape(16, 1, order='F')
        bumper_1_pipeline['scale'] = tr.scale(0.4,0.4,0.4).reshape(16, 1, order='F')
        bumper_1_pipeline['view'] = camera_view
        bumper_1_pipeline['projection'] = projection
        bumper_1_pipeline['color'] = [1, 1, 0.5]

        #Dibujamos el segundo bumper
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        bumper_2_pipeline.use()
        bumper_2_gpu.draw(GL.GL_TRIANGLES)

        bumper_2_pipeline['translate'] = tr.translate(1.5, 0, -0.5).reshape(16, 1, order='F')
        bumper_2_pipeline['rotation'] = np.dot(rotation_X, rotation_Z).reshape(16, 1, order='F')
        bumper_2_pipeline['scale'] = tr.scale(0.4,0.4,0.4).reshape(16, 1, order='F')
        bumper_2_pipeline['view'] = camera_view
        bumper_2_pipeline['projection'] = projection
        bumper_2_pipeline['color'] = [1, 1, 0.5]

        #Dibujamos el primer flipper
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        flipper_1_pipeline.use()
        flipper_1_gpu.draw(GL.GL_TRIANGLES)

        matrix_rotation = tr.rotationX(np.pi/2)
        flipper_1_pipeline['scale'] = tr.scale(0.4,0.4,0.4).reshape(16, 1, order='F')
        flipper_1_pipeline['rotation'] = matrix_rotation.reshape(16, 1, order='F')
        flipper_1_pipeline['translate'] = tr.translate(2.5, 0, -3).reshape(16, 1, order='F')

        flipper_1_pipeline['view'] = camera_view
        flipper_1_pipeline['projection'] = projection
        flipper_1_pipeline['color'] = [0.5, 1, 0.5]

        #Segundo flipper
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        flipper_2_pipeline.use()
        flipper_2_gpu.draw(GL.GL_TRIANGLES)

        matrix_rotation = tr.rotationX(np.pi/2) @ tr.rotationY(np.pi/1.6)
        flipper_2_pipeline['scale'] = tr.scale(0.4,0.4,0.4).reshape(16, 1, order='F')
        flipper_2_pipeline['rotation'] = matrix_rotation.reshape(16, 1, order='F')
        flipper_2_pipeline['translate'] = tr.translate(0.4,0,4).reshape(16, 1, order='F')
        flipper_2_pipeline['view'] = camera_view
        flipper_2_pipeline['projection'] = projection
        flipper_2_pipeline['color'] = [0.5, 1, 0.5]

    # aquí comienza pyglet a ejecutar su loop.
    pyglet.app.run()