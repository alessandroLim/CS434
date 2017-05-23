import numpy as np
import random as rand
import math, csv

def read_from_file():
	with open("data-2.txt", 'r') as f:
		data = csv.reader(f)
		data =  list(data)
	return data

def read_from_file1():
	with open("data-1.txt", 'r') as f:
		data = csv.reader(f)
		data =  list(data)
	return data

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

def kmeans(data, k, threshold):
	center = [];
	with open("result"+str(k)+".txt", "w") as f:
		do = 0;
		f.write("k = "+ str(k)+"\n");
		for i in range(0,k):
				center.append(data[rand.randint(0, len(data))]);
		while(do < threshold):
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
			#print("Error : " + str(find_SSE(points,center)))
			f.write(str(find_SSE(points,center)));
			f.write("\n")
			#for x in range (0,k):
				#print(len(points[x]))

			#temp_print_to_file(points)
			for x in range(0, k):
				TotalInArea = [0]*len(data[0])
				if(len(points[x])==0):
					for a in range(0,k):
						print(len(points[a]), k)
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
				#print (similarity)
				if(similarity == 784):
					change= change+1
				#print("change ="+str(change))
			if (change == k):
				return center
			else:
				center = newcenter
				do = do+1

class Node:

	def __init__(self, points, self_id, pair_id):
		self.points = points
		self.self_id = self_id
		self.height = 0

def single_link_dist(clusters, calc):
	min_dist = 999999999999999999999
	lhs, rhs = None, None
	for i in range(len(clusters)):
		for j in range(i + 1, len(clusters)):
			# print '---', len(clusters[i].self_id), len(clusters[j].self_id)
			# min_dist = 999999999999999999999
			# for a in clusters[i].self_id:
			# 	for b in clusters[j].self_id:
			# 		if min_dist > calc[a][b]:
			# 			min_dist = calc[a][b]
			# 			lhs, rhs = i, j
			tmp_dist = calc[clusters[i].self_id[0]][clusters[j].self_id[0]]
			if tmp_dist < min_dist:
				min_dist = tmp_dist
				lhs, rhs = i, j
	return min_dist, lhs, rhs

def complete_link_dist(clusters, calc):
	max_dist = 0
	lhs, rhs = None, None
	for i in range(len(clusters)):
		for j in range(i + 1, len(clusters)):
			# tmp_dist = 0
			# for a in clusters[i].self_id:
			# 	for b in clusters[j].self_id:
			# 		if tmp_dist < calc[a][b]:
			# 			tmp_dist = calc[a][b]
			tmp_dist = calc[clusters[i].self_id[0]][clusters[j].self_id[0]]
			if tmp_dist > max_dist:
				max_dist = tmp_dist
				lhs, rhs = i, j
	return max_dist, lhs, rhs

def merge_cluster(cluster1,cluster2, min_dist):
	# print 'merge:', cluster2.self_id
	for i in range(len(cluster2.self_id)):
		cluster1.points.append(cluster2.points[i])
		cluster1.self_id.append(cluster2.self_id[i])
	cluster1.height = min_dist

def init_cluster(clusters):
	nodes = []
	for i in range(len(clusters)):
		nodes.append(Node([clusters[i]], [i], 0))
	calc = [];
	for i in range(len(clusters)):
		calc.append([]);
		for j in range(len(clusters)):
			calc[i].append(euclidean_distance(clusters[i],clusters[j]));
	return nodes, calc

def hac_single_link(clusters):
	nodes, calc = init_cluster(clusters)
	while len(nodes) > 1:
		min_dist, lhs, rhs = single_link_dist(nodes, calc)
		merge_cluster(nodes[lhs], nodes[rhs], min_dist)
		del nodes[rhs]
		if(len(nodes) == 10):
			print ("============== Single Link HAC ==============")
		if(len(nodes)<= 10):
			for i in range(len(nodes)):
				print(nodes[i].self_id, nodes[i].height)
			print("==========next============");

def hac_complete_link(clusters):
	nodes, calc = init_cluster(clusters)
	while len(nodes) > 1:
		max_dist, lhs, rhs = complete_link_dist(nodes, calc)
		merge_cluster(nodes[lhs], nodes[rhs], max_dist)
		del nodes[rhs]

		if(len(nodes) == 10):
			print ("============== Complete Link HAC ==============")
		if(len(nodes)<= 10):
			for i in range(len(nodes)):
				print(nodes[i].self_id, nodes[i].height)
			print("==========next============");

c = [
	    [123,    312,     434,     4325,   345345],
	    [23124,  141241,  434234,  9837489, 34743],
	    [128937, 127,     12381,   424,      8945],
	    [323,    4348,    5040,    8189,     2348],
	    [51249,  42190,   2713,    2319,     4328],
	    [13957,  1871829, 8712847, 34589,   30945],
	    [1234,   45094,   23409,   13495,  348052],
	    [49853,  3847,    4728,    4059,     5389]
	]

if __name__ == "__main__":
	# data =  read_from_file()
	# for i in range(2, 11):
	# 	kmeans(data, i, 1000000)
	data =  read_from_file()
	hac_single_link(data)
	hac_complete_link(data)
