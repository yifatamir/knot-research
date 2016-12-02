from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
import transform
import numpy as np
import nonahedron as nona
import costfunction as c
import time

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

global_step = 0.01
global_step_threshold = 0.000001

alpha = 1
beta = 1
gamma = 100000

non = nona.Nonahedron(x_edge, radius_corner, height_corner, top_z)
cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
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

def gradient_descent():
	global non, cost, global_step, end, global_step_threshold, lowest_cost
	# if (global_step < global_step_threshold):
	# 	return
	base_cost = cost
	non.ex += global_step
	non.rebuild()
	cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
	delta_x = cost - base_cost
	non.ex -= global_step
	non.rc += global_step
	non.rebuild()
	cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
	delta_r = cost - base_cost
	non.rc -= global_step
	non.hc += global_step
	non.rebuild()
	cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
	delta_h = cost - base_cost
	non.hc -= global_step
	non.tz += global_step
	non.rebuild()
	cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
	delta_t = cost - base_cost
	non.tz -= global_step
	highest_sensitivity = max([abs(x) for x in [delta_t, delta_h, delta_r, delta_x]])
	if highest_sensitivity == abs(delta_x):
		if (delta_x < 0):
			non.ex += global_step
		else:
			non.ex -= global_step
	elif highest_sensitivity == abs(delta_r):
		if (delta_r < 0):
			non.rc += global_step
		else:
			non.rc -= global_step
	elif highest_sensitivity == abs(delta_h):
		if (delta_h < 0):
			non.hc += global_step
		else:
			non.hc -= global_step
	else:
		if (delta_t < 0):
			non.tz += global_step
		else:
			non.tz -= global_step
	non.rebuild()
	cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
	if (abs(cost - base_cost) < 0.0001):
		if (cost - lowest_cost > 0):
			global_step = float(global_step) / 2
		else:
			global_step = global_step * 2
	if (abs(cost - base_cost) > 0.1):
		global_step = float(global_step) / 2
	lowest_cost = min(lowest_cost, cost)

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
	global non, cost, past_cost, lowest_cost, colors, eld, pad, fnp
	non.rebuild()
	cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
	if (cost != past_cost):
		print("eld: " +  str(eld) + "     pad: " + str(pad) + "     fnp: " + str(fnp))
		print(cost - lowest_cost)
		lowest_cost = min(lowest_cost, cost)
		past_cost = cost

	# surfaces = non.topPentas + non.bottomPentas + non.quads
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
	global non, x_step, z_step, radius_step, height_step, global_step, global_step_threshold, delay
	if key == 27:
		exit(0)
	elif key == "x":
		non.ex += x_step
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
	global non, x_step, z_step, radius_step, height_step, cost, lowest_cost
	print("x = " + str(non.ex))
	print("z = " + str(non.tz))
	print("r = " + str(non.rc))
	print("h = " + str(non.hc))
	print("x_step " + str(x_step))
	print("z_step = " + str(z_step))
	print("r_step = " + str(radius_step))
	print("h_step = " + str(height_step))
	print("global_step = " + str(global_step))
	print("lowest cost = " + str(lowest_cost))
	print("current cost = " + str(cost))

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
