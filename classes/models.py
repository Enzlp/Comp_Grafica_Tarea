import trimesh as tm
from pathlib import Path
import os
import pyglet
import pyglet.gl as GL
import aux_functions.transformations as tr
import numpy as np


with open(Path(os.path.dirname(__file__)).parent.absolute() /"vertex_program.glsl") as f:
    vertex_source_code = f.read()

with open(Path(os.path.dirname(__file__)).parent.absolute() / "fragment_program.glsl") as f:
    fragment_source_code = f.read()

vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")


#Clase Object_Static
# obj: tipo de objeto a graficar
# init_scale: escala inicial a la que sera renderizado
class Object_Static:
    def __init__(self, obj, init_scale):
        self._obj = tm.load(Path(os.path.dirname(__file__)).parent.absolute() /"assets_obj"/obj)
        self._obj.apply_translation(-self._obj.centroid)
        self._obj.apply_scale(init_scale /  self._obj.scale)
        self._pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)
        self._vertex_list = tm.rendering.mesh_to_vertexlist(self._obj)
        self._gpu = self._pipeline.vertex_list_indexed(
            len(self._vertex_list[4][1]) // 3,
            GL.GL_TRIANGLES,
            self._vertex_list[3]
        )
        self._gpu.position[:] = self._vertex_list[4][1]

    def pipeline(self):
        return self._pipeline
    def gpu(self):
        return self._gpu
    
    def set_pipeline(self, projection, camera_view, translate, rotation, scale, color):
        self._pipeline['translate'] = translate.reshape(16, 1, order='F')
        self._pipeline['rotation'] = rotation.reshape(16, 1, order='F')
        self._pipeline['scale'] = scale.reshape(16, 1, order='F')
        self._pipeline['view'] = camera_view
        self._pipeline['projection'] = projection
        self._pipeline['color'] = color

    

class Flipper:
    def __init__(self):
        #Cargar Modelo
        self._obj = tm.load(Path(os.path.dirname(__file__)).parent.absolute() /"assets_obj/flipper.obj")
        self._obj.apply_translation(-self._obj.centroid)
        self._obj.apply_scale(1.0/  self._obj.scale)
        self._pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)
        self._vertex_list = tm.rendering.mesh_to_vertexlist(self._obj)
        self._gpu = self._pipeline.vertex_list_indexed(
            len(self._vertex_list[4][1]) // 3,
            GL.GL_TRIANGLES,
            self._vertex_list[3]
        )
        self._gpu.position[:] = self._vertex_list[4][1]
        #Atributos 
        self.x = 0
        self.z = 0
        self.y = 0
        self.t = 0

    def pipeline(self):
        return self._pipeline
    def gpu(self):
        return self._gpu
    def activate(self):
        pass