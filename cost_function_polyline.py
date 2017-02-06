import numpy as np

def cost_function(polyline, alpha, beta, gamma):
	# eld = ELD(nonahedron)
	# pad = PAD(nonahedron)
	# fnp = FNP(nonahedron)
	# return (alpha*eld + beta*pad + gamma*fnp, eld, pad, fnp)
	return 0

# def ELD(nonahedron):
# 	all_edges = nonahedron.edges
# 	lengths = [edgelength(edge) for edge in all_edges]
# 	avg_length = mean(lengths)
# 	squared_devs = [(length - avg_length)**2 for length in lengths]
# 	result = sum(squared_devs)
# 	return result

# def PAD(nonahedron):
# 	quads = nonahedron.quads
# 	listlist_quad_edges = [nonahedron.getEdges(quad) for quad in quads]
# 	listlist_quad_angles = [angles_of_edges(list_quad_edges) for list_quad_edges in listlist_quad_edges]
# 	quad_angles = []
# 	for list_quad_angles in listlist_quad_angles:
# 		quad_angles += list_quad_angles
# 	quads_dev = sum([(angle - 0.5*np.pi)**2 for angle in quad_angles])
# 	pentas = nonahedron.topPentas + nonahedron.bottomPentas
# 	listlist_pent_edges = [nonahedron.getEdges(pent) for pent in pentas]
# 	listlist_pent_angles = [angles_of_edges(list_pent_edges) for list_pent_edges in listlist_pent_edges]
# 	pent_angles = []
# 	for list_pent_angles in listlist_pent_angles:
# 		pent_angles += list_pent_angles
# 	pents_dev = sum([(angle - 0.6*np.pi)**2 for angle in pent_angles])
# 	result = quads_dev + pents_dev
# 	return result

# def FNP(nonahedron):
# 	shapes = nonahedron.quads + nonahedron.topPentas + nonahedron.bottomPentas
# 	result = 0
# 	for shape in shapes:
# 		plane = compute_plane(shape)
# 		for point in shape:
# 			result += dist_of_point_from_plane(point, plane)**2
# 	return result

# #returns the Euclidean distance between two points that make up an edge. 
# #the edge passed in to this function is of type ((x1, y1, z1), (x2, y2, z2)).
# def edgelength(edge):
# 	a = np.array(edge[0])
# 	b = np.array(edge[1])
# 	return np.linalg.norm(a-b)

# #takes in a list of numbers and computes the average
# def mean(numbers):
#     return float(sum(numbers)) / max(len(numbers), 1)

# #takes in an edge (p1, p2) and returns a vector from the origin (dx, dy, dz) representing that edge.
# def vectorize(edge):
# 	p1 = edge[0]
# 	p2 = edge[1]
# 	return (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])

# #returns the unit vector representing the given vector
# def unit_vector(vector):
#     return vector / np.linalg.norm(vector)

# #returns the angle in radians between two vectors. ex: angle_between((1, 0, 0), (-1, 0, 0)) will output pi/2
# def angle_between(v1, v2):
#     v1_u = unit_vector(v1)
#     v2_u = unit_vector(v2)
#     return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

# #takes in the list of edges in a shape [(p1, p2), (p2, p3), (p3, p1)] and returns a list of angles in that shape.
# # ex: [60, 60, 60]
# def angles_of_edges(list_of_edges):
# 	angles = []
# 	for i in range(0, len(list_of_edges)):
# 		edge = list_of_edges[i]
# 		if (i != len(list_of_edges) - 1):
# 			next_edge = list_of_edges[i + 1]
# 		else:
# 			next_edge = list_of_edges[0]
# 		vector_of_edge = vectorize(edge)
# 		vector_of_next_edge = vectorize(next_edge)
# 		angle = abs(angle_between(vector_of_edge, vector_of_next_edge))
# 		if (angle > np.pi):
# 			angle = 2*np.pi - angle
# 		angles += [angle]
# 	return angles

# def x(point):
# 	return point[0]

# def y(point):
# 	return point[1]

# def z(point):
# 	return point[2]

# #returns the value of A in http://cs.haifa.ac.il/~gordon/plane.pdf using the given shape (p1, p2, ... pn)
# def computeA(shape):
# 	a_sum = 0
# 	num_points = len(shape)
# 	for i in range(0, num_points):
# 		point_i = shape[i]
# 		if (i == num_points - 1):
# 			point_ip1 = shape[0]
# 		else:
# 			point_ip1 = shape[i + 1]
# 		a_sum += (y(point_i) - y(point_ip1)) * (z(point_i) + z(point_ip1))
# 	return a_sum

# #returns the value of B in http://cs.haifa.ac.il/~gordon/plane.pdf using the given shape (p1, p2, ... pn)
# def computeB(shape):
# 	b_sum = 0
# 	num_points = len(shape)
# 	for i in range(0, num_points):
# 		point_i = shape[i]
# 		if (i == num_points - 1):
# 			point_ip1 = shape[0]
# 		else:
# 			point_ip1 = shape[i + 1]
# 		b_sum += (z(point_i) - z(point_ip1)) * (x(point_i) + x(point_ip1))
# 	return b_sum

# #returns the value of B in http://cs.haifa.ac.il/~gordon/plane.pdf using the given shape (p1, p2, ... pn)
# def computeC(shape):
# 	c_sum = 0
# 	num_points = len(shape)
# 	for i in range(0, num_points):
# 		point_i = shape[i]
# 		if (i == num_points - 1):
# 			point_ip1 = shape[0]
# 		else:
# 			point_ip1 = shape[i + 1]
# 		c_sum += (x(point_i) - x(point_ip1)) * (y(point_i) + y(point_ip1))
# 	return c_sum

# #returns the value of P (centroid point; center of gravity) in 
# #http://cs.haifa.ac.il/~gordon/plane.pdf using the given shape (p1, p2, ... pn)
# def computeP(shape):
# 	p_sum = (0, 0, 0)
# 	num_points = len(shape)
# 	for i in range(0, num_points):
# 		point_i = shape[i]
# 		p_sum = (x(p_sum) + x(point_i), y(p_sum) + y(point_i), z(p_sum) + z(point_i))
# 	p_sum = (x(p_sum)/num_points, y(p_sum)/num_points, z(p_sum)/num_points)
# 	return p_sum

# #returns the value of B in http://cs.haifa.ac.il/~gordon/plane.pdf using the given shape (p1, p2, ... pn)
# def computeD(shape, a, b, c):
# 	p = computeP(shape)
# 	n = (a, b, c)
# 	return -1 * dot_product(p, n)

# #takes in two vectors of the form (a, b, ... z) and returns their scalar dot product.
# def dot_product(v1, v2):
# 	result = 0
# 	if len(v1) != len(v2):
# 		return -1
# 	for i in range(0, len(v1)):
# 		result += v1[i] * v2[i]
# 	return result

# #computes the distance from point (x, y, z) to plane (a, b, c, d).
# def dist_of_point_from_plane(point, plane):
# 	x, y, z = point
# 	a, b, c, d = plane
# 	return a*x + b*y + c*z + d
	
# #returns the value of (A, B, C, D) for the best fitting plane of the given shape.
# def compute_plane(shape):
# 	a = computeA(shape)
# 	b = computeB(shape)
# 	c = computeC(shape)
# 	d = computeD(shape, a, b, c)
# 	return (a, b, c, d)
