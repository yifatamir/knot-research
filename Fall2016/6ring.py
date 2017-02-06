from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
import transform
import numpy as np
import nona_6_8_ring as nona

eye = np.array([0.0,-13.0,1.5])
up = np.array([0.0,0.0,1.0])
prevX = 0
prevY = 0
r = 0

x_edge = 1.105
height_corner = 0.707
top_z = 0.877
x_translation = -0.86602540378 - x_edge

x_step = 0.01
height_step = 0.01
z_step = 0.01

alpha = 1
beta = 1
gamma = 1

non_one = nona.Nonahedron_ring(x_edge, height_corner, top_z, x_translation, 0)
non_two = nona.Nonahedron_ring(x_edge, height_corner, top_z, x_translation, 60)
non_three = nona.Nonahedron_ring(x_edge, height_corner, top_z, x_translation, 120)
non_four = nona.Nonahedron_ring(x_edge, height_corner, top_z, x_translation, 180)
non_five = nona.Nonahedron_ring(x_edge, height_corner, top_z, x_translation, 240)
non_six = nona.Nonahedron_ring(x_edge, height_corner, top_z, x_translation, 300)
nons = [non_one, non_two, non_three, non_four, non_five, non_six]

colors = (
	(0,0,1),
	(0,1,0),
	(1,0,0),
	(1,1,0),
	(1,0,1),
	(0,1,1),
	(0,0,0),
	(1,1,1),
	)

def init():
	glClearColor(0.0, 0.0, 0.0, 1.0) # Set background color to black and opaque
	glClearDepth(1.0)                   # Set background depth to farthest
	glEnable(GL_DEPTH_TEST)   # Enable depth testing for z-culling
	glDepthFunc(GL_LEQUAL)    # Set the type of depth-test
	glShadeModel(GL_SMOOTH)   # Enable smooth shading
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def mainDisplay():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	gluLookAt(eye[0],eye[1],eye[2],  0,0,0,  up[0],up[1],up[2])
	glBegin(GL_LINES)
	# x axis
	glColor3f(1.0, 0.0, 0.0) 
	glVertex3f(0.0,0.0,0.0)
	glVertex3f(10.0,0.0,0.0)
	# y axis
	glColor3f(0.0,1.0,0.0)
	glVertex3f(0.0,0.0,0.0)
	glVertex3f(0.0,10.0,0.0)
	# z axis
	glColor3f(0.0,0.0,1.0)
	glVertex3f(0.0,0.0,0.0)
	glVertex3f(0.0,0.0,10.0)

	glEnd()

	#Draw Geometry
	global nons, colors, eld, pad, fnp
	for non in nons:
		non.rebuild()
		surfaces = non.quads
		x = 0
		a = 0
		for surface in surfaces:
			if a == 3:
				a = 0
				x = (x + 1) % 8
			glBegin(GL_POLYGON)
			for vertex in surface:
				glColor3fv(colors[x])
				glVertex3fv(vertex)
			glEnd()
			a += 1

		glBegin(GL_LINES)
		glColor3f(1, 1, 1)
		for edge in non.edges:
			for v in edge:
				glVertex3fv(v)
		glEnd()

	glutSwapBuffers()

def mainReshape(w,h):
	if h == 0:
		h = 1
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity() 
	gluPerspective(45, float(w) / h, 0.1, 100)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

def idle():
	glutPostRedisplay()

def drag(x,y):
	global prevX
	global prevY
	global eye
	global up
	diffX = x - prevX
	diffY = -y + prevY
	eye = transform.left(diffX,eye,up)
	eye, up = transform.up(diffY,eye,up)
	prevX = x
	prevY = y
	glutPostRedisplay()

def keyboard(key,x,y):
	global nons, x_step, z_step, height_step
	if key == 27:
		exit(0)
	elif key == "x":
		for non in nons:
			non.ex += x_step
	elif key == "d":
		for non in nons:
			non.ex -= x_step
	elif key == "z":
		for non in nons:
			non.tz += z_step
	elif key == "s":
		for non in nons:
			non.tz -= z_step
	elif key == "h":
		for non in nons:
			non.hc += height_step
	elif key == "u":
		for non in nons:
			non.hc -= height_step
	elif key == "p":
		printValues()
	glutPostRedisplay()

def printValues():
	global non, x_step, z_step, height_step
	print("x = " + str(non_one.ex))
	print("z = " + str(non_one.tz))
	print("h = " + str(non_one.hc))
	print("x_step " + str(x_step))
	print("z_step = " + str(z_step))
	print("h_step = " + str(height_step))

def mouse(button,state,x,y):
	global prevX
	global prevY
	if state == 1:
		prevX = 0
		prevY = 0

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE)
	glutInitWindowSize(640, 480)
	glutInitWindowPosition(0, 0)
	glutCreateWindow("Nonahedron for 6-ring")
	glutDisplayFunc(mainDisplay)
	glutReshapeFunc(mainReshape)
	glutMotionFunc(drag)
	glutMouseFunc(mouse)
	glutKeyboardFunc(keyboard)
	init()
	glutMainLoop()
	return

if __name__ == '__main__': main()
