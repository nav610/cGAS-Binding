import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import matplotlib.ticker as ticker
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

parser=argparse.ArgumentParser()
parser.add_argument("-grid","--grid",help="grid file to graph")
parser.add_argument("-name","--name",help="title of plot")
parser.add_argument("-angle0","--angle0",help="angle naught")
parser.add_argument("-d0","--d0",help="d naught")
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

arr =np.array(arr)* .239
arr_df = pd.DataFrame(arr)
col = np.around(np.linspace(-55,55,len(arr[0])),2)
row = np.around(np.linspace(-3.14,3.14,len(arr)),2)
arr_df.columns = col

if args.angle0 is not None and args.d0 is not None:
    d0,angle0=np.round(float(args.d0),2),np.round(float(args.angle0),2)
    angle0_idx = np.where(row==find_nearest(row,angle0))[0][0]
    d0_idx = np.where(col==find_nearest(col,d0))[0][0]
    e_const=arr_df.at[angle0_idx,col[d0_idx]]
    arr_df = arr_df - float(e_const)

cmap1= matplotlib.colors.ListedColormap(['black','indigo','mediumvioletred',
    'orangered','darkorange','bisque'])
cmap2=sns.color_palette("RdBu",7)
cmap3=sns.color_palette("ch:2.5,-.2,dark=.3")
bounds = [0,1,2,3,4,5,6,7]
arr_df=arr_df

fig = plt.figure()
ytick = np.around(np.linspace(-3.14,3.14,62),3)
graph1 = sns.heatmap(-arr_df,
        yticklabels=ytick,xticklabels=50,cmap=cmap2)
for ind,label in enumerate(graph1.get_yticklabels()):
    if ind%10 == 0:
        label.set_visible(True)
    else: label.set_visible(False)

graph1.set_xlim(550,880)
graph1.set(ylabel='phi [rad]',xlabel='d [mE-11]')
plt.savefig(args.name+".png")

fig=plt.figure()
graph2=plt.contour(col,row,-arr,colors='black',levels=[0,15,20,25,30,35,40,45,50])
plt.clabel(graph2,fontsize='10',color='black')
plt.savefig(args.name+".contour.png")

fig = plt.figure()
graph3=Axes3D(fig)
X,Y = np.meshgrid(arr_df.columns,arr_df.index)
graph3.plot_surface(X, Y,-arr_df.values)
graph3.view_init(elev=35,azim=270)
plt.savefig(args.name + ".3D.png")
