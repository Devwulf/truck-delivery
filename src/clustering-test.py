from sklearn.cluster import AgglomerativeClustering
from matplotlib.pylab import show, axis
import networkx as nx
import csv
import numpy as np
from src.data import Data

matrix = Data(True).get_locations_matrix()

# Convert the matrix to a numpy array to be able to work with
# the clustering method below
adj_matrix = np.array(matrix)

# Cluster the points specified by the given distance matrix
# into 4 clusters
n_clusters = 4
clustering = AgglomerativeClustering(affinity="precomputed", linkage="complete", n_clusters=n_clusters).fit(matrix)

clusters = [[] for i in range(n_clusters)]
for i, label in enumerate(clustering.labels_):
    clusters[label].append(i)

# Everything below is for plotting the clustered points
# into a visual graph, and can thus be removed
graph = nx.Graph(adj_matrix)

# map node to cluster id for colors
cluster_map = {node: i for i, cluster in enumerate(clusters) for node in cluster}
colors = [cluster_map[i] for i in range(len(graph.nodes()))]

pos = nx.circular_layout(graph)

angs = np.linspace(0, 2*np.pi, 1+len(clusters))
repos = []
rad = 3.5 # radius of circle
for ea in angs:
    if ea > 0:
        repos.append(np.array([rad*np.cos(ea), rad*np.sin(ea)]))
for ea in pos.keys():
    posx = 0
    for i in range(n_clusters):
        if ea in clusters[i]:
            posx = i
            break

    pos[ea] += repos[posx]

# draw
nx.draw_networkx(graph, pos=pos, node_color=colors, edge_color="silver")
axis("off")
show(block=False)