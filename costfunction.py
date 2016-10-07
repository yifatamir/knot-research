import numpy as np

def cost_function(nonahedron, alpha, beta, gamma):
	eld = ELD(nonahedron)
	pad = PAD(nonahedron)
	fnp = FNP(nonahedron)
	print("eld: " +  str(eld))
	print("pad: " + str(pad))
	print("fnp: " + str(fnp))
	return alpha*eld + beta*pad + gamma*fnp

def ELD(nonahedron):
	all_edges = nonahedron.edges
	lengths = [edgelength(edge) for edge in all_edges]
	avg_length = mean(lengths)
	squared_devs = [(length - avg_length)**2 for length in lengths]
	result = sum(squared_devs)
	return result

def PAD(nonahedron):
	quads = nonahedron.quads
	listlist_quad_edges = [nonahedron.getEdges(quad) for quad in quads]
	listlist_quad_angles = [angles_of_edges(list_quad_edges) for list_quad_edges in listlist_quad_edges]
	quad_angles = []
	for list_quad_angles in listlist_quad_angles:
		quad_angles += list_quad_angles
	quads_dev = sum([(angle - 90)**2 for angle in quad_angles])
	pentas = nonahedron.topPentas + nonahedron.bottomPentas
	listlist_pent_edges = [nonahedron.getEdges(pent) for pent in pentas]
	listlist_pent_angles = [angles_of_edges(list_pent_edges) for list_pent_edges in listlist_pent_edges]
	pent_angles = []
	for list_pent_angles in listlist_pent_angles:
		pent_angles += list_pent_angles
	pents_dev = sum([(angle - 108)**2 for angle in pent_angles])
	result = quads_dev + pents_dev
	return result

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

#takes in the list of edges in a shape [(p1, p2), (p2, p3), (p3, p1)] and returns a list of angles in that shape.
# ex: [60, 60, 60]
def angles_of_edges(list_of_edges):
	angles = []
	for i in range(0, len(list_of_edges)):
		edge = list_of_edges[i]
		if (i != len(list_of_edges) - 1):
			next_edge = list_of_edges[i + 1]
		else:
			next_edge = list_of_edges[0]
		vector_of_edge = vectorize(edge)
		vector_of_next_edge = vectorize(next_edge)
		angle = abs(angle_between(vector_of_edge, vector_of_next_edge))
		if (angle > 180):
			angle = 360 - angle
		angles += [angle]
	return angles