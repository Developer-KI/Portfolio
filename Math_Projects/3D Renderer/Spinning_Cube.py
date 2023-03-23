import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

filename_file = open(f'./shapes/filenames.ttx', "r", encoding="utf8")
shape = filename_file.readline()[:-1]

if shape == "Sphere":
    sphere = gluNewQuadric()
else:
    read = filename_file.readline()[:-1]
    vertex_file = open(f'./shapes/{shape}/{read}.ttx', "r", encoding="utf8")
    edge_file = open(f'./shapes/{shape}/{filename_file.readline()[:-1]}.ttx', "r", encoding="utf8")
    verticies = []
    temp_v = []
    for token in vertex_file.readline().split(", "):
        num = int(token.replace("(", "").replace(")", ""))
        temp_v.append(num)
        if ")" in token:
            verticies.append(tuple(temp_v))
            temp_v = []

    edges = []
    temp_e = []
    for token in edge_file.readline().split(", "):
        num = int(token.replace("(", "").replace(")", ""))
        temp_e.append(num)
        if ")" in token:
            edges.append(tuple(temp_e))
            temp_e = []

    vertex_file.close()
    edge_file.close()


def Shape():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Stereometry Tool (by Kiril Ivanov)")

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0,0, -5)

    #glRotatef(25, 2, 1, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-1,0,0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(1,0,0)

                if event.key == pygame.K_UP:
                    glTranslatef(0,1,0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0,-1,0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0,0,0.5)

                if event.button == 5:
                    glTranslatef(0,0,-0.5)

        glRotatef(1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        if shape == "Sphere":
            gluSphere(sphere, 1.0, 32, 16)
        else:
            Shape()
        pygame.display.flip()
        pygame.time.wait(90)


main()

filename_file.close()
