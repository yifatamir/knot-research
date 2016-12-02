# quads planar
# degrees = 360/number modules
# no threefold symmetry
# parameters: length of diagonal of quad, height of the shoulder above the quad face, sliders of third quad in and out, tz, radial tz

import math

class Nonahedron_reparam_ring:

	def __init__(self, num_modules, hd, hc, fx, tz, tr, x_trans = 0, y_trans = 0, z_trans = 0, rot_x = 0, rot_y = 0, rot_z = 0):
		self.num_modules = num_modules
		self.hd = hd
		self.hc = hc
		self.fx = fx
		self.tz = tz
		self.tr = tr
		self.x_trans = x_trans
		self.y_trans = y_trans
		self.z_trans = z_trans
		self.rot_x = rot_x
		self.rot_y = rot_y
		self.rot_z = rot_z
		self.points = self.buildPoints()
		self.quads = self.buildQuads()
		self.topPentas = self.buildTopPentas()
		self.bottomPentas = self.buildBottomPentas()
		self.edges = self.getAllEdges()

	#returns a dictionary with 14 "name":(x, y z) entries. 
	#MODIFIED FOR 6 and 8-RING by enforcing planarity of quads (changing x & y values of k1, k3, k5, c1, c3, c5)
	def buildPoints(self):
		angle = 360.0 / self.num_modules
		angle_over_two = angle / 2.0
		theta = math.radians(angle_over_two)
		sine = math.sin(theta)
		cosine = math.cos(theta)

		e0 = (self.hd*cosine + self.x_trans, 		-0.5-(self.hd*sine) + self.y_trans, 		self.z_trans)
		e1 = (self.x_trans, 						-0.5 + self.y_trans, 						self.z_trans)
		e2 = (self.x_trans, 						0.5 + self.y_trans, 						self.z_trans)
		e3 = (self.hd*cosine + self.x_trans, 		0.5+(self.hd*sine) + self.y_trans, 			self.z_trans)
		e4 = (self.fx + self.x_trans, 				self.hd/2.0 + self.y_trans, 				self.z_trans)
		e5 = (self.fx + self.x_trans, 				-self.hd/2.0 + self.y_trans, 				self.z_trans)
		c1 = ((self.hd/2.0)*cosine + self.x_trans, 	-0.5-((self.hd/2.0)*sine) + self.y_trans, 	self.hc + self.z_trans)
		c3 = ((self.hd/2.0)*cosine + self.x_trans, 	0.5+((self.hd/2.0)*sine) + self.y_trans, 	self.hc + self.z_trans)
		c5 = (self.fx + self.x_trans, 				self.y_trans, 								self.hc + self.z_trans)
		k1 = ((self.hd/2.0)*cosine + self.x_trans, 	-0.5-((self.hd/2.0)*sine) + self.y_trans, 	-self.hc + self.z_trans)
		k3 = ((self.hd/2.0)*cosine + self.x_trans, 	0.5+((self.hd/2.0)*sine) + self.y_trans, 	-self.hc + self.z_trans)
		k5 = (self.fx +self.x_trans, 				self.y_trans, 								-self.hc + self.z_trans)
		tz = (self.tr + self.x_trans, 				self.y_trans, 								self.tz + self.z_trans)
		bz = (self.tr + self.x_trans, 				self.y_trans, 								-self.tz + self.z_trans)
		return {"e0": e0, "e1": e1, "e2": e2, "e3" : e3, "e4" : e4, "e5" : e5, "c1" : c1, "c3" : c3, "c5" : c5, "k1": k1, "k3" : k3, "k5" : k5, "tz" : tz, "bz" : bz}

	#returns a list of the three quads, each represented as a tuple (p1, p2, p3, p4)
	def buildQuads(self):
		q1 = (self.points["e0"], self.points["k1"], self.points["e1"], self.points["c1"])
		q3 = (self.points["e2"], self.points["k3"], self.points["e3"], self.points["c3"])
		q5 = (self.points["e4"], self.points["k5"], self.points["e5"], self.points["c5"])
		return [q1, q3, q5]

	#returns a list of the three top pentagons, each represented as a tuple (p1, p2, p3, p4, p5)
	def buildTopPentas(self):
		p0 = (self.points["e0"], self.points["c1"], self.points["tz"], self.points["c5"], self.points["e5"])
		p2 = (self.points["e2"], self.points["c3"], self.points["tz"], self.points["c1"], self.points["e1"])
		p4 = (self.points["e4"], self.points["c5"], self.points["tz"], self.points["c3"], self.points["e3"])
		return [p0, p2, p4]

	#returns a list of the three bottom pentagons, each represented as a tuple (p1, p2, p3, p4, p5)
	def buildBottomPentas(self):
		b0 = (self.points["e5"], self.points["k5"], self.points["bz"], self.points["k1"], self.points["e0"])
		b2 = (self.points["e1"], self.points["k1"], self.points["bz"], self.points["k3"], self.points["e2"])
		b4 = (self.points["e3"], self.points["k3"], self.points["bz"], self.points["k5"], self.points["e4"])
		return [b0, b2, b4]

	#takes in a shape represented as a tuple of points (p1, p2, p3) and returns a list of edges assuming 
	#the shape is closed and the points are listed in counterclockwise order. ex: [(p1, p2), (p2, p3), (p3, p1)]
	def getEdges(self, shape):
		edges = []
		for i in range(0, len(shape)):
			if (i != len(shape) - 1):
				edges += [(shape[i], shape[i+1])]
			else:
				edges += [(shape[i], shape[0])]
		return edges

	#returns a list of 21 tuples representing edges for the entire nonahedron. ex: [(p1, p2), (p2, p3), ...]
	def getAllEdges(self):
		allshapes = self.quads + self.topPentas + self.bottomPentas
		alledgelists = [self.getEdges(shape) for shape in allshapes]
		alledges = []
		for listofedges in alledgelists:
			alledges += listofedges
		return list(set(alledges))

	def rebuild(self):
		self.points = self.buildPoints()
		if (self.rot_x != 0 or self.rot_y != 0 or self.rot_z != 0):
			self.rotate()
		self.quads = self.buildQuads()
		self.topPentas = self.buildTopPentas()
		self.bottomPentas = self.buildBottomPentas()
		self.edges = self.getAllEdges()

	#rotates point about the x-axis by angle.
	def rotate_point_x(self, point, angle):
		if (angle == 0):
			return point
		theta = math.radians(angle)
		sine = math.sin(theta)
		cosine = math.cos(theta)
		x = point[0]
		y = point[1]
		z = point[2]
		return (x, y*cosine - z*sine, z*cosine + y*sine)

	#rotates point about the y-axis by angle.
	def rotate_point_y(self, point, angle):
		if (angle == 0):
			return point
		theta = math.radians(angle)
		sine = math.sin(theta)
		cosine = math.cos(theta)
		x = point[0]
		y = point[1]
		z = point[2]
		return (x*cosine - z*sine, y, z*cosine + x*sine)

	#rotates point about the z-axis by angle. 
	# http://petercollingridge.appspot.com/3D-tutorial/rotating-objects
	def rotate_point_z(self, point, angle):
		if (angle == 0):
			return point
		theta = math.radians(angle)
		sine = math.sin(theta)
		cosine = math.cos(theta)
		x = point[0]
		y = point[1]
		z = point[2]
		return (x*cosine - y*sine, y*cosine + x*sine, z)

	# #rotates point about the y-axis by angle. Axis should be a triple eg: (1, 0, 0) is x-axis.
	# def rotate_point_axis(self, point, angle, axis):
	# 	if (angle == 0):
	# 		return point
	# 	theta = math.radians(angle)
	# 	sine = math.sin(theta)
	# 	cosine = math.cos(theta)
	# 	x = point[0]
	# 	y = point[1]
	# 	z = point[2]
	# 	return 

	def rotate(self):
		for key in self.points:
			self.points[key] = self.rotate_point_x(self.points[key], self.rot_x)
			self.points[key] = self.rotate_point_y(self.points[key], self.rot_y)
			self.points[key] = self.rotate_point_z(self.points[key], self.rot_z)
		self.quads = self.buildQuads()
		self.topPentas = self.buildTopPentas()
		self.bottomPentas = self.buildBottomPentas()
		self.edges = self.getAllEdges()
