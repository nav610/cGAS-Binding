import mdtraj as md 
import numpy as np 
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-xtc", "--xtc", help = "xtc file")
parser.add_argument("-gro", "--gro", help = "gro file")
parser.add_argument("-out", "--out", help = "out file name")
parser.add_argument("-atom", "--atom", help = "atom, resSeq ? and name ?")

args = parser.parse_args() 

uniqueResList = [] 

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

def find_3A(distMatrix,nn,atom):
	out = []
	for i in range(len(distMatrix)): 
		dist = distMatrix[i]
		if dist < .4:
			time = .2*nn
			resname = resnames[i]
			out.append([time,dist,atom,i,resname])
			uniqueResList.append(resname)
	return out


traj,top = load_traj(args.xtc,args.gro,1)

resnames = [atom.residue for atom in top.atoms]
atom = top.select(str(args.atom))

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
		f.write(str(line[0]) + "," +str(line[1]) + "," + str(line[2]) + "," + str(line[3]) + "," + str(line[4]))
		f.write("\n")
f.close()

setUniqueResList = list(set(uniqueResList))

f = open(args.atom+"uniqueRes.txt","w+")
for item in setUniqueResList: 
	f.write(str(item))
	f.write("\n")
f.close()



