import numpy as np

def cost_function(nonahedron, alpha, beta, gamma):
	return alpha*ELD(nonahedron) + beta*PAD(nonahedron) + gamma*FNP(nonahedron)

def ELD(nonahedron):
	all_edges = nonahedron.edges
	lengths = [edgelength(edge) for edge in all_edges]
	avg_length = mean(lengths)
	squared_devs = [(length - avg_length)**2 for length in lengths]
	return sum(squared_devs)

def PAD(nonahedron):
	quads = nonahedron.quads
	pentas = nonahedron.topPentas + nonahedron.bottomPentas

def FNP(nonahedron):
	return 0

#returns the Euclidean distance between two points that make up an edge. 
#the edge passed in to this function is of type ((x1, y1, z1), (x2, y2, z2)).
def edgelength(edge):
	a = np.array(edge[0])
	b = np.array(edge[1])
	return np.linalg.norm(a-b)

#takes in a list of numbers and computes the average
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

#takes in an edge (p1, p2) and returns a vector from the origin (dx, dy, dz) representing that edge.
def vectorize(edge):
	p1 = edge[0]
	p2 = edge[1]
	return (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])

#returns the unit vector representing the given vector
def unit_vector(vector):
    return vector / np.linalg.norm(vector)

#returns the angle in degrees between two vectors. ex: angle_between((1, 0, 0), (-1, 0, 0)) will output 180
def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.rad2deg(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))