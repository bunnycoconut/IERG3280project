import snap
import random
import sys
from datetime import datetime
from queue import Queue 
import matplotlib.pyplot as plt
from operator import itemgetter, attrgetter

adopters_arr = [10]


def cascade_with_init_adopters(G,threshold,init_adopters,f):
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
    next_threshold=0
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
    cascade_percent = (count_B-len(init_adopters))*100/(count_nodes-len(init_adopters))
    node_is_B_count=0
    for i in range(count_nodes):
        if node_is_B[i]:
            node_is_B_count+=1
    print("Current payoff= "+str(threshold)+"   Current cascade= "+str(cascade_percent))
    print(str(node_is_B_count)+" Nodes adopted B")
    f.write("Current payoff: "+str(threshold)+"   Current cascade= "+str(cascade_percent)+"\n")
    f.write(str(node_is_B_count)+" Nodes adopted B\n")

    clusters=[]
    clusters_id=0
    for i in range(count_nodes):
        if node_is_B[i]:
            continue
        in_clusters=False
        for cluster in clusters:
            if i in cluster:
                in_clusters=True
                break
        if not in_clusters:
            cluster_ids=[]
            cluster_q = Queue(maxsize = 0) 
            cluster_ids.append(i)
            cluster_q.put(i)
            while cluster_q.empty() is False:       
                node_Id = cluster_q.get()
                for Id in G.GetNI(node_Id).GetOutEdges():
                    if not node_is_B[Id] and Id not in cluster_ids:
                        if have_common_friends(G,node_Id,Id,node_is_B):
                            cluster_ids.append(Id)
                            cluster_q.put(Id)
            cluster_density = 1
            for cluster_node_id in cluster_ids:
                neigh_total = 0
                neigh_same_cluster = 0
                for cluster_node_fd_id in G.GetNI(cluster_node_id).GetOutEdges():
                    neigh_total+=1
                    if cluster_node_fd_id in cluster_ids:
                        neigh_same_cluster+=1
                if neigh_same_cluster/neigh_total < cluster_density:
                    cluster_density = neigh_same_cluster/neigh_total
            if len(cluster_ids) >1:
                print("Cluster "+str(clusters_id)+" contains "+str(len(cluster_ids))+" nodes")
                print("Cluster "+str(clusters_id)+"'s density= "+str(cluster_density))
                f.write("Cluster contains= "+str(len(cluster_ids))+" nodes\n")
                f.write("Cluster density= "+str(cluster_density)+"\n")
                
            clusters.append(cluster_ids)
            clusters_id+=1
    f.write("Nodes adopted B: \n")
    for i in range(count_nodes):
        if node_is_B[i]:
           f.write(str(i)+" ")      
    for i in range(len(clusters)):
        f.write("Cluster "+str(i)+"\n")
        f.write(str(clusters[i])+"\n")
    return 

def have_common_friends(G,a,b,node_is_B):
    friends_a = []
    for Id in G.GetNI(a).GetOutEdges():
        if Id != a and Id != b and not node_is_B[Id]:
            friends_a.append(Id)
    for Id in G.GetNI(b).GetOutEdges():
        if Id in friends_a:
            return True
    return False


LoadedGraph = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt", 0, 1)
snap.DelSelfEdges(LoadedGraph)


random.seed(datetime.now())
PRankH = snap.TIntFltH()
snap.GetPageRank(LoadedGraph,PRankH)
PRankH_arr=[]
for item in PRankH:
    PRankH_arr.append((item,PRankH[item]))
PRankH_arr.sort(key=itemgetter(1), reverse=True)
f=open("task3result.txt","w+")
for num_init_adopters in adopters_arr:
    key_nodes_Id=[]
    for i in range(num_init_adopters):
        random_number = random.randint(0,100)
        while PRankH_arr[random_number][0] in key_nodes_Id:
            random_number = random.randint(0,100)
        key_nodes_Id.append(PRankH_arr[random_number][0])
    print("Initial adopters No= "+str(num_init_adopters))
    cascade_with_init_adopters(LoadedGraph,0.4,key_nodes_Id,f)