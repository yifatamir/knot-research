import math
import numpy as np

class Polyline:

	#takes in a list of points i.e. [(1, 2, 3), (0, 1, 0)]
	def __init__(self, pnts, closed = True):
		self.points = pnts
		self.closed = closed
		self.edges = self.buildEdges(self.points, self.closed)

	def point_num(self, num):
		p = self.points[num]
		return p

	def buildEdges(self, points, closed):
		edges = []
		for i in range(0, len(points)):
			if (i != len(points) - 1):
				edges += [(points[i], points[i+1])]
			else:
				if (closed):
					edges += [(points[i], points[0])]
		return edges

	def rebuild(self):
		self.edges = self.buildEdges(self.points, self.closed)

	def generateBspline(self, plist):
    """
    Generate a cubic B-spline from the points in PLIST.
    Adapted from https://github.com/kawache/Python-B-spline-examples.
    """
    # Make point list into loop.
    first = plist[0]
    last = plist[-1]
    plist.insert(0, last)
    # Convert to numpy format.
    ctr = np.array(plist)
    # Split into components.
    x = ctr[:,0]
    y = ctr[:,1]
    z = ctr[:,2]
    # Define the knot vector, with k = 3 (degree of B-spline) equal ending points.
    l = len(x)
    t = np.linspace(0, 1, l-2, endpoint=True)
    t = np.append([0, 0, 0], t)
    t = np.append(t, [1, 1, 1])
    # Sequence of knots, coefficients, and degree.
    tck = [t, [x, y, z], 3]
    # Determine granularity of interpolation.
    u3 = np.linspace(0, 1, (max(l*2,70)), endpoint=True)
    # Evaluate the interpolation.
    out = interpolate.splev(u3,tck) 
    return out
