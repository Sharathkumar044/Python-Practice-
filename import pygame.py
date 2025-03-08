import numpy as np
import pygame
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Initialize pygame
pygame.init()

# Set up display with OpenGL
WIDTH, HEIGHT = 800, 600
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Flying Bird Simulation")

# Set up the OpenGL environment
glViewport(0, 0, WIDTH, HEIGHT)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
glEnable(GL_DEPTH_TEST)


class Bird3D:
    def __init__(self):
        # Bird's position and movement
        self.position = [-5, 0, -15]  # x, y, z
        self.speed = 0.03
        self.wing_angle = 0
        self.wing_direction = 1
        self.wing_speed = 2
        self.oscillation = 0
        self.oscillation_speed = 0.02
        self.rotation = 0
        
        # Bird body color
        self.body_color = (0.6, 0.3, 0.1)  # Brown
        self.wing_color = (0.5, 0.2, 0.0)  # Darker brown
        self.beak_color = (1.0, 0.6, 0.0)  # Orange
        
    def update(self):
        # Move bird forward
        self.position[0] += self.speed
        if self.position[0] > 10:
            self.position[0] = -10
            
        # Create a gentle up and down motion
        self.oscillation += self.oscillation_speed
        self.position[1] = math.sin(self.oscillation) * 0.5
        
        # Flap wings
        self.wing_angle += self.wing_speed * self.wing_direction
        if self.wing_angle > 30 or self.wing_angle < -10:
            self.wing_direction *= -1
            
        # Slight rotation for more natural flight
        self.rotation = math.sin(self.oscillation * 2) * 5
    
    def draw_body(self):
        glColor3f(*self.body_color)
        
        # Draw bird body (ellipsoid)
        glPushMatrix()
        glTranslatef(0, 0, 0)
        glScalef(1.0, 0.5, 0.5)
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.5, 20, 20)
        gluDeleteQuadric(quadric)
        glPopMatrix()
        
        # Draw head (sphere)
        glPushMatrix()
        glTranslatef(0.5, 0.1, 0)
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.3, 20, 20)
        gluDeleteQuadric(quadric)
        glPopMatrix()
        
        # Draw eyes
        glColor3f(0, 0, 0)  # Black
        glPushMatrix()
        glTranslatef(0.65, 0.2, 0.15)
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.05, 10, 10)
        gluDeleteQuadric(quadric)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0.65, 0.2, -0.15)
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.05, 10, 10)
        gluDeleteQuadric(quadric)
        glPopMatrix()
        
        # Draw beak
        glColor3f(*self.beak_color)
        glPushMatrix()
        glTranslatef(0.8, 0.0, 0)
        glRotatef(90, 0, 1, 0)
        quadric = gluNewQuadric()
        gluCylinder(quadric, 0.05, 0, 0.3, 20, 5)
        gluDeleteQuadric(quadric)
        glPopMatrix()
    
    def draw_wings(self):
        glColor3f(*self.wing_color)
        
        # Right wing
        glPushMatrix()
        glTranslatef(0, 0, 0.25)
        glRotatef(self.wing_angle, 1, 0, 0)
        
        glBegin(GL_TRIANGLES)
        glVertex3f(-0.3, 0, 0)
        glVertex3f(0.3, 0, 0)
        glVertex3f(0, 0, 0.8)
        glEnd()
        glPopMatrix()
        
        # Left wing
        glPushMatrix()
        glTranslatef(0, 0, -0.25)
        glRotatef(-self.wing_angle, 1, 0, 0)
        
        glBegin(GL_TRIANGLES)
        glVertex3f(-0.3, 0, 0)
        glVertex3f(0.3, 0, 0)
        glVertex3f(0, 0, -0.8)
        glEnd()
        glPopMatrix()
        
        # Tail
        glPushMatrix()
        glTranslatef(-0.5, 0, 0)
        glRotatef(15, 1, 0, 0)
        
        glBegin(GL_TRIANGLES)
        glVertex3f(0, 0, 0.2)
        glVertex3f(0, 0, -0.2)
        glVertex3f(-0.5, 0, 0)
        glEnd()
        glPopMatrix()
    
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation, 0, 0, 1)
        
        self.draw_body()
        self.draw_wings()
        
        glPopMatrix()


def draw_sky():
    # Set sky blue background
    glClearColor(0.53, 0.81, 0.92, 1.0)
    
    # Draw some clouds (spheres)
    glColor4f(1.0, 1.0, 1.0, 0.7)  # White with some transparency
    
    cloud_positions = [
        [-3, 3, -20],
        [2, 4, -18],
        [5, 2, -15],
        [-4, 1, -12],
        [0, 5, -25]
    ]
    
    for pos in cloud_positions:
        glPushMatrix()
        glTranslatef(*pos)
        for i in range(3):
            offset_x = np.random.uniform(-0.7, 0.7)
            offset_y = np.random.uniform(-0.4, 0.4)
            offset_z = np.random.uniform(-0.4, 0.4)
            size = np.random.uniform(0.6, 1.2)
            
            glPushMatrix()
            glTranslatef(offset_x, offset_y, offset_z)
            quadric = gluNewQuadric()
            gluSphere(quadric, size, 15, 15)
            gluDeleteQuadric(quadric)
            glPopMatrix()
        glPopMatrix()


# Create bird
bird = Bird3D()

# Set the camera
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)
glTranslatef(0, 0, 5)

# Enable transparency for clouds
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Lighting setup
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

light_position = [5.0, 10.0, 5.0, 1.0]
light_ambient = [0.2, 0.2, 0.2, 1.0]
light_diffuse = [1.0, 1.0, 1.0, 1.0]
light_specular = [0.5, 0.5, 0.5, 1.0]

glLightfv(GL_LIGHT0, GL_POSITION, light_position)
glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Clear the screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Draw sky with clouds
    draw_sky()
    
    # Update and draw bird
    bird.update()
    bird.draw()
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)