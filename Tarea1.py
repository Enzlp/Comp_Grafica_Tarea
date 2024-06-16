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

    #Usamos la clase objeto para crear los objetos a graficar
    #Generamos los objetos estaticos
    tablero = Object_Static("superficie.obj",2.0)
    paredes = Object_Static("paredes.obj",2.0)
    bumper_1 = Object_Static("bumper.obj",1.0)
    bumper_2 = Object_Static("bumper.obj",1.0)
    spaceship_1 = Object_Static("RocketShip.obj",1.0)
    spaceship_2 = Object_Static("RocketShip.obj",1.0)

    #Creamos los objetos dinamicos
    flipper_1 = Flipper()
    flipper_2 = Flipper()
    pelota = Pelota()


    # GAME LOOP
    @window.event
    def on_draw():
        GL.glClearColor(0, 0, 0, 1.0)
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

        #Dibujamos el tablero
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        tablero_translate = tr.translate(0, 0, 0)
        tablero_rotation = tr.rotationX(np.pi/2) 
        tablero_scale = tr.scale(2, 2, 2)
        tablero_color = [0.5, 0.5, 1]
        tablero.set_pipeline(projection, camera_view, tablero_translate, tablero_rotation, tablero_scale, tablero_color)
        tablero_pipeline = tablero.pipeline()
        tablero_gpu = tablero.gpu()
        tablero_pipeline.use()
        tablero_gpu.draw(GL.GL_TRIANGLES)

        #Dibujamos las paredes
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        paredes_translate = tr.translate(-0.14, 0, -0.08)
        paredes_rotation = tr.rotationX(np.pi/2)
        paredes_scale = tr.scale(2.1, 2.1, 2.1)
        paredes_color = [0.5, 0.5, 0.5]
        paredes.set_pipeline(projection, camera_view, paredes_translate, paredes_rotation, paredes_scale, paredes_color)
        paredes_pipeline = paredes.pipeline()
        paredes_gpu = paredes.gpu()
        paredes_pipeline.use()
        paredes_gpu.draw(GL.GL_TRIANGLES)

  
        #Dibujamos los obstaculos
        #Dibujamos el primer bumper
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        bumper_1_translate =  tr.translate(-1.5, 0, 1)
        bumper_1_rotation = tr.rotationX(np.pi/2) 
        bumper_1_scale = tr.scale(0.4,0.4,0.4)
        bumper_1_color = [1, 1, 0.5]
        bumper_1.set_pipeline(projection, camera_view, bumper_1_translate, bumper_1_rotation, bumper_1_scale, bumper_1_color)
        bumper_1_pipeline = bumper_1.pipeline()
        bumper_1_gpu =bumper_1.gpu()
        bumper_1_pipeline.use()
        bumper_1_gpu.draw(GL.GL_TRIANGLES)

        #Dibujamos el segundo bumper
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        bumper_2_translate =  tr.translate(1.5, 0, -0.5)
        bumper_2_rotation = tr.rotationX(np.pi/2) 
        bumper_2_scale = tr.scale(0.4,0.4,0.4)
        bumper_2_color = [1, 1, 0.5]
        bumper_2.set_pipeline(projection, camera_view, bumper_2_translate, bumper_2_rotation, bumper_2_scale, bumper_2_color)
        bumper_2_pipeline = bumper_2.pipeline()
        bumper_2_gpu =bumper_2.gpu()
        bumper_2_pipeline.use()
        bumper_2_gpu.draw(GL.GL_TRIANGLES)

        #Dibujamos la nave espacial 1
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        spaceship_rotation = tr.rotationX(0) 
        spaceship_translate =  tr.translate(-2.8,1,0)
        spaceship_scale = tr.scale(0.8,0.8,0.8)
        spaceship_color = [0.2,0.2,0.2]
        spaceship_1.set_pipeline(projection, camera_view, spaceship_translate, spaceship_rotation, spaceship_scale, spaceship_color)
        spaceship_1_pipeline = spaceship_1.pipeline()
        spaceship_1_gpu = spaceship_1.gpu()
        spaceship_1_pipeline.use()
        spaceship_1_gpu.draw(GL.GL_TRIANGLES)

        #Dibujamos la nave espacial 2
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        spaceship_rotation = tr.rotationX(0) 
        spaceship_translate =  tr.translate(-2.8,-1,0)
        spaceship_scale = tr.scale(0.8,0.8,0.8)
        spaceship_color = [0.2,0.2,0.2]
        spaceship_2.set_pipeline(projection, camera_view, spaceship_translate, spaceship_rotation, spaceship_scale, spaceship_color)
        spaceship_2_pipeline = spaceship_2.pipeline()
        spaceship_2_gpu =spaceship_2.gpu()
        spaceship_2_pipeline.use()
        spaceship_2_gpu.draw(GL.GL_TRIANGLES)

        #Dibujamos el primer flipper
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        flipper_1_pipeline = flipper_1.pipeline()
        flipper_1_gpu = flipper_1.gpu()
        flipper_1_pipeline.use()
        flipper_1_gpu.draw(GL.GL_TRIANGLES)
        matrix_rotation = tr.rotationX(np.pi/2) #@ tr.rotationY(-np.pi/4)
        flipper_1_pipeline['scale'] = tr.scale(0.4,0.4,0.4).reshape(16, 1, order='F')
        flipper_1_pipeline['rotation'] = matrix_rotation.reshape(16, 1, order='F')
        flipper_1_pipeline['translate'] = tr.translate(4, 0, 1).reshape(16, 1, order='F')
        flipper_1_pipeline['view'] = camera_view
        flipper_1_pipeline['projection'] = projection
        flipper_1_pipeline['color'] = [0.5, 1, 0.5]

        #Segundo flipper
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        flipper_2_pipeline = flipper_2.pipeline()
        flipper_2_gpu = flipper_2.gpu()
        flipper_2_pipeline.use()
        flipper_2_gpu.draw(GL.GL_TRIANGLES)
        matrix_rotation = tr.rotationX(np.pi/2)# @ tr.rotationY(np.pi/4)
        flipper_2_pipeline['scale'] = tr.scale(0.4,0.4,0.4).reshape(16, 1, order='F')
        flipper_2_pipeline['rotation'] = matrix_rotation.reshape(16, 1, order='F')
        flipper_2_pipeline['translate'] = tr.translate(4,0,-0.5).reshape(16, 1, order='F')
        flipper_2_pipeline['view'] = camera_view
        flipper_2_pipeline['projection'] = projection
        flipper_2_pipeline['color'] = [0.5, 1, 0.5]

        #Pelota
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        pelota_pipeline = pelota.pipeline()
        pelota_gpu = pelota.gpu()
        pelota_pipeline.use()
        pelota_gpu.draw(GL.GL_TRIANGLES)
        pelota_matrix_rotation = tr.rotationX(0)# @ tr.rotationY(np.pi/4)
        pelota_pipeline['scale'] = tr.scale(0.4,0.4,0.4).reshape(16, 1, order='F')
        pelota_pipeline['rotation'] = pelota_matrix_rotation.reshape(16, 1, order='F')
        pelota_pipeline['translate'] = tr.translate(3.2,1.9,0).reshape(16, 1, order='F')
        pelota_pipeline['view'] = camera_view
        pelota_pipeline['projection'] = projection
        pelota_pipeline['color'] = [1, 1, 1]

    # aquí comienza pyglet a ejecutar su loop.
    pyglet.app.run()