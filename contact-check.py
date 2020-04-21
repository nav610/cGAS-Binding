import mdtraj as md 
import numpy as np 
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-xtc", "--xtc", help = "xtc file")
parser.add_argument("-gro", "--gro", help = "gro file")
parser.add_argument("-out", "--out", help = "out file name")
parser.add_argument("-atom", "--atom", help = "atom, resSeq ? and name ?")

args = parser.parse_args() 

def load_traj(xtc,top,stride):
	traj=md.load(str(xtc), top = str(top), stride = int(stride))
	print("Number of Frames Loaded:" + str(traj.n_frames))
	topology = traj.topology
	return traj, topology

def return_2D_matrix(stan,protien):
	out = []	
	for atom in cGAS: 
		out.append([stan,atom])
	return out

def find_3A(distMatrix,time,atom):
	out = []
	for i in range(len(distMatrix)): 
		dist = distMatrix[i]
		if dist < .4:
			out.append([time,dist,atom,i])
	return out


traj,top = load_traj(args.xtc,args.gro,1)

atom = top.select(str(args.atom))
print(atom)

cGAS = top.select("protein")

Matrix = return_2D_matrix(atom[0],cGAS)

dist_Matrix = md.compute_distances(traj,Matrix)
print(dist_Matrix)

lessThan3A = []
for nn in range(traj.n_frames):
	nearest = find_3A(dist_Matrix[nn],nn,atom[0])	
	lessThan3A.append(nearest)

f = open(args.atom+".txt","w+")
for nn in range(traj.n_frames):
	for line in lessThan3A[nn]: 
		f.write(str(line[0]) + "," +str(line[1]) + "," + str(line[2]) + "," + str(line[3]))
		f.write("\n")
f.close()




