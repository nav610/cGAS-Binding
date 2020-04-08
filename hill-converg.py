import argparse
import numpy as np
import matplotlib.pyplot as plt

parser=argparse.ArgumentParser()
parser.add_argument("-hill","--hill",help="grid file to graph")
parser.add_argument("-time","--time",help="simulationtime")
args=parser.parse_args()

hills=[]
f = open(args.hill,'r') 
for line in f.readlines()[4:]:
    if not line.startswith('#'):
        hills.append(float(line.split()[len(line.split())-2])) 
time = np.linspace(0,int(args.time),len(hills))
fig, (figure)= plt.subplots(nrows=1, figsize=(8,5))
figure.plot(time,hills,color='black')
plt.xlabel("ns")
plt.ylabel("kJ/mol")
plt.title("Gaussian Hill Energy Height Deposition")
plt.savefig('hills-graphed.png')

