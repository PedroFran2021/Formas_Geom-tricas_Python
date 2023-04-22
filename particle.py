import glfw
from OpenGL.GL import *
import numpy as np
import random
import OpenGL.GL as gl
from OpenGL.GL import shaders
import pyrr
from pyrr import matrix44
from pyrr import Vector3

vertex_shader_source = """
#version 330 core

layout (location = 0) in vec2 position;
layout (location = 1) in vec4 color;
layout (location = 2) in float size;
out vec4 v_color;

uniform mat4 projection;
uniform mat4 view;

void main()
{
    gl_Position = projection * view * vec4(position, 0.0, 1.0);
    v_color = color;
    gl_PointSize = size * 4;
}
"""

fragment_shader_source = """
#version 330 core

in vec4 v_color;

out vec4 frag_color;

void main()
{
    frag_color = v_color;
}
"""

class Particle:
    def _init_(self, position, velocity, color, life, size):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.color = np.array(color)
        self.life = life
        self.size = size

class ParticleEmitter:
    def _init_(self, position, velocity, color, rate, size):
        self.position = np.array(position)
        self.velocity = np.array(velocity) + np.array([random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)])
        self.color = np.array(color)
        self.rate = rate
        self.time_since_last_emit = 0.0
        self.size = size
    def update(self, dt):
        self.time_since_last_emit += dt
        num_particles = int(self.time_since_last_emit * self.rate)
        self.time_since_last_emit -= num_particles / self.rate
        return [Particle(self.position, self.velocity + np.array([random.uniform(-0.1, 0.1),random.uniform(-0.1, 0.1)]),self.color, self.size, 5.0) for i in range(num_particles)]

class ParticleSystem:
    def _init_(self, max_particles):
        self.max_particles = max_particles 
        self.particles = []
        self.emitters = []
        particle_position = np.array([1.0, 0.0]) 
        particle_rotation = 50.0
        particle_size = 100.0
        
    def add_emitter(self, emitter):
        self.emitters.append(emitter)
        
    def update(self, dt):
        new_particles = []
        for emitter in self.emitters:
            new_particles.extend(emitter.update(dt))
        self.particles.extend(new_particles)
        self.particles = [particle for particle in self.particles if particle.life > 0.0]
        if len(self.particles) > self.max_particles:
            self.particles = self.particles [:self.max_particles]
        for particle in self.particles:
            particle.position += particle.velocity * dt
            particle.life -= dt

def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader

def create_program(vertex_shader, fragment_shader):
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(program))
    return program

def main():
    if not glfw.init():
        return
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(640,480, "Particle System", None, None)
    glfw.set_window_pos(window, 400, 200)
    
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_PROGRAM_POINT_SIZE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    vertex_shader = create_shader(GL_VERTEX_SHADER, vertex_shader_source)
    fragment_shader = create_shader(GL_FRAGMENT_SHADER, fragment_shader_source)
    program = create_program(vertex_shader, fragment_shader)
    if program is None:
        print("Program creation failed.")
        return
    glUseProgram(program)
    projection_location = glGetUniformLocation(program, "projection")
    view_location = glGetUniformLocation(program, "view")
    position_location = glGetAttribLocation(program, "position")
    color_location = glGetAttribLocation(program, "color")
    
    particles = ParticleSystem(150000)
    emitter = ParticleEmitter([0.0, 0.5], [-0.5, 1.0], [1.0, 1.0, 0.0, 1.0], 50.0 , 1500.0)
    new_emitter = ParticleEmitter([-0.5, 0.0], [-0.5, 1.0], [1.0, 0.0, 1.0, 1.0], 150.0 , 1500.0)
    particles.add_emitter(new_emitter)
    new_emitter1 = ParticleEmitter([0.0, 1.0], [-0.5, 1.0], [1.0, 0.0, 0.0, 1.0], 50.0 , 1500.0)
    particles.add_emitter(new_emitter1)
    new_emitter2 = ParticleEmitter([0.5, 0.0], [-0.5, 1.0], [0.0, 0.0, 1.0, 1.0], 50.0 , 1500.0)
    particles.add_emitter(new_emitter2)
    new_emitter3 = ParticleEmitter([0.5, 0.0], [-0.5, 1.0], [0.5, 0.0, 1.0, 0.0], 50.0 , 1500.0)
    particles.add_emitter(new_emitter3)
    new_emitter4 = ParticleEmitter([0.5, 0.0], [-0.5, 1.0], [1.0, 0.5, 1.0, 1.0], 50.0 , 1500.0)
    particles.add_emitter(new_emitter4)
    new_emitter5 = ParticleEmitter([0.5, 0.0], [-0.5, 1.0], [0.0, 1.0, 5.0, 1.0], 50.0 , 1500.0)
    particles.add_emitter(new_emitter5)
    new_emitter6 = ParticleEmitter([0.5, 0.0], [-0.5, 1.0], [1.0, 0.0, 1.0, 1.0], 50.0 , 1500.0)
    particles.add_emitter(new_emitter6)
    particles.add_emitter(emitter)
    
    time = 0.0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        width, height = glfw.get_framebuffer_size(window)
        projection = np.array([[ -7.0 / width, 0.0, 0.0, 0.0],
                               [0.0, -5.0 /height, 0.0, 0.0],
                               [0.0, 0.0, 1.0, 0.0],
                               [-1.0, -1.0, 0.5, 1.0]], dtype=np.float32)
        view = np.eye(4, dtype=np.float32)
        glUniformMatrix4fv(projection_location, 1, GL_TRUE, projection)
        glUniformMatrix4fv(view_location, 1, GL_TRUE, view)
        dt = glfw.get_time() - time
        time = glfw.get_time()
        particles.update(dt)
        position = np.array([particle.position for particle in particles.particles], dtype=np.float32)
        colors = np.array([particle.color for particle in particles.particles], dtype=np.float32)
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        vbo_position = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_position)
        glBufferData(GL_ARRAY_BUFFER, position.nbytes, position, GL_DYNAMIC_DRAW)
        glVertexAttribPointer(position_location, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray (position_location)
        sizes = np.array([particle.size for particle in particles.particles], dtype=np.float32)
        vbo_sizes = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,vbo_sizes)
        glBufferData(GL_ARRAY_BUFFER, sizes.nbytes, sizes, GL_DYNAMIC_DRAW)
        size_location = glGetAttribLocation(program, "size")
        if size_location < 0:
            print("size_location not found in shader")
        glVertexAttribPointer(size_location,1, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(size_location)
        vbo_colors = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_colors)
        glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_DYNAMIC_DRAW)
        glVertexAttribPointer(color_location,4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(color_location)
        glDrawArrays(GL_POINTS, 2,len(particles.particles))
        glDeleteVertexArrays(1,[vao])
        glfw.swap_buffers (window)
    glfw.terminate()
if __name__ == '_main_':
    main()