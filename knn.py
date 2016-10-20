import networkx as nx
import numpy as np
from scipy.spatial import distance

dolphins_grap = nx.read_gml("..\data\dolphins.gml")
#print nx.info(dolphins_grap)

d_matr = nx.to_numpy_matrix(dolphins_grap, nodelist=range(62))
G = d_matr + np.eye(d_matr.shape[1])


size=62

#Compute Similarity using euclicdean
S = np.eye(size)
for i in range(size):
    for j in range(size):
        similar = distance.euclidean(G[i],G[j])
        S[i][j] = similar

def predict_knn(G, S, k):
    size = S.shape[1]
    P = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if i != j and G.item(i, j) != 1.0:
                # find top k similar of d_j and compute predict
                d_j = S[:][j]
                index = d_j.argsort()[-k:][::-1]
                top_d_j = d_j[d_j.argsort()[-k:][::-1]]
                # print top_d_j
                # print index
                Connect = G[:][i].T
                P[i][j] = top_d_j * Connect[index] / sum(top_d_j)
            else:
                P[i][j] = -1
    return P
Predict = predict_knn(G, S, 5)
#print Predict
for i in range(62):
    pr = Predict[:][i]
    index = pr.argsort()[-3:][::-1]
    top_node_pr = pr[pr.argsort()[-3:][::-1]]
    #print "Node %d <---> Node %d " %(i, index[0])
    print "%s <---> %s" % (dolphins_grap.node[i]['label'], dolphins_grap.node[index[0]]['label'])
    #print top_node_pr
