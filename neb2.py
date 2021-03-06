import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import matplotlib.ticker as ticker
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import copy
parser=argparse.ArgumentParser()
parser.add_argument("-grid","--grid",help="grid file to graph")
parser.add_argument("-images","--images",help="# of intermediate images")
parser.add_argument("-initial","--initial", help="initial position", nargs='+')
parser.add_argument("-final","--final", help="final position",nargs='+')

args = parser.parse_args()
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
arr = np.array(arr)
arr = arr.transpose()
arr = arr*.239
initial = np.array(args.initial).astype(int)
final = np.array(args.final).astype(int)
arr =np.array(arr)

#(1) Pick Random Path knowing the two endpoints
class image(object):
    def __init__(self,pos,pot,springLeft,springRight):
        self.pos = pos
        self.pot = pot
        self.springLeft = springLeft
        self.springRight = springRight
def make_line(initial,final):
    """Makes a straight line from intial to final"""
    slope = (final[1]-initial[1])/(final[0]-initial[0])
    const = final[1]-slope*final[0]
    print(slope,const)
    return(slope,const)

def space_line(slope,const,initial,final,numImages):
    """Evenly places points on a line"""
    spacing = np.linalg.norm(final-initial)/int(numImages)
    if final[0]<initial[0]: sign = -1
    else: sign=1
    points = []
    for i in range(int(numImages)):
        x = initial[0] + sign*i*spacing
        y = x*slope + const
        points.append([int(x),int(y)])
    points.append([final[0],final[1]])
    return(points,spacing)

def distance(a,b):
    return(np.linalg.norm(np.array(a)-np.array(b)))

def get_potential(cord,arr):
    return(arr[cord[0],cord[1]])

def calc_springEnergy(xi,xf,x0,k):
    """Calculate Spring Energy"""
    springV = (distance(xi,xf)-x0)**2
    return (k*springV/2)

def calc_spring(initPath,x0,k):
    """Initialize Spring Energy into initPath"""
    for i in range(1,len(initPath)-1):
        left = calc_springEnergy(initPath[i].pos,initPath[i+1].pos,x0,k)
        right = calc_springEnergy(initPath[i].pos,initPath[i-1].pos,x0,k)
        initPath[i].springLeft=left
        initPath[i].springRight=right
    initPath[0].springRight = initPath[1].springLeft
    initPath[len(initPath)-1].springLeft = initPath[len(initPath)-2].springRight

def init_path(points,arr):
    """Initailize Linear Path"""
    initalImages = []
    for cord in points:
        pot = get_potential(cord,arr)
        springLeft = 0
        springRight = 0
        initalImages.append(image(cord,pot,springLeft,springRight))
    return(initalImages)

def perturbPos(pos,delta,arr):
    theta = np.random.ranf()*np.pi
    d = np.random.randint(1,delta)
    dx,dy = d*np.cos(theta),d*np.sin(theta)
    newPos = np.array(pos) + np.array([dx,dy])
    if checkifPosonGrid(newPos,arr)==True:
        return(newPos.astype(int))
    else: return(pos)

def checkifPosonGrid(pos,arr):
    bounds = [len(arr),len(arr[0])]
    if pos[0]> bounds[0]: return(False)
    if pos[1]> bounds[1]: return(False)
    if pos[0]< 0 or pos[1]<0: return(False)
    return(True)

def perturbImage(image,arr,delta):
    oldPos = image.pos
    newPos = perturbPos(oldPos,delta,arr)
    image.pos = newPos
    image.pot = get_potential(image.pos, arr)

def sumEnergy(initPath):
    sum=0
    for i in initPath:
        sum = sum -i.pot + i.springLeft + i.springRight
    return(sum)

slope,const = make_line(initial,final)
points,spacing = space_line(slope,const,initial,final,args.images)
initPath = init_path(points,arr)
delta,k,x0 = 20,10,3
calc_spring(initPath,x0, k)
print("Init Pathway: " + "\n")
for i in initPath: print(i.pos,i.pot,i.springLeft,i.springRight)
print("\n")

oldPath = copy.deepcopy(initPath)
for i in range(60000):
    newPath = copy.deepcopy(oldPath)
    indextoAlt = np.random.randint(1,len(initPath)-1)
    perturbImage(newPath[indextoAlt],arr, delta)
    calc_spring(newPath,x0,k)
    print(str(oldPath[indextoAlt].pos) + "--> " + str(newPath[indextoAlt].pos)
        + "  init: " + str(sumEnergy(oldPath))
        + "  final: " +  str(sumEnergy(newPath))
        + "  " + str(-float(sumEnergy(oldPath))+ float(sumEnergy(newPath))))
    if sumEnergy(oldPath)>sumEnergy(newPath):
        oldPath = copy.deepcopy(newPath)


print("\n"+"Final Pathway: "+"\n")

for i in newPath: print(i.pos,i.pot,i.springLeft,i.springRight)

print("\n")
for i in range(len(initPath)):
    print(initPath[i].pos,newPath[i].pos)

cmap3=sns.color_palette("ch:2.5,-.2,dark=.3")
fig, (figure)= plt.subplots(nrows=1, figsize=(8,5))
graph1 = sns.heatmap(-arr.transpose(),cmap=cmap3)
for i in newPath: plt.plot(i.pos[0],i.pos[1],marker=".",color="red")
plt.show()

f = open("path_" + str(args.initial) + "-->" + str(args.final)+".txt","w")
for value in newPath:
    f.write(str(value.pos[1])+","+str(value.pos[0]))
    f.write("\n")
