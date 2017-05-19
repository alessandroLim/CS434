import numpy as np
import random as rand
import math
import csv
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
		total = total + pow((float(point1[i])+float(point2[i])),2);
	total = math.sqrt(total)
	return total


def kmeans(data, k):
	center = [];
	points = [];
	do = 0;
	while(do == 0):
		newcenter = [];
		for i in range(0,k):
			center.append(data[rand.randint(0, len(data))]);
			points.append([]);
		temp = data[0]
		for x in range(0,len(data)):
			addto = k+1;
			tempdistance = 999999999999999999999;
			for y in range(0,k):
				if(tempdistance > euclidean_distance(center[y],data[x])):
					tempdistance = euclidean_distance(center[y],data[x])
					addto = y;
			#print(addto);
			points[addto].append(data[x]);
		#print (len(points[0]));
		#print (len(points[1]));
		temp_print_to_file(points)
		do = 1;

if __name__ == "__main__":
	data =  read_from_file();
	print(len(data))
	kmeans(data,2);