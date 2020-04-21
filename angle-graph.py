import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as ticker
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FormatStrFormatter
import plotly 
import plotly.graph_objects as go
import plotly.io as pio
parser=argparse.ArgumentParser()
parser.add_argument("-angle","--angle",help="grid file to graph")
parser.add_argument("-name","--name",help="title of plot")


args=parser.parse_args()

data = []
f = open(args.angle)
for line in f.readlines():
	if not line.startswith('#'):
		line=line.split(' ')
		data.append([float(line[1])*.2,float(line[2]),float(line[3]),float(line[4])])

data = pd.DataFrame(data)
data.columns = ['time','angle1','angle2','angle3']
graph1  = go.Figure()

graph1.add_trace(go.Box(x=data['angle1'],boxpoints='all',jitter=0.3,name='$\epsilon$'))
graph1.add_trace(go.Box(x=data['angle2'],boxpoints='all',jitter=0.3,name='$\omega$'))
graph1.add_trace(go.Box(x=data['angle3'],boxpoints='all',jitter=0.3,name='$\psi$'))
graph1.update_layout(xaxis_title="rad",height=700,width=1200,font=dict(size=15),showlegend=False)
pio.write_image(graph1,args.name+".png") 
"""
fig, graph1 = plt.subplots() 
for line in data:
	plt.plot(1,line[1],marker='.',color='black')
	plt.plot(2,line[2],marker='.', color='red')
	plt.plot(3,line[],marker='.', color='blue')

plt.show()"""