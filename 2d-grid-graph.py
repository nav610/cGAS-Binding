import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
parser=argparse.ArgumentParser()
parser.add_argument("-grid","--grid",help="grid file to graph")
parser.add_argument("-title","--title",help="title of plot")
args=parser.parse_args()

arr=(551,62)
arr = np.zeros(arr)

def convert_CV2(value):
    return(int(value*100))

def convert_CV1(value):
    return(int(10*value+31.4))

data=[]
f = open(args.grid)
for i in f.readlines()[9:]:
    if len(i.strip()) ==0:
        pass
    else:data.append(i)

for row in data:
    #print(row.split()[0],row.split()[1])
    CV2_index=convert_CV2(np.round(float(row.split()[0]),2))
    CV1_index=convert_CV1(np.round(float(row.split()[1]),2))
    bias=float(row.split()[2])
    arr[CV2_index,CV1_index]=bias

arr = arr*.239
xtick = np.around(np.linspace(-3.14,3.14,62),3)
ytick = np.around(np.linspace(0,5.5,552),3)

#plt.figure(figsize=(10,10))
graph = sns.heatmap(arr,vmin=np.amin(arr),vmax=np.amax(arr),xticklabels=xtick,
    yticklabels=ytick)
for ind,label in enumerate(graph.get_xticklabels()):
    if ind%10 == 0:
        label.set_visible(True)
    else: label.set_visible(False)
for ind,label in enumerate(graph.get_yticklabels()):
    if ind%50 == 0:
        label.set_visible(True)
    else: label.set_visible(False)
graph.set(xlabel='phi [rad]',ylabel='d [nm]')


plt.show()
