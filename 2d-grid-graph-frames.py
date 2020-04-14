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
arr =np.array(arr)* .239
arr_df = pd.DataFrame(arr)
col = np.around(np.linspace(0,5.5,len(arr[0])),1)
row = np.around(np.linspace(-3.14,3.14,len(arr)),2)
arr_df.columns = col
arr_df.index = row

cmap1= matplotlib.colors.ListedColormap(['navy','indigo','mediumvioletred',
    'darkorchid','palevioletred','orangered','darkorange','bisque'])
cmap2=sns.color_palette("RdBu",11)
cmap3=sns.color_palette("ch:2.5,-.2,dark=.3")
cmap4=sns.color_palette("PuBu",8)
cmap5=plt.cm.get_cmap('Spectral')

initPoint = frames[0]
print(initPoint)
min = arr[int(initPoint[1]),int(initPoint[0])]
arr=arr-min
arr_df = arr_df - min

fig = plt.figure()
ytick = np.around(np.linspace(-3.14,3.14,62),3)
graph1 = sns.heatmap(-arr_df.loc[:,0:3.81],yticklabels=5,
        xticklabels=50,cmap=cmap1,cbar_kws={'label': 'kcal/mol'})
"""for ind,label in enumerate(graph1.get_yticklabels()):
    if ind%10 == 0:
        label.set_visible(True)
    else: label.set_visible(False)"""

graph1.set_xlim(0,210)
graph1.set(ylabel='CV2 [rad]',xlabel='CV1 [nm]')

for i in frames: 
    plt.plot(i[0],i[1],marker=".",markersize=4,color="white")
for i in range(len(frames)):
    plt.text(frames[i][0],frames[i][1],str(i),color='white')

plt.savefig(args.name + "-path.png")

fig = plt.figure()
graph1 = sns.heatmap(-arr_df.loc[:,0:3.82],yticklabels=5,
        xticklabels=50,cmap=cmap1,cbar_kws={'label': 'kcal/mol'})
graph1.set_xlim(0,310)
graph1.set(ylabel='CV2 [rad]',xlabel='CV1 [nm]')
#graph1.xaxis.set_ajor_formatter(FormatStrFormatter('%.1f'))
plt.savefig(args.name  + "-norm.png")


fig = plt.figure()
graph3=Axes3D(fig)
X,Y = np.meshgrid(arr_df.columns,arr_df.index)
graph3.plot_surface(X, Y,-arr_df.values)
graph3.view_init(elev=25,azim=270)
plt.savefig(args.name + "norm.3D.png")




