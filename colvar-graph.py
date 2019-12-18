import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

parser=argparse.ArgumentParser()
parser.add_argument("-colvar","--colvar",help="grid file to graph")
args=parser.parse_args()

CV1,CV2=[],[]
f = open(args.colvar)
for row in f.readlines()[3:]:
    CV1.append(float(row.split()[1]))
    CV2.append(float(row.split()[2]))

graph = sns.scatterplot(x=CV2,y=CV1,marker="+")
graph.set(ylim=(-3.2,3.2))
graph.set(xlim=(0,5.5))
plt.show()
