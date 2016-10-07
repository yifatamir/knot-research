from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
import transform
import numpy as np
import nonahedron as nona
import costfunction as c

eye = np.array([0.0,-13.0,1.5])
up = np.array([0.0,0.0,1.0])

prevX = 0
prevY = 0
r = 0

x_edge = 1.105
radius_corner = 0.985
height_corner = 0.707
top_z = 0.877

x_step = 0.01
radius_step = 0.01
height_step = 0.01
z_step = 0.01

alpha = 1000000
beta = 0.0001
gamma = 1

non = nona.Nonahedron(x_edge, radius_corner, height_corner, top_z)
cost = c.cost_function(non, alpha, beta, gamma)
past_cost = 0

def init():
	glClearColor(0.0, 0.0, 0.0, 1.0); # Set background color to black and opaque
	glClearDepth(1.0);                   # Set background depth to farthest
	glEnable(GL_DEPTH_TEST);   # Enable depth testing for z-culling
	glDepthFunc(GL_LEQUAL);    # Set the type of depth-test
	glShadeModel(GL_SMOOTH);   # Enable smooth shading
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);

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
	global non, cost, past_cost
	non.rebuild()
	cost = c.cost_function(non, alpha, beta, gamma)
	if (cost != past_cost):
		print(cost)
		past_cost = cost

	glBegin(GL_LINES)
	#color the for lines you're about to draw
	glColor3f(1.0, 0.0, 0.0);
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
	global non, x_step, z_step, radius_step, height_step
	if key == 27:
		exit(0)
	elif key == "x":
		non.ex += x_step
		print(non.ex)
	elif key == "d":
		non.ex -= x_step
	elif key == "z":
		non.tz += z_step
	elif key == "s":
		non.tz -= z_step
	elif key == "r":
		non.rc += radius_step
	elif key == "5":
		non.rc -= radius_step
	elif key == "h":
		non.hc += height_step
	elif key == "u":
		non.hc -= height_step

	glutPostRedisplay()


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
	glutCreateWindow("Nonahedron")
	glutDisplayFunc(mainDisplay)
	glutReshapeFunc(mainReshape)
	glutMotionFunc(drag)
	glutMouseFunc(mouse)
	glutKeyboardFunc(keyboard)
	init()
	glutMainLoop()
	return

if __name__ == '__main__': main()