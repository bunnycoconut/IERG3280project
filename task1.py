import snap
import random
import sys
from datetime import datetime
from queue import Queue 
import matplotlib.pyplot as plt

initialadopters = 10
adopters_arr = [1,10,30,50,70,100]

def cascade(G,threshold,num_init_adopters,random_seed):
    q = Queue(maxsize = 0) 
    init_adopters = []
    count_nodes = 0
    for i in G.Nodes():
        count_nodes+=1
    node_is_B = [False] * count_nodes
    Rnd = snap.TRnd(random_seed)
    for i in range(0,num_init_adopters):
        nodeId = G.GetRndNId(Rnd)
        init_adopters.append(nodeId)
        node_is_B[nodeId] = True
    for NId in init_adopters:
        node = G.GetNI(NId)
        for node_fd_Id in node.GetOutEdges():
            if not node_is_B[node_fd_Id]:
                q.put((node_fd_Id,1))
    process_num=0
    while q.empty() is False:
        NId, num_ita = q.get()
        if node_is_B[NId]:
            continue
        node = G.GetNI(NId)
        neigh_total=0
        neigh_B=0
        for node_fd_Id in node.GetOutEdges():
            if node_fd_Id == NId:
                continue
            neigh_total+=1
            if node_is_B[node_fd_Id]:
                neigh_B+=1
        if neigh_B/neigh_total >= threshold:
            node_is_B[NId] = True
            for node_fd_Id in node.GetOutEdges():
                if not node_is_B[node_fd_Id]:
                    q.put((node_fd_Id,num_ita+1))
    count_B = 0
    for is_B in node_is_B:
        if is_B:
            count_B+=1
    return (count_B-num_init_adopters)*100/(count_nodes-num_init_adopters)


LoadedGraph = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1)
snap.DelSelfEdges(LoadedGraph)
seed_arr = []
random.seed(datetime.now())
for i in range(initialadopters):
    seed_arr.append(int(10000*random.random()))
plt.title("Payoff(Threshold) vs Cascading")
plt.ylabel('Cascading')
plt.xlabel('Payoff')
f=open("task1result.txt","w+")

for num_init_adopters in adopters_arr:
    print("Initial adopters No.= "+str(num_init_adopters))
    print("For each payoff value, there are "+str(initialadopters)+" sets of initial adopters")
    cascade_percent_arr = []
    threshold_arr = []
    for threshold in reversed(range(99)):
        if threshold > 20 and ((threshold+1)%5)!=0:
            continue
        threshold = (threshold+1)/100
        cascade_percent = 0
        for seed_index in range(len(seed_arr)):
            cascade_percent += cascade(LoadedGraph,threshold,num_init_adopters,seed_arr[seed_index])
        cascade_percent = cascade_percent/len(seed_arr)
        cascade_percent_arr.append(cascade_percent)
        threshold_arr.append(threshold)
        print("Payoff= "+str(threshold)+" Cascade Percentage= "+str(cascade_percent))
        if cascade_percent==100:
            break
    plt.plot(threshold_arr, cascade_percent_arr, label = str(num_init_adopters))
    try:
        f.write("number of initial adopters: "+str(num_init_adopters)+"\n")
        f.write("For each payoff value, there are "+str(initialadopters)+" sets of initial adopters\n")
        for i in range(len(threshold_arr)):
            f.write("Payoff= "+str(threshold_arr[i])+" Cascade Percentage= "+str(cascade_percent_arr[i])+"\n")
    except:
        print("Cant open")
plt.legend(title="Number of initial adopters")
plt.savefig('task1result.png')
plt.show()