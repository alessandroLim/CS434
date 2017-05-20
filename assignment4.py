import numpy as np
import random as rand
import math, csv

def read_from_file():
	with open("data.txt", 'r') as f:
		data = csv.reader(f);
		data =  list(data);
	return data;

def temp_print_to_file(data):
	with open("cluster.csv", "w") as f:
		f. write("cluster1\n")
		for line in data[0]:
			line = ','.join(line)
			f.write(line)
			f.write('\n')
		f.write("cluster2\n")
		for line in data[1]:
			line = ','.join(line)
			f.write(line)
			f.write('\n')

def euclidean_distance(point1,point2):
	total = 0;
	for i in range(0, len(point1)):
		total = total + pow((float(point1[i])-float(point2[i])),2);
	total = math.sqrt(total)
	return total

def find_SSE(points,center):
	error = 0.
	for x in range(0,len(points)):
		for y in range(0,len(points[x])):
			for z in range(0, len(points[x][y])):
				error = error + pow(float(points[x][y][z]) - float(center[x][z]),2);
	return error;

def kmeans(data, k):
	center = [];

	do = 0;
	for i in range(0,k):
			center.append(data[rand.randint(0, len(data))]);
	while(do < 10):
		print ("Start new iteration")
		newcenter = [];
		points = [];
		change = 0
		for i in range(0,k):
			points.append([]);
			newcenter.append([]);
		temp = data[0]
		for x in range(0,len(data)):
			addto = k+1;
			mindistance = 999999999999999999999;
			for y in range(0,k):
				if(mindistance > euclidean_distance(center[y],data[x])):
					mindistance = euclidean_distance(center[y],data[x])
					addto = y;
			#print(addto);
			points[addto].append(data[x]);

		#print (len(points[0]));
		#print (len(points[1]));
		temp_print_to_file(points)
		do = 1;

		print("Error : " + str(find_SSE(points,center)))
		for x in range (0,k):
			print(len(points[x]))

		#temp_print_to_file(points)
		for x in range(0, k):
			TotalInArea = [0]*len(data[0])
			for y in range(0,len(points[x])):
				for i in range(0,784):
					TotalInArea[i] = TotalInArea[i] + float(points[x][y][i])
			for i in range(0,784):
					newcenter[x].append(TotalInArea[i]/len(points[x]));

		for x in range(0, k):
			similarity = 0
			for y in range(0,784):
				#print("newcenter = "+str(newcenter[x][y]))
				#print("oldcenter = "+str(center[x][y]))
				if(newcenter[x][y]-float(center[x][y])==0):
					similarity= similarity + 1
				#	print ("sim")
			print (similarity)
			if(similarity == 784):
				change= change+1
			#print("change ="+str(change))
		if (change == k):
			return center
		else:
			center = newcenter

class Cluster:

	def __init__(self, vec = [], lhs = None, rhs = None, dist = 0, node_id = None):
		self.vec = vec
		self.lhs, self.rhs = lhs, rhs
		self.dist, self.node_id = dist, node_id
# https://www.cnblogs.com/Key-Ky/p/3440684.html
# https://nlp.stanford.edu/IR-book/html/htmledition/time-complexity-of-hac-1.html
# http://bluewhale.cc/2016-04-19/hierarchical-clustering.html
def hac_single_link(dist_vec, n):
	clusters = [Cluster(vec = dist_vec[i], node_id = i) for i in range(len(dist_vec))]
	dist_set = {}
	tmp_pos, tmp_id = None, None
	while len(clusters) > n:
		min_dist = 999999999999999999999
		for i in range(len(clusters) - 1):
			for j in range(i + 1, len(clusters)):
				ids = clusters[i].id, clusters[j].id
				if dist_set.get(ids) == None: dist_set[ids] = euclidean_distance(ids[0], ids[1])
				tmp_dist = euclidean_distance(ids[0], ids[1])
				if tmp_dist < min_dist:
					min_dist, tmp_pos = tmp_dist, (i, j)
		lhs, rhs = tmp_pos
		new_vec = [(clusters[lhs].vec[i] + clusters[rhs].vec[i]) / 2 for i in range(len(clusters[lhs].vec))]
		new_cluster = Cluster(vec = new_vec, lhs = clusters[lhs], rhs = clusters[rhs], dist = min_dist, id = tmp_id)
		clusters[lhs], clusters[rhs] = [], []
		clusters.append(new_cluster)
	return clusters

def hac_single_dist(dist, row, col):
    rows, cols = dist.shape
    min_dist = 999999999999999999999
    for i in range(rows):
        for j in range(cols):
            tmp_dist = dist[row[i]][col[j]];
            if tmp_dist < min_dist: min_dist = tmp_dist
    return min_dist

def hac_complete_dist(dist, row, col):
    rows, cols = dist.shape
    max_dist = 0
    for i in range(rows):
        for j in range(cols):
            tmp_dist = dist[row[i]][col[j]];
            if tmp_dist > max_dist: max_dist = tmp_dist
    return max_dist

if __name__ == "__main__":
	data =  read_from_file();
	center = kmeans(data,2);
	print(center)
