import pyglet
import pyglet.gl as GL
from pyglet.window import key
from pathlib import Path
import os

ORTOGRAPHIC_PROYECTION = 1
PERSPECTIVE_PROYECTION = 0

#Import classes propias
from classes.controller import *
from aux_functions.transformations import *



if __name__ == "__main__":
    #Ventana
    window = pyglet.window.Window(960, 960)
    controller = Controller()

    #Cargamos el vertex program y el fragment program
    with open(Path(os.path.dirname(__file__)) / "vertex_program.glsl") as f:
        vertex_source_code = f.read()
    with open(Path(os.path.dirname(__file__)) / "fragment_program.glsl") as f:
        fragment_source_code = f.read()

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    pinball_pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)


    #Acciones al presionar teclas
    @window.event
    def on_key_press(symbol, modifier):
        if(key.C == symbol):
            controller.change_view()

    @window.event
    def on_draw():
        #Configuracion de la ventana
        GL.glClearColor(0.1, 0.1, 0.1, 1.0)
        
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glLineWidth(1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        #Limpiamos la ventana de objetos
        window.clear()
        #Activamos el pipeline para el pinball
        pinball_pipeline.use()
        #Definimos la vista en la que se encuentra el pipeline
        if(controller.view == ORTOGRAPHIC_PROYECTION):
            #fovy, aspect, near, far
            matrix_projection = ortho(0, 100, 0, 100, 0, 100)
        else:
            matrix_projection = perspective(45, window.width/window.height, 0.001, 100)

        #Definimos el pipeline
        pinball_pipeline['translate'] = translate(controller.x, controller.y, controller.z).reshape(16, 1, order='F')
        pinball_pipeline['projection'] = matrix_projection.reshape(16, 1, order='F')
        pinball_pipeline['view'] = lookAt(
                np.array([3, 3, 3]),
                np.array([0, 0, 0]), 
                np.array([0, 0, 1])
            ).reshape(16, 1, order='F')

    pyglet.app.run()