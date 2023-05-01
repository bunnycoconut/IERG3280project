import snap
import random
import sys
from datetime import datetime
from queue import Queue 
import matplotlib.pyplot as plt


LoadedGraph = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1)
snap.DelSelfEdges(LoadedGraph)
snap.PrintInfo(LoadedGraph,"Result","data.txt",False)

edge_arr=[]
for NI in LoadedGraph.Nodes():
    count=0
    for Id in NI.GetOutEdges():
        count+=1
    edge_arr.append(count)
plt.title("Distribution of Number of edges")
plt.ylabel('Number of edges')
plt.xlabel('Node ID')
plt.plot(edge_arr)
plt.savefig('dataanalysis1.png')
plt.show()

edge_arr.sort()
mini = str(edge_arr[0])
max = str(edge_arr[len(edge_arr)-1])
avg = str(sum(edge_arr)/len(edge_arr))
median = str(edge_arr[int(len(edge_arr)/2)])
num_nodes_with_edge_arr = [0] * (int(max)+1)
for i in edge_arr:
    num_nodes_with_edge_arr[i]+=1
plt.title("Number of nodes vs edge")
plt.ylabel('Number of nodes')
plt.xlabel('Edge')
plt.plot(num_nodes_with_edge_arr)
plt.savefig('dataanalysis2.png')
plt.show()
print("Maximum= "+max)
print("Minimum= "+mini)
print("Median= "+median)
print("Average= "+avg)
f=open("dataanalysis.txt","w+")
f.write("Maximum= "+max+"\n")
f.write("Minimum= "+mini+"\n")
f.write("Median= "+median+"\n")
f.write("Average= "+avg+"\n")
for i in range(len(num_nodes_with_edge_arr)):
    f.write(str(num_nodes_with_edge_arr[i])+" nodes have "+str(i)+" edges\n")