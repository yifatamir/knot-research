from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
import transform
import numpy as np
import polyline as poly
import cost_function_polyline as c
import time

eye = np.array([0.0,-13.0,1.5])
up = np.array([0.0,0.0,1.0])
prevX = 0
prevY = 0
r = 0

points = [(2.0, -0.40, 0.80), (-1.3464, 1.532, -0.80), (-1.3464, -1.532, 0.80), (2.0, 0.40, -0.80), (-0.6536,  1.932, 0.80), (-0.6536,  -1.932, -0.80)]

global_step = 0.01
global_step_threshold = 0.00001
delay = 0.1

alpha = 1
beta = 1
gamma = 1

pol = poly.Polyline(points)
cost = c.cost_function(pol, alpha, beta, gamma)
lowest_cost = cost
past_cost = 0

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

# def gradient_descent():
# 	# look at nearmissjohnson.py for algorithm

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
	global pol, cost, past_cost, lowest_cost, colors
	pol.rebuild()
	cost = c.cost_function(pol, alpha, beta, gamma)
	if (cost != past_cost):
		print(cost - lowest_cost)
		lowest_cost = min(lowest_cost, cost)
		past_cost = cost

	glBegin(GL_LINES)
	glColor3f(1, 1, 1)
	for edge in pol.edges:
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
	global prevX, prevY, eye, up
	diffX = x - prevX
	diffY = -y + prevY
	eye = transform.left(diffX,eye,up)
	eye, up = transform.up(diffY,eye,up)

	prevX = x
	prevY = y
	glutPostRedisplay()

def keyboard(key,x,y):
	global pol, global_step, global_step_threshold, delay
	if key == 27:
		exit(0)
	elif key == "p":
		printValues()
	elif key == " ":
		gradient_descent()
	elif key == "1":
		global_step = float(global_step) / 2
	elif key == "2":
		global_step = global_step * 2
	elif key == "g":
		print("~~performing gradient descent~~")
		print("initial values: ")
		printValues()
		while (global_step > global_step_threshold):
			gradient_descent()
			glutPostRedisplay()
			time.sleep(delay)
		print("final values: ")
		printValues()

	glutPostRedisplay()

def printValues():
	global pol, cost, lowest_cost
	print("global_step = " + str(global_step))
	print("lowest cost = " + str(lowest_cost))
	print("current cost = " + str(cost))

def mouse(button,state,x,y):
	global prevX, prevY
	if state == 1:
		prevX = 0
		prevY = 0

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE)
	glutInitWindowSize(640, 480)
	glutInitWindowPosition(0, 0)
	glutCreateWindow("Trefoil")
	glutDisplayFunc(mainDisplay)
	glutReshapeFunc(mainReshape)
	glutMotionFunc(drag)
	glutMouseFunc(mouse)
	glutKeyboardFunc(keyboard)
	init()
	glutMainLoop()
	return

if __name__ == '__main__': main()
