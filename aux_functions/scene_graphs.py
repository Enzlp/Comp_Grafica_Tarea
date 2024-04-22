import networkx as nx
import aux_functions.transformations as tr
import numpy as np
import pyglet.gl as GL


def create_pinball_graph(mesh, mesh_pipeline, axis, axis_pipeline):
    graph = nx.DiGraph(root="tablero")

    graph.add_node("tablero", transform = tr.identity())
    graph.add_node(
        "tablero_geometry",
        mesh = mesh,
        pipeline = mesh_pipeline,
        transform = tr.uniformScale(1),
        coor = np.array((1.0, 1.0, 1.0)),
    )
    
    return 




def create_solar_system(mesh, mesh_pipeline, axis, axis_pipeline):
    graph = nx.DiGraph(root="sun")

    graph.add_node("sun", transform=tr.identity())
    graph.add_node(
        "sun_geometry",
        mesh=mesh,
        pipeline=mesh_pipeline,
        transform=tr.uniformScale(0.8),
        color=np.array((1.0, 0.73, 0.03)),
    )
    graph.add_node(
        "sun_axis",
        mesh=axis,
        pipeline=axis_pipeline,
        transform=tr.uniformScale(1.25),
        mode=GL.GL_LINES,
    )
    graph.add_edge("sun", "sun_geometry")
    graph.add_edge("sun", "sun_axis")

    graph.add_node("earth", transform=tr.translate(2.5, 0.0, 0.0))
    graph.add_node(
        "earth_geometry",
        transform=tr.uniformScale(0.3),
        mesh=mesh,
        pipeline=mesh_pipeline,
        color=np.array((0.0, 0.59, 0.78)),
    )
    graph.add_node(
        "earth_axis",
        mesh=axis,
        pipeline=axis_pipeline,
        transform=tr.uniformScale(0.25),
        mode=GL.GL_LINES,
    )
    graph.add_edge("sun", "earth")
    graph.add_edge("earth", "earth_geometry")
    graph.add_edge("earth", "earth_axis")

    graph.add_node("moon", transform=tr.translate(0.5, 0.0, 0.0))
    graph.add_node(
        "moon_geometry",
        transform=tr.uniformScale(0.1),
        mesh=mesh,
        pipeline=mesh_pipeline,
        color=np.array((0.3, 0.3, 0.3)),
    )
    graph.add_node(
        "moon_axis",
        mesh=axis,
        pipeline=axis_pipeline,
        transform=tr.uniformScale(0.25),
        mode=GL.GL_LINES,
    )
    graph.add_edge("earth", "moon")
    graph.add_edge("moon", "moon_geometry")
    graph.add_edge("moon", "moon_axis")

    return graph