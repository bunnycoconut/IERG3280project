import snap
import random
import sys
from datetime import datetime
from queue import Queue 
import matplotlib.pyplot as plt
from operator import itemgetter, attrgetter

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

def cascade_with_init_adopters(G,threshold,init_adopters):
    q = Queue(maxsize = 0) 
    count_nodes = 0
    for i in G.Nodes():
        count_nodes+=1
    node_is_B = [False] * count_nodes
    for NId in init_adopters:
        node_is_B[NId] = True
        node = G.GetNI(NId)
        for node_fd_Id in node.GetOutEdges():
            if not node_is_B[node_fd_Id]:
                q.put((node_fd_Id,1))
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
    return (count_B-len(init_adopters))*100/(count_nodes-len(init_adopters))
initialadopters = 10
adopters_arr = [1,50,100]
LoadedGraph = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1)
snap.DelSelfEdges(LoadedGraph)

plt.title("Payoff(Threshold) vs Cascading (Adopting Key Nodes)")
plt.ylabel('Cascading')
plt.xlabel('Payoff')
random.seed(datetime.now())
PRankH = snap.TIntFltH()
snap.GetPageRank(LoadedGraph,PRankH)
PRankH_arr=[]
for item in PRankH:
    PRankH_arr.append((item,PRankH[item]))
PRankH_arr.sort(key=itemgetter(1), reverse=True)
f=open("task2result.txt","w+")


for num_init_adopters in adopters_arr:
    print("Randomly choose key nodes from the 100 largest PRank nodes as initial adopters")
    print("Initial adopters No.= "+str(num_init_adopters))
    print("For each payoff value,there are "+str(initialadopters)+" sets of initial adopters")
    key_nodes_Id=[]
    for i in range(initialadopters):
        key_nodes_Id.append([])
        for j in range(num_init_adopters):
            random_number = random.randint(0,100)
            while PRankH_arr[random_number][0] in key_nodes_Id[i]:
                random_number = random.randint(0,100)
            key_nodes_Id[i].append(PRankH_arr[random_number][0])
    cascade_percent_arr = []
    threshold_arr = []
    for threshold in reversed(range(99)):
        if threshold > 20 and ((threshold+1)%5)!=0:
            continue
        threshold = (threshold+1)/100
        cascade_percent = 0
        for num_run_index in range(initialadopters):
            cascade_percent+=cascade_with_init_adopters(LoadedGraph,threshold,key_nodes_Id[num_run_index])
        cascade_percent = cascade_percent/initialadopters
        if cascade_percent != 0:
            cascade_percent_arr.append(cascade_percent)
            threshold_arr.append(threshold)
            print("Payoff= "+str(threshold)+" Cascade percentage= "+str(cascade_percent))
            if cascade_percent==100:
                break
        f.write("Randomly choose key nodes from the 100 largest PRank nodes as initial adopters\n")
        f.write("Initial adopters No.= "+str(num_init_adopters)+"\n")
        f.write("For each payoff,there are "+str(initialadopters)+" sets of initial adopters\n")
        for i in range(len(threshold_arr)):
            f.write("Payoff= "+str(threshold_arr[i])+" Cascade percentage= "+str(cascade_percent_arr[i])+"\n")
    plt.plot(threshold_arr,cascade_percent_arr,label="Initial adopters No.(Key Nodes)="+str(num_init_adopters))

seed_arr = []
for i in range(initialadopters):
    seed_arr.append(int(10000*random.random()))
for num_init_adopters in adopters_arr:
    print("Randomly choose nodes from all the nodes as initial adopters")
    print("Initial adopters No.= "+str(num_init_adopters))
    print("For each payoff value,there are "+str(initialadopters)+" sets of initial adopters")
    cascade_percent_arr = []
    threshold_arr = []
    for threshold in reversed(range(99)):
        if threshold > 20 and ((threshold+1)%5)!=0:
            continue
        threshold = (threshold+1)/100
        cascade_percent = 0
        for num_run_index in range(initialadopters):
            cascade_percent+=cascade(LoadedGraph,threshold,num_init_adopters,seed_arr[num_run_index])
        cascade_percent = cascade_percent/initialadopters
        cascade_percent_arr.append(cascade_percent)
        threshold_arr.append(threshold)
        print("Payoff= "+str(threshold)+" Cascade percentage= "+str(cascade_percent))
        if cascade_percent==100:
            break
        f.write("Randomly choose nodes from all the nodes as initial adopters\n")
        f.write("Initial adopters No.= "+str(num_init_adopters)+"\n")
        f.write("For each payoff value,there are "+str(initialadopters)+" sets of initial adopters\n")
        for i in range(len(threshold_arr)):
            f.write("Payoff= "+str(threshold_arr[i])+" Cascade percentage= "+str(cascade_percent_arr[i])+"\n")
    plt.plot(threshold_arr,cascade_percent_arr,label="Initial adopters No.(Normal Nodes)="+str(num_init_adopters))
plt.legend(title="Number of initial adopters")
plt.savefig('task2result.png')
plt.show()
