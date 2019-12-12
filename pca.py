import argparse
import numpy as np
import mdtraj as md
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-activextc", "--axtc", help="xtc")
parser.add_argument("-activegro", "--agro", help="topology")
parser.add_argument("-inactivextc", "--inxtc", help="xtc")
parser.add_argument("-inactivegro", "--ingro", help="topology")
parser.add_argument("-stride", "--stride", help="stride", type=int)
args = parser.parse_args()

##################################### READ ME ###############################
## Code For Finding Some Principal Analysis Characteristics from two trajs ##
## Method 1: Heat Map in Time the "global(xyz)" movements of each Calph    ##
## Method 2: Pick Random Time points and graph movmenets of each Calph     ##
## Method 3: Average "global" movments and then graph for each Calph       ##
#############################################################################

def load_traj(xtc,top,stride):
	traj=md.load(str(xtc), top = str(top), stride = int(stride))
	print("Number of Frames Loaded:" + str(traj.n_frames))
	topology = traj.topology
	return traj, topology

def get_CA_coords(traj,topology):
    CA = topology.select('name CA')
    CAxyz=list([] for _ in range(traj.n_frames))
    for nn  in range(traj.n_frames):
        for i in range(len(CA)):
            CAi=CA[i]
            CAxyz[nn].append(traj.xyz[nn][CAi][0:3:1])
    return CAxyz

class cA(object):
	def __init__(self,int,xa,ya,za):
		self.int=int
		self.xa,self.ya,self.za = xa,ya,za

inactive_traj, inactive_topolgy = load_traj(args.inxtc, args.ingro, 10000)
active_traj, active_topology = load_traj(args.axtc,args.agro,args.stride)

inactive_CA_coords = get_CA_coords(inactive_traj, inactive_topolgy)
active_CA_coords = get_CA_coords(active_traj,active_topology)

re_cast_matrix =[]
for i in range(len(active_CA_coords[0])):
    local=[]
    for nn in range(active_traj.n_frames):
        local.append(np.array(active_CA_coords[nn][i]))
    re_cast_matrix.append(np.array(local))

res_list=[]
for i in range(len(re_cast_matrix)):
	res_list.append(cA(inactive_CA_coords[0][i],re_cast_matrix[i][:,0],
	re_cast_matrix[i][:,1],re_cast_matrix[i][:,2]
	))

frame_avg_dev = list([] for _ in range(active_traj.n_frames))
x = list([] for _ in range(active_traj.n_frames))
y = list([] for _ in range(active_traj.n_frames))
z = list([] for _ in range(active_traj.n_frames))
for nn in range(active_traj.n_frames):
	for res in res_list:
		x[nn].append(res.xa[nn] - res.int[0])
		y[nn].append(res.ya[nn] - res.int[1])
		z[nn].append(res.za[nn] - res.int[2])

for nn in range(active_traj.n_frames):
	frame_avg_dev[nn] = np.array([np.mean(x[nn]),np.mean(y[nn]),np.mean(z[nn])])


for nn in range(active_traj.n_frames):
	for res in res_list:
		res.xa[nn]=res.xa[nn] - frame_avg_dev[nn][0]
		res.ya[nn]=res.ya[nn] - frame_avg_dev[nn][1]
		res.za[nn]=res.za[nn] - frame_avg_dev[nn][2]

x_avg,y_avg,z_avg  = [],[],[]
x_std,y_std,z_std  = [],[],[]
for res in res_list:
	x_avg.append(np.mean(res.xa-res.int[0]))
	x_std.append(np.std(res.xa-res.int[0]))
	y_avg.append(np.mean(res.ya -res.int[1]))
	y_std.append(np.std(res.ya-res.int[1]))
	z_avg.append(np.mean(res.za-res.int[2]))
	z_std.append(np.std(res.za-res.int[2]))

x = np.arange(161,len(res_list)+161,1)
fig1, (figure)= plt.subplots(nrows=1, figsize=(15,5))

plt.errorbar(x,x_avg,yerr=x_std,fmt='o')
plt.xlabel("Amino Acid")
plt.ylabel("nm")
plt.title("X-Distance")
plt.show()

fig1, (figure)= plt.subplots(nrows=1, figsize=(15,5))
plt.errorbar(x,y_avg,yerr=y_std,fmt='o')
plt.xlabel("Amino Acid")
plt.ylabel("nm")
plt.title("Y-Distance")
plt.show()

fig1, (figure)= plt.subplots(nrows=1, figsize=(15,5))
plt.errorbar(x,z_avg,yerr=z_std,fmt='o')
plt.xlabel("Amino Acid")
plt.ylabel("nm")
plt.title("Z-Distance")
plt.show()
