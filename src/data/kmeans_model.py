import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib.pyplot as plt
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import RANDOM_STATE, N_CLUSTERS_RANGE, FIGURES_PATH

def find_optimal_clusters(X, n_clusters_range=N_CLUSTERS_RANGE, random_state=RANDOM_STATE):
    """
    Find the optimal number of clusters using the Elbow method and Silhouette score.
    
    Parameters:
    -----------
    X : numpy.ndarray
        Feature matrix
    n_clusters_range : range
        Range of cluster numbers to try
    random_state : int
        Random seed for reproducibility
        
    Returns:
    --------
    tuple
        (optimal_k, results_dict)
    """
    results = {
        'n_clusters': list(n_clusters_range),
        'inertia': [],
        'silhouette': []
    }
    
    for k in n_clusters_range:
        # Train K-means model
        kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        kmeans.fit(X)
        
        # Get inertia
        results['inertia'].append(kmeans.inertia_)
        
        # Get silhouette score (for k > 1)
        if k > 1:
            labels = kmeans.labels_
            silhouette = silhouette_score(X, labels)
            results['silhouette'].append(silhouette)
        else:
            results['silhouette'].append(0)
    
    # Find optimal k using silhouette score
    optimal_k_silhouette = results['n_clusters'][np.argmax(results['silhouette'])]
    
    # Create elbow method plot
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(results['n_clusters'], results['inertia'], 'bo-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method')
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(results['n_clusters'], results['silhouette'], 'ro-')
    plt.axvline(x=optimal_k_silhouette, color='green', linestyle='--')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    plt.title(f'Silhouette Score (Optimal k = {optimal_k_silhouette})')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_PATH, 'optimal_clusters.png'))
    plt.close()
    
    return optimal_k_silhouette, results

def train_kmeans(X, n_clusters, random_state=RANDOM_STATE):
    """
    Train a K-means model.
    
    Parameters:
    -----------
    X : numpy.ndarray
        Feature matrix
    n_clusters : int
        Number of clusters
    random_state : int
        Random seed for reproducibility
        
    Returns:
    --------
    tuple
        (kmeans_model, cluster_labels, metrics)
    """
    # Train K-means model
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    cluster_labels = kmeans.fit_predict(X)
    
    # Calculate metrics
    metrics = {}
    metrics['inertia'] = kmeans.inertia_
    
    if n_clusters > 1:
        metrics['silhouette'] = silhouette_score(X, cluster_labels)
        metrics['davies_bouldin'] = davies_bouldin_score(X, cluster_labels)
    
    return kmeans, cluster_labels, metrics