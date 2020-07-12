from sklearn.cluster import AgglomerativeClustering
import numpy as np

def clustering(matrix, n_clusters):
    adj_matrix = np.array(matrix)

    # Cluster the points specified by the given distance matrix
    # into 4 clusters
    clustering = AgglomerativeClustering(affinity="precomputed", linkage="complete", n_clusters=n_clusters).fit_predict(matrix)

    clusters = [[] for i in range(n_clusters)]
    for i, label in enumerate(clustering):
        clusters[label].append(i)

    return clusters

