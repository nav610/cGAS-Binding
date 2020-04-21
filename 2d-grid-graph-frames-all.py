import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import matplotlib.ticker as ticker
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FormatStrFormatter
parser=argparse.ArgumentParser()
parser.add_argument("-grid","--grid",help="grid file to graph")
parser.add_argument("-name","--name",help="title of plot")
parser.add_argument("-frames","--frames",help="frame list")
parser.add_argument("-frames2","--frames2",help="frames.all")

args=parser.parse_args()

def convert_CV2(value):
    return(int(value*100))

def convert_CV1(value):
    return(int(10*value+31.4))

def find_nearest(array,value):
    array = np.asarray(array)
    idx = (np.abs(array-value)).argmin()
    return array[idx]

data=[]
f = open(args.grid)
for i in f.readlines()[9:]:
    if len(i.strip()) ==0:
        pass
    else:data.append(i)
f.close()

previous_angle = float(data[0].split()[1])
local,arr=[],[]
for row in data:
    angle = float(row.split()[1])
    if angle == previous_angle:
        local.append(float(row.split()[2]))
    else:
        arr.append(local)
        previous_angle=angle
        local=[]
        local.append(float(row.split()[2]))

frames = [] 
f = open(args.frames)
for i in f.readlines():
    line=i.split(",")
    frames.append([float(line[1]),float(line[2])])

frames_all= [] 
f = open(args.frames2)
for i in f.readlines():
    line=i.split(",")
    frames_all.append([float(line[0]),float(line[1])])
print(args.frames2)

arr =np.array(arr)* .239
arr_df = pd.DataFrame(arr)
col = np.around(np.linspace(0,5.5,len(arr[0])),1)
row = np.around(np.linspace(-3.14,3.14,len(arr)),2)
arr_df.columns = col
arr_df.index = row

cmap1= matplotlib.colors.ListedColormap(['navy','indigo','mediumvioletred',
    'darkorchid','palevioletred','orangered','darkorange','bisque'])

initPoint = frames[0]
print(initPoint)
min = arr[int(initPoint[1]),int(initPoint[0])]
arr=arr-min
arr_df = arr_df - min

fig = plt.figure()
ytick = np.around(np.linspace(-3.14,3.14,62),3)
graph1 = sns.heatmap(-arr_df,yticklabels=5,
        xticklabels=50,cmap=cmap1,cbar_kws={'label': 'kcal/mol'})


graph1.set_xlim(60,310)
graph1.set(ylabel='CV2 [rad]',xlabel='CV1 [nm]')

for i in frames_all: 
    plt.plot(i[0],i[1],marker=".",markersize=4,color="white")

for i in range(len(frames)):
    if frames[i] in frames_all:
        plt.text(frames[i][0],frames[i][1],str(i),color='white')

plt.savefig(args.name + "-path-all.png")





