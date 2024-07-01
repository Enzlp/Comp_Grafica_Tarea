import random
import pyglet
import pyglet.gl as GL
import pymunk
from pymunk.pyglet_util import DrawOptions
from pymunk import Vec2d
from pyglet.window import key
from grafica.utils import load_pipeline
from pathlib import Path
import os

if __name__ == "__main__":
    # Initialize pyglet window
    width = 960
    height = 960
    window = pyglet.window.Window(width, height)
    #window.push_handlers(keys)

    # Physics space setup
    space = pymunk.Space()
    space.gravity = (0.0, -900.0)  # Inverted gravity direction
    #draw_options = DrawOptions()
    pipeline = load_pipeline(
        Path(os.path.dirname(__file__)) / "vertex_program.glsl",
        Path(os.path.dirname(__file__)) / "fragment_program.glsl",
    )


    # Walls setup (inverted positions)
    static_lines = [
        pymunk.Segment(space.static_body, (150, 100), (150, 550), 2.0),  # Inverted y positions
        pymunk.Segment(space.static_body, (450, 100), (450, 550), 2.0),  # Inverted y positions
        pymunk.Segment(space.static_body, (150, 550), (450, 550), 2.0),
    ]
    for line in static_lines:
        line.elasticity = 0.7
        line.group = 1
    space.add(*static_lines)

    # Flippers setup (inverted positions and adjusted spring angles)
    fp = [(20, 20), (-120, 0), (20, -20)]  # Inverted y positions
    mass = 100
    moment = pymunk.moment_for_poly(mass, fp)

    # Right flipper
    r_flipper_body = pymunk.Body(mass, moment)
    r_flipper_body.position = 450, 100  # Inverted y position
    r_flipper_shape = pymunk.Poly(r_flipper_body, fp)
    space.add(r_flipper_body, r_flipper_shape)

    r_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    r_flipper_joint_body.position = r_flipper_body.position
    j = pymunk.PinJoint(r_flipper_body, r_flipper_joint_body, (0, 0), (0, 0))
    s = pymunk.DampedRotarySpring(r_flipper_body, r_flipper_joint_body, -0.15, 20000000, 900000)  # Adjusted spring rotation direction
    space.add(j, s)

    # Left flipper
    l_flipper_body = pymunk.Body(mass, moment)
    l_flipper_body.position = 150, 100  # Inverted y position
    l_flipper_shape = pymunk.Poly(l_flipper_body, [(-x, -y) for x, y in fp])  # Inverted y positions
    space.add(l_flipper_body, l_flipper_shape)

    l_flipper_joint_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    l_flipper_joint_body.position = l_flipper_body.position
    j = pymunk.PinJoint(l_flipper_body, l_flipper_joint_body, (0, 0), (0, 0))
    s = pymunk.DampedRotarySpring(l_flipper_body, l_flipper_joint_body, 0.15, 20000000, 900000)  # Adjusted spring rotation direction
    space.add(j, s)

    r_flipper_shape.group = l_flipper_shape.group = 1
    r_flipper_shape.elasticity = l_flipper_shape.elasticity = 0.4

    # Bumpers setup (inverted positions)
    for p in [(240, 350), (360, 350)]:  # Inverted y positions
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        body.position = p
        shape = pymunk.Circle(body, 10)
        shape.elasticity = 0.2
        space.add(body, shape)

    #Pelota
    mass = 1
    radius = 25
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    x = random.randint(150, 450)
    body.position = x, 500  # Inverted y position
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.elasticity = 0.95
    space.add(body, shape)


    @window.event
    def on_draw():
        GL.glClearColor(0, 0, 0, 1.0)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        window.clear()
        #space.debug_draw(draw_options)
        pipeline.use()
        pipeline['color'] = [1,1,1]
        if body.position[0] <2:
            print("No Existe")
        else:
            print("Existe")


    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == key.D:
            r_flipper_body.apply_impulse_at_local_point(Vec2d.unit() * -40000, (100, 0))  # Inverted impulse direction
        elif symbol == key.A:
            l_flipper_body.apply_impulse_at_local_point(Vec2d.unit() * 40000, (100, 0))  # Inverted impulse direction

    def update(dt):
        space.step(dt)

    pyglet.clock.schedule_interval(update, 1 / 60.0)
    pyglet.app.run()
