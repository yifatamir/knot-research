from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
import transform
import numpy as np
import nona_5_7_ring as nona
import costfunction as c
import time

eye = np.array([0.0,-13.0,1.5])
up = np.array([0.0,0.0,1.0])
prevX = 0
prevY = 0
r = 0

num_modules = 7
hd = 1.2
hc = 0.6
fx = 2.0
tz = 1.0
tr = 1.0
x_trans = (0.5*math.sin(math.radians(90-((360/num_modules)/2.0))))/math.sin(math.radians(((360/num_modules)/2.0)))
y_trans = 0
z_trans = 0

hd_step = 0.1
hc_step = 0.1
fx_step = 0.1
tz_step = 0.1
tr_step = 0.1

global_step = 0.01
global_step_threshold = 0.000001
delay = 0.002

alpha = 1
beta = 1
gamma = 1

non_one = nona.Nonahedron_reparam_ring(num_modules, hd, hc, fx, tz, tr, x_trans, y_trans, z_trans, 0, 0, 0)
non_two = nona.Nonahedron_reparam_ring(num_modules, hd, hc, fx, tz, tr, x_trans, y_trans, z_trans, 0, 0, 360.0/num_modules)
non_three = nona.Nonahedron_reparam_ring(num_modules, hd, hc, fx, tz, tr, x_trans, y_trans, z_trans, 0, 0, 2*360.0/num_modules)
non_four = nona.Nonahedron_reparam_ring(num_modules, hd, hc, fx, tz, tr, x_trans, y_trans, z_trans, 0, 0, 3*360.0/num_modules)
non_five = nona.Nonahedron_reparam_ring(num_modules, hd, hc, fx, tz, tr, x_trans, y_trans, z_trans, 0, 0, 4*360.0/num_modules)
non_six = nona.Nonahedron_reparam_ring(num_modules, hd, hc, fx, tz, tr, x_trans, y_trans, z_trans, 0, 0, 5*360.0/num_modules)
non_seven = nona.Nonahedron_reparam_ring(num_modules, hd, hc, fx, tz, tr, x_trans, y_trans, z_trans, 0, 0, 6*360.0/num_modules)
nons = [non_one, non_two, non_three, non_four, non_five, non_six, non_seven]

cost, eld, pad, fnp = c.cost_function(non_one, alpha, beta, gamma)
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
	global nons, non_one, cost, global_step, global_step_threshold, lowest_cost
	# if (global_step < global_step_threshold):
	# 	return
	base_cost = cost
	non = non_one
	non.fx += global_step
	non.rebuild()
	cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
	delta_fx = cost - base_cost
	non.fx -= global_step
	non.hc += global_step
	non.rebuild()
	cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
	delta_hc = cost - base_cost
	non.hc -= global_step
	non.hd += global_step
	non.rebuild()
	cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
	delta_hd = cost - base_cost
	non.hd -= global_step
	non.tz += global_step
	non.rebuild()
	cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
	delta_tz = cost - base_cost
	non.tz -= global_step
	non.tr += global_step
	non.rebuild()
	cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
	delta_tr = cost - base_cost
	non.tr -= global_step
	highest_sensitivity = max([abs(x) for x in [delta_fx, delta_hc, delta_hd, delta_tz, delta_tr]])
	if highest_sensitivity == abs(delta_fx):
		if (delta_fx < 0):
			for nona in nons:
				nona.fx += global_step
		else:
			for nona in nons:
				nona.fx -= global_step
	elif highest_sensitivity == abs(delta_hc):
		if (delta_hc < 0):
			for nona in nons:
				nona.hc += global_step
		else:
			for nona in nons:
				nona.hc -= global_step
	elif highest_sensitivity == abs(delta_hd):
		if (delta_hd < 0):
			for nona in nons:
				nona.hd += global_step
		else:
			for nona in nons:
				nona.hd -= global_step
	elif highest_sensitivity == abs(delta_tz):
		if (delta_tz < 0):
			for nona in nons:
				nona.tz += global_step
		else:
			for nona in nons:
				nona.tz -= global_step
	else:
		if (delta_tr < 0):
			for nona in nons:
				nona.tr += global_step
		else:
			for nona in nons:
				nona.tr += global_step
	for nona in nons:
				nona.rebuild()
	cost, eld, pad, fnp = c.cost_function(non, alpha, beta, gamma)
	if (abs(cost - base_cost) < 0.0001):
		if (cost - lowest_cost > 0):
			global_step = float(global_step) / 2.0
		else:
			global_step = global_step * 2.0
	if (abs(cost - base_cost) > 0.1):
		global_step = float(global_step) / 2.0
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
	global nons, non_one, cost, past_cost, lowest_cost, colors, eld, pad, fnp
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

	cost, eld, pad, fnp = c.cost_function(non_one, alpha, beta, gamma)
	if (cost != past_cost):
		print("eld: " +  str(eld) + "     pad: " + str(pad) + "     fnp: " + str(fnp))
		print(cost - lowest_cost)
		lowest_cost = min(lowest_cost, cost)
		past_cost = cost

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
	global nons, hd_step, hc_step, tz_step, tr_step, fx_step, global_step, global_step_threshold, delay
	if key == 27:
		exit(0)
	elif key == "d":
		for non in nons:
			non.hd += hd_step
	elif key == "e":
		for non in nons:
			non.hd -= hd_step
	elif key == "c":
		for non in nons:
			non.hc += hc_step
	elif key == "f":
		for non in nons:
			non.hc -= hc_step
	elif key == "z":
		for non in nons:
			non.tz += tz_step
	elif key == "a":
		for non in nons:
			non.tz -= tz_step
	elif key == "x":
		for non in nons:
			non.fx += fx_step
	elif key == "s":
		for non in nons:
			non.fx -= fx_step
	elif key == "r":
		for non in nons:
			non.tr += tr_step
	elif key == "4":
		for non in nons:
			non.tr -= tr_step
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
	global hd, hc, fx, tz, tr, cost, lowest_cost, global_step
	print("hd = " + str(hd))
	print("hc = " + str(hc))
	print("fx = " + str(fx))
	print("tz = " + str(tz))
	print("tr = " + str(tr))
	print("hd_step = " + str(hd_step))
	print("hc_step = " + str(hc_step))
	print("fx_step = " + str(fx_step))
	print("tz_step = " + str(tz_step))
	print("tr_step = " + str(tr_step))
	print("cost = " + str(cost))
	print("lowest_cost = " + str(lowest_cost))
	print("global_step = " + str(global_step))

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
	glutCreateWindow("Odd-ring Nonahedron Toroid")
	glutDisplayFunc(mainDisplay)
	glutReshapeFunc(mainReshape)
	glutMotionFunc(drag)
	glutMouseFunc(mouse)
	glutKeyboardFunc(keyboard)
	init()
	glutMainLoop()
	return

if __name__ == '__main__': main()
