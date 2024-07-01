import trimesh as tm
import os
import sys
from pathlib import Path
import numpy as np
import pyglet
import pyglet.gl as GL
import trimesh as tm
from pyglet.window import key

#Import clases 
import aux_functions.transformations as tr
from classes.controller import *
from grafica.utils import load_pipeline


PERSPECTIVE_VIEW = 0
ORTOGRAPHIC_VIEW = 1


if __name__ == "__main__":

    width = 960
    height = 960
    window = pyglet.window.Window(width, height)

    controller = Controller()

    #Generamos los pipelines para los objetos
    pipeline = load_pipeline(
        Path(os.path.dirname(__file__)) / "vertex_program.glsl",
        Path(os.path.dirname(__file__)) / "fragment_program.glsl",
    )

    # Tablero
    tablero_obj = tm.load(Path(os.path.dirname(__file__)) /"assets_obj/superficie.obj")
    tablero_obj.apply_translation(-tablero_obj.centroid)
    tablero_obj.apply_scale(2.0 /  tablero_obj.scale)
    tablero_vertex_list = tm.rendering.mesh_to_vertexlist(tablero_obj)
    tablero_gpu = pipeline.vertex_list_indexed(
        len(tablero_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        tablero_vertex_list[3]
    )
    tablero_gpu.position[:] = tablero_vertex_list[4][1]
    # Paredes
    paredes_obj = tm.load(Path(os.path.dirname(__file__))/"assets_obj/paredes.obj")
    paredes_obj.apply_translation(-paredes_obj.centroid)
    paredes_obj.apply_scale(2.0 /  paredes_obj.scale)
    paredes_vertex_list = tm.rendering.mesh_to_vertexlist(paredes_obj)
    paredes_gpu = pipeline.vertex_list_indexed(
        len(paredes_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        paredes_vertex_list[3]
    )
    paredes_gpu.position[:] = paredes_vertex_list[4][1]
    # bumper_1 y 2
    bumper_obj = tm.load(Path(os.path.dirname(__file__)) /"assets_obj/bumper.obj")
    bumper_obj.apply_translation(-bumper_obj.centroid)
    bumper_obj.apply_scale(1.0 /  bumper_obj.scale)
    bumper_vertex_list = tm.rendering.mesh_to_vertexlist(bumper_obj)
    bumper_gpu = pipeline.vertex_list_indexed(
        len(bumper_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        bumper_vertex_list[3]
    )
    bumper_gpu.position[:] = bumper_vertex_list[4][1]
    bumper2_vertex_list = tm.rendering.mesh_to_vertexlist(bumper_obj)
    bumper2_gpu = pipeline.vertex_list_indexed(
        len(bumper2_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        bumper2_vertex_list[3]
    )
    bumper2_gpu.position[:] = bumper2_vertex_list[4][1]
    #spaceship 1 y 2
    spaceship_obj = tm.load(Path(os.path.dirname(__file__)) /"assets_obj/RocketShip.obj")
    spaceship_obj.apply_translation(-spaceship_obj.centroid)
    spaceship_obj.apply_scale(1.0 /  spaceship_obj.scale)
    spaceship_vertex_list = tm.rendering.mesh_to_vertexlist(spaceship_obj)
    spaceship_gpu = pipeline.vertex_list_indexed(
        len(spaceship_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        spaceship_vertex_list[3]
    )
    spaceship_gpu.position[:] = spaceship_vertex_list[4][1]
    spaceship2_vertex_list = tm.rendering.mesh_to_vertexlist(spaceship_obj)
    spaceship2_gpu = pipeline.vertex_list_indexed(
        len(spaceship2_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        spaceship2_vertex_list[3]
    )
    spaceship2_gpu.position[:] = spaceship2_vertex_list[4][1] 

    #Objetos dinamicos
    #Flipper 1 y 2
    flipper_obj = tm.load(Path(os.path.dirname(__file__)) /"assets_obj/flipper_3.obj")
    flipper_obj.apply_scale(1.0/  flipper_obj.scale)
    flipper_vertex_list = tm.rendering.mesh_to_vertexlist(flipper_obj)
    flipper_gpu = pipeline.vertex_list_indexed(
        len(flipper_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        flipper_vertex_list[3]
    )
    flipper_gpu.position[:] = flipper_vertex_list[4][1]
    flipper2_vertex_list = tm.rendering.mesh_to_vertexlist(flipper_obj)
    flipper2_gpu = pipeline.vertex_list_indexed(
        len(flipper2_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        flipper2_vertex_list[3]
    )
    flipper2_gpu.position[:] = flipper2_vertex_list[4][1]
    #Pelota
    pelota_obj = tm.load(Path(os.path.dirname(__file__)) /"assets_obj/sphere.off")
    pelota_obj.apply_scale(1.0/  pelota_obj.scale)
    pelota_vertex_list = tm.rendering.mesh_to_vertexlist(pelota_obj)
    pelota_gpu = pipeline.vertex_list_indexed(
        len(pelota_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        pelota_vertex_list[3]
    )
    pelota_gpu.position[:] = pelota_vertex_list[4][1]

    
    @window.event
    def on_key_press(symbol, modifier):
        # print(symbol)
        if(key.C == symbol):
            controller.change_view()
        if(key.A == symbol):
            controller.start_left_flipper()
        if(key.D == symbol):
            controller.start_right_flipper()
    @window.event
    def on_key_release(symbol, modifier):
        if(key.A == symbol):
            controller.stop_left_flipper()
        if(key.D == symbol):
            controller.stop_right_flipper()

    # GAME LOOP
    @window.event
    def on_draw():
        GL.glClearColor(0, 0, 0, 1.0)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        window.clear()
        pipeline.use()
        
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

        #Dibujamos el tablero
        pipeline['rotation'] = tr.rotationX(np.pi/2).reshape(16, 1, order='F')
        pipeline['translate'] = tr.translate(0, 0, 0).reshape(16, 1, order='F')
        pipeline['scale'] = tr.scale(2, 2, 2).reshape(16, 1, order='F')
        pipeline['view'] = camera_view
        pipeline['projection'] = projection
        pipeline['color'] = [0.5, 0.5, 1]
        tablero_gpu.draw(GL.GL_TRIANGLES)

        #Dibujamos las paredes
        pipeline['rotation'] = tr.rotationX(np.pi/2).reshape(16, 1, order='F')
        pipeline['translate'] = tr.translate(-0.14, 0, -0.08).reshape(16, 1, order='F')
        pipeline['scale'] = tr.scale(2.1, 2.1, 2.1).reshape(16, 1, order='F')
        pipeline['color'] = [0.5, 0.5, 0.5]
        paredes_gpu.draw(GL.GL_TRIANGLES)

        #Dibujamos los bumpers
        pipeline['rotation'] = tr.rotationX(np.pi/2).reshape(16, 1, order='F')
        pipeline['translate'] = tr.translate(-1.5, 0, 1).reshape(16, 1, order='F')
        pipeline['scale'] = tr.scale(0.4,0.4,0.4).reshape(16, 1, order='F')
        pipeline['color'] = [1, 1, 0.5]
        bumper_gpu.draw(GL.GL_TRIANGLES)
        pipeline['translate'] = tr.translate(1.5, 0, -0.5).reshape(16, 1, order='F')
        bumper2_gpu.draw(GL.GL_TRIANGLES)

        #Dibujamos las naves espaciales
        pipeline['rotation'] = tr.rotationX(0).reshape(16, 1, order='F')
        pipeline['translate'] = tr.translate(-2.8,1,0).reshape(16, 1, order='F')
        pipeline['scale'] = tr.scale(0.8,0.8,0.8).reshape(16, 1, order='F')
        pipeline['color'] = [0.2,0.2,0.2]
        spaceship_gpu.draw(GL.GL_TRIANGLES)
        pipeline['translate'] = tr.translate(-2.8,-1,0).reshape(16, 1, order='F')
        spaceship2_gpu.draw(GL.GL_TRIANGLES)

        #Dibujamos las piezas moviles
        #Pelota
        pelota_matrix_rotation = tr.rotationX(0)
        pipeline['scale'] = tr.scale(0.4,0.4,0.4).reshape(16, 1, order='F')
        pipeline['rotation'] = pelota_matrix_rotation.reshape(16, 1, order='F')
        pipeline['translate'] = tr.translate(3.2,1.9,0).reshape(16, 1, order='F')
        pipeline['color'] = [1, 1, 1]
        pelota_gpu.draw(GL.GL_TRIANGLES)
        
        #Movimiento paletas
        if(controller.right_flipper_rotating):
            controller.alpha_1 += 0.1
        else:
            if controller.alpha_1>0:
                controller.alpha_1 -= 0.1

        if(controller.left_flipper_rotating):
            controller.alpha_2 -= 0.1
        else:
            if controller.alpha_2<0:
                controller.alpha_2 += 0.1
                
        #Flippers
        matrix_rotation = tr.rotationX(np.pi/2) @ tr.rotationY(controller.alpha_1)
        pipeline['scale'] = tr.scale(0.4,0.4,0.4).reshape(16, 1, order='F')
        pipeline['rotation'] = matrix_rotation.reshape(16, 1, order='F')
        pipeline['translate'] = tr.translate(4, 0, 1).reshape(16, 1, order='F')
        pipeline['color'] = [0.5, 1, 0.5]
        flipper_gpu.draw(GL.GL_TRIANGLES)
        matrix_rotation = tr.rotationX(np.pi/2)
        matrix_rotation2 = tr.rotationX(np.pi/2) @ tr.rotationY(controller.alpha_2)
        pipeline['rotation'] = matrix_rotation2.reshape(16, 1, order='F')
        pipeline['translate'] = tr.translate(4,0,-0.5).reshape(16, 1, order='F')
        flipper2_gpu.draw(GL.GL_TRIANGLES)
        

    # aquí comienza pyglet a ejecutar su loop.
    pyglet.app.run()