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

    #Grafica
    # Tablero
    tablero_obj = tm.load(Path(os.path.dirname(__file__)) /"assets_obj/superficie_copy.obj")
    tablero_obj.apply_translation(-tablero_obj.centroid)
    tablero_obj.apply_scale(1.0 /  tablero_obj.scale)
    tablero_vertex_list = tm.rendering.mesh_to_vertexlist(tablero_obj)
    tablero_gpu = pipeline.vertex_list_indexed(
        len(tablero_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        tablero_vertex_list[3]
    )
    tablero_gpu.position[:] = tablero_vertex_list[4][1]
    # Paredes
    paredes_obj = tm.load(Path(os.path.dirname(__file__))/"assets_obj/paredes_2.obj")
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
    bumper3_vertex_list = tm.rendering.mesh_to_vertexlist(bumper_obj)
    bumper3_gpu = pipeline.vertex_list_indexed(
        len(bumper3_vertex_list[4][1]) // 3,
        GL.GL_TRIANGLES,
        bumper3_vertex_list[3]
    )
    bumper3_gpu.position[:] = bumper3_vertex_list[4][1]
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
    flipper_obj.apply_scale(2.0/  flipper_obj.scale)
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

    #Fisica
    import pymunk

    space = pymunk.Space()
    space.gravity = (20.0, 0.0)  # Gravity Direction

    #Paredes
    static_lines = [
        pymunk.Segment(space.static_body, (-10, 3.5), (10, 3.5), 1.0),  # Inverted y positions
        pymunk.Segment(space.static_body, (-10, -3.5), (10, -3.5), 1.0),  # Inverted y positions
        pymunk.Segment(space.static_body, (-6, -10), (-6,10), 1.0),
    ]
    for line in static_lines:
        line.elasticity = 0.7
        line.group = 1
    space.add(*static_lines)
    
    #Pelota
    balls = []
    
    @window.event
    def on_key_press(symbol, modifier):
        # print(symbol)
        if(key.C == symbol):
            controller.change_view()
        elif(key.A == symbol):
            controller.start_left_flipper()
        elif(key.D == symbol):
            controller.start_right_flipper()
        elif(key.SPACE == symbol):
            mass = 1
            radius = 0.5
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            body.position = 0,0  # Inverted y position
            shape = pymunk.Circle(body, radius, (0, 0))
            shape.elasticity = 0.95
            space.add(body, shape)
            balls.append(shape)
            
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

        #Al hacer transformaciones es de la ultima matriz a la primera
        #Dibujamos el tablero
        trans_tablero = [tr.translate(0, 0, 0),tr.uniformScale(4)]
        pipeline['transform'] = tr.matmul(trans_tablero).reshape(16, 1, order='F')
        pipeline['view'] = camera_view
        pipeline['projection'] = projection
        pipeline['color'] = [0.5, 0.5, 1]
        tablero_gpu.draw(GL.GL_TRIANGLES)

        #Dibujamos las paredes
        tr_paredes = [tr.translate(-0.55,0,0), tr.scale(2.1, 2.1, 2.1), tr.rotationX(np.pi/2)]
        pipeline['transform'] = tr.matmul(tr_paredes).reshape(16, 1, order='F')
        pipeline['color'] = [0.2,0.2,0.2]
        paredes_gpu.draw(GL.GL_TRIANGLES)

        #Dibujamos los bumpers
        tr_bumper1 = [tr.scale(0.4,0.4,0.4),tr.translate(0,0,0), tr.rotationX(np.pi/2)]
        pipeline['transform'] = tr.matmul(tr_bumper1).reshape(16, 1, order='F')
        pipeline['color'] = [1, 1, 0.5]
        bumper_gpu.draw(GL.GL_TRIANGLES)
        tr_bumper2 = [tr.scale(0.4,0.4,0.4),tr.translate(-1.5,1,0), tr.rotationX(np.pi/2)]
        pipeline['transform'] = tr.matmul(tr_bumper2).reshape(16, 1, order='F')
        bumper2_gpu.draw(GL.GL_TRIANGLES)
        tr_bumper3 = [tr.scale(0.4,0.4,0.4),tr.translate(-1.5,-1,0), tr.rotationX(np.pi/2)]
        pipeline['transform'] = tr.matmul(tr_bumper3).reshape(16, 1, order='F')
        bumper3_gpu.draw(GL.GL_TRIANGLES)

        #Dibujamos las piezas moviles
        #Pelota
        for ball in balls:    
            dx,dy = 0,0
            dx,dy = ball.body.position
            if(dx<-6):
                pyglet.app.exit()
            tr_pelota = [tr.scale(0.4,0.4,0.4),tr.translate(dx,dy,0)]
            pipeline['transform'] = tr.matmul(tr_pelota).reshape(16, 1, order='F')
            pipeline['color'] = [0.5,0.5,0.5]
            pelota_gpu.draw(GL.GL_TRIANGLES)

        #Movimiento paletas
        if(controller.right_flipper_rotating):
            if(controller.alpha_1>-np.pi/2):
                controller.alpha_1 -= 0.3
        else:
            if controller.alpha_1<0:
                controller.alpha_1 += 0.3

        if(controller.left_flipper_rotating):
            if(controller.alpha_2<np.pi/2):
                controller.alpha_2 += 0.3
        else:
            if controller.alpha_2>0:
                controller.alpha_2 -= 0.3
                
        #Flipper
        tr_flipper_1 = [tr.translate(1.6, 0.8,0),tr.rotationZ(-np.pi/2+controller.alpha_1),tr.rotationX(np.pi/2),tr.uniformScale(0.4)]
        pipeline['transform'] = tr.matmul(tr_flipper_1).reshape(16, 1, order='F')
        pipeline['color'] = [0.5, 1, 0.5]
        flipper_gpu.draw(GL.GL_TRIANGLES)
        tr_flipper_2 = [tr.translate(1.6, -0.8,0),tr.rotationZ(np.pi/2+controller.alpha_2),tr.rotationX(np.pi/2),tr.uniformScale(0.4)]
        pipeline['transform'] = tr.matmul(tr_flipper_2).reshape(16, 1, order='F')
        flipper2_gpu.draw(GL.GL_TRIANGLES)
        
    # aquí comienza pyglet a ejecutar su loop.
    def update(dt):
        space.step(dt)
    pyglet.clock.schedule_interval(update, 1 / 360.0)
    pyglet.app.run()
