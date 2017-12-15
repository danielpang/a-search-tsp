import sys
from scipy.spatial import distance
from queue import PriorityQueue
import copy

# Class for the city nodes
# Used to stores cities as nodes in a graph
# Has name of city along with x and y positions on a 2D plane
class Node:
	def __init__(self, city="", x=0, y=0):
		self.name = city
		self.x = x
		self.y = y

# Class for the search states
# A* search uses these states to store possible traversal of city nodes
# and to determine which path to take based on backward and forward costs i.e. f(n) = g(n) + h(n)
class State:
	def __init__(self, u_nodes=[], v_nodes=[], current_node=None, f_score=sys.maxsize):
		self.unvisited_nodes = u_nodes
		self.visited_nodes = v_nodes
		self.node = current_node
		self.f_score = f_score

# Helper function for Prim's algorithm
# Method to find the node in PriorityQueue Q with the lowest edge weight
def min_key(nodes, key, mst_set):
	minimum = sys.maxsize
	# For all the nodes in the PriorityQueue
	for node in nodes:
		# If the key is smaller than the minimum weight and is NOT in the MST
		if key[node.name] < minimum and mst_set[node.name] == False:
			minimum = key[node.name]
			min_index = node
	return min_index

# Prim's algorithm to find the minimum spanning tree of all unvisited nodes
# This is used as a part of the heuristic function to estimate the cost it takes
# to travel to all the unvisited nodes (forward cost)
def prim(unvisited_nodes, edges):
	nodes = copy.deepcopy(unvisited_nodes)
	# Initialize all dicts, initially all keys will be maxsize and predecessor will be None
	key = {}
	pred = {}
	mst_set = {}
	for n in nodes:
		pred[n.name] = None
		key[n.name] = sys.maxsize
		mst_set[n.name] = False
	# Declare dict values for starting node A
	key[nodes[0].name] = 0
	pred[nodes[0].name] = None

	for n in nodes:
		# Find the node with the smallest edge weight
		u = min_key(nodes, key, mst_set)
		# Add it to the minimum spanning tree (MST) by setting flag to true
		mst_set[u.name] = True
		# Go through all the neighbours of node u, which in this problem is all the other cities
		for node in nodes:
			# If neighbour of u is not in the MST, and current key is larger than the edge between u and neighbour
			if node.name != u and mst_set[node.name] == False and key[node.name] > edges[node.name, u.name]:
				# Update key of neighbour node and make u the predecessor of the neighbour
				key[node.name] = edges[node.name,u.name]
				pred[node.name] = u
	# Calculate the cost of our Minimum spanning tree
	mst_cost = 0
	for key in pred:
		if pred[key] != None:
			mst_cost += edges[key, pred[key].name]
	return mst_cost

# Heuristic function for A* Search
# h(n) at node n is the minimum spanning tree of remaining cities +
# distance to the NEAREST unvisited node + nearest distance from unvisted node
# to the starting node
def h(cur_node, unvisited_nodes, edges):
	# If we are at the goal state (visited all nodes)
	# then h(n) = 0
	if len(unvisited_nodes) == 0:
		return 0
	# Calculate distance to the NEAREST unvisited node from current node
	nearest_unvisited = sys.maxsize
	for n in unvisited_nodes:
		if n.name != cur_node.name and edges[n.name, cur_node.name] < nearest_unvisited:
			nearest_unvisited = edges[n.name, cur_node.name]
	# Calculate NEAREST distance from an unvisited node to the start node
	nearest_unvisited_to_start = sys.maxsize
	for n in unvisited_nodes:
		if edges['A', n.name] < nearest_unvisited_to_start:
			nearest_unvisited_to_start = edges['A', n.name]
	# Calculate nearest distance to travel all other unvisited nodes
	return prim(unvisited_nodes, edges) + nearest_unvisited + nearest_unvisited_to_start

# Similar to g(n), cost of the path from start node to n
# cur_path: is the list of nodes visited in order
def g(cur_path, edges):
	cost = 0
	# Find the cost of the path by calculating the edges between each node in the path
	for i in range(0, len(cur_path) - 1):
		cost += edges[cur_path[i].name, cur_path[i+1].name]
	return cost

# Determines the f score of the current state
# f(n) = g(n) + h(n)
def f(cur_path, cur_node, unvisited_nodes, edges):
	return g(cur_path, edges) + h(cur_node, unvisited_nodes, edges)

# Determines the cost of the chosen path
def build_path(path, edges):
	path_cost = 0
	lst = []
	freq = {}
	for i in range(0, len(path) - 1):
		lst.append(path[i].name)
		path_cost += edges[path[i].name, path[i+1].name]
	# Add cost from last city to start city
	lst.append('A')
	path_cost += edges[path[len(path) - 1].name, path[0].name]
	return {"path": lst, "cost": path_cost}

# Remove node from the list of nodes
# Returns a new list without the given node
def remove_node(nodes, city):
	new_lst = copy.deepcopy(nodes)
	for i in range(0, len(new_lst)):
		if new_lst[i].name == city:
			new_lst.pop(i)
			break
	return new_lst

# Implements the main A* search algorithm
def a_search(unvisited_nodes, edges):
	cur_path = []
	# Create initial start state with the starting city A
	start_node = unvisited_nodes[0]
	unvisited_nodes = remove_node(unvisited_nodes, 'A')
	f_start = f(cur_path, start_node, unvisited_nodes, edges)
	start_state = State(unvisited_nodes, [start_node], start_node, f_start)
	num_states = 1
	open_set = PriorityQueue()
	open_set.put((f_start, 1, start_state))
	# Continue expanding nodes until there are no more nodes to expand
	while not open_set.empty():
		# Obtain state with smallest f_score, top node from min heap
		item = open_set.get()
		cur_state = item[2]
		# We have chosen cur_state leaf node for expansions
		cur_path.append(cur_state.node)
		# If we have no more nodes to visited, we have reached goal state
		if len(cur_state.unvisited_nodes) == 0:
			num_states += 1 # for the goal state
			return build_path(cur_state.visited_nodes, edges)
		# Expand the nodes, adding the next level of nodes
		for unvisited in cur_state.unvisited_nodes:
			num_states += 1
			visited = copy.deepcopy(cur_state.visited_nodes)
			visited.append(unvisited)
			temp_lst = remove_node(cur_state.unvisited_nodes, unvisited.name)
			# Calculate f_score for this new state
			f_score = f(visited, unvisited, temp_lst, edges)
			s = State(temp_lst, visited, unvisited, f_score)
			# Add new state to the open_set of states to explore
			open_set.put((f_score, num_states, s))
	return 0

# Creates a node for each city
def create_nodes(file):
	next(file)
	lst = []
	for line in file:
		line = line.rstrip('\n')
		vals = line.split()
		n = Node(str(vals[0]), int(vals[1]), int(vals[2]))
		lst.append(n)
	return lst

# Calculates the cost (Euclidean distance) of travel
# between 2 nodes
def calculate_cost(lst):
	dict = {}
	for node in lst:
		for other_node in lst:
			a = (node.x,node.y)
			b = (other_node.x,other_node.y)
			dst = distance.euclidean(a,b)
			dict[node.name,other_node.name] = dst
	return dict

def main():
	# Example use of 'a_search'
	# Open file
	file = open(sys.argv[1], 'r')
	unvisited_nodes = create_nodes(file)
	edge_costs = calculate_cost(unvisited_nodes)
	results = (a_search(unvisited_nodes, edge_costs))
	print("Path of Nodes to visit are", results['path'])
	print("Cost of Path is", round(results['cost'],2))

if __name__ == '__main__':
	main()
