import math

class Nonahedron:

	def __init__(self, ex, rc, hc, tz):
		self.ex = ex
		self.rc = rc
		self.hc = hc
		self.tz = tz
		self.points = self.buildPoints()
		self.quads = self.buildQuads()
		self.topPentas = self.buildTopPentas()
		self.bottomPentas = self.buildBottomPentas()
		self.edges = self.getAllEdges()

	#returns a dictionary with 14 "name":(x, y z) entries.
	def buildPoints(self):
		e0 = (self.ex, 0.5, 0)
		e1 = (-self.ex*0.5 +0.866*0.5, self.ex*0.866 +0.5*0.5,  0)
		e2 = (-self.ex*0.5 -0.866*0.5, self.ex*0.866 -0.5*0.5,  0)
		e3 = (-self.ex*0.5 -0.866*0.5, -self.ex*0.866 +0.5*0.5,  0)
		e4 = (-self.ex*0.5 +0.866*0.5, -self.ex*0.866 -0.5*0.5,  0)
		e5 = (self.ex,				   -0.5,  					0)
		c1 = (self.rc*0.5,  			self.rc*0.866,  	self.hc)
		c3 = (-self.rc,  				0, 					self.hc)
		c5 = (self.rc*0.5,  			-self.rc*0.866,  	self.hc)
		k1 = (self.rc*0.5, 				self.rc*0.866,  	-self.hc)
		k3 = (-self.rc, 				0,  				-self.hc)
		k5 = (self.rc*0.5, 				-self.rc*0.866, 	-self.hc)
		tz = (0,  						0, 					self.tz)
		bz = (0,  						0,  				-self.tz)
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
		self.quads = self.buildQuads()
		self.topPentas = self.buildTopPentas()
		self.bottomPentas = self.buildBottomPentas()
		self.edges = self.getAllEdges()
