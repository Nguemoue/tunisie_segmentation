"""
Module de segmentation des clients Tunisie Telecom.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import sys
import os

# Ajout du répertoire parent au PYTHONPATH
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root))

from src.config import (
    CLUSTERING_PARAMS,
    SEGMENT_LABELS,
    COMMERCIAL_OFFERS,
    NUMERIC_FEATURES,
    PROCESSED_DATA_FILE,
    CLUSTERS_FILE,
    N_CLUSTERS,
    RANDOM_STATE
)

class CustomerSegmentation:
    """
    Classe pour la segmentation des clients.
    """
    
    def __init__(self):
        self.model = KMeans(
            n_clusters=CLUSTERING_PARAMS['kmeans']['n_clusters'],
            random_state=CLUSTERING_PARAMS['kmeans']['random_state'],
            n_init=CLUSTERING_PARAMS['kmeans']['n_init']
        )
        self.features = NUMERIC_FEATURES
    
    def load_data(self, input_file):
        """
        Charge les données prétraitées depuis un fichier CSV.
        
        Args:
            input_file (str): Chemin du fichier d'entrée
            
        Returns:
            pd.DataFrame: DataFrame contenant les données prétraitées
        """
        return pd.read_csv(input_file)
    
    def fit(self, X):
        """
        Entraîne le modèle de segmentation.
        
        Args:
            X (pd.DataFrame): Données d'entrée
            
        Returns:
            self: Instance de la classe
        """
        self.model.fit(X[self.features])
        return self
    
    def predict(self, X):
        """
        Prédit les segments pour de nouvelles données.
        
        Args:
            X (pd.DataFrame): Données d'entrée
            
        Returns:
            np.array: Labels des segments prédits
        """
        return self.model.predict(X[self.features])
    
    def evaluate(self, X):
        """
        Évalue la qualité de la segmentation.
        
        Args:
            X (pd.DataFrame): Données d'entrée
            
        Returns:
            dict: Métriques d'évaluation
        """
        labels = self.model.labels_
        silhouette = silhouette_score(X[self.features], labels)
        
        metrics = {
            "silhouette_score": silhouette,
            "inertia": self.model.inertia_
        }
        
        return metrics
    
    def get_cluster_profiles(self, X):
        """
        Calcule les profils des segments.
        
        Args:
            X (pd.DataFrame): Données d'entrée
            
        Returns:
            pd.DataFrame: Profils des segments
        """
        X_with_clusters = X.copy()
        X_with_clusters['cluster'] = self.model.labels_
        
        profiles = []
        for cluster in range(CLUSTERING_PARAMS['kmeans']['n_clusters']):
            cluster_data = X_with_clusters[X_with_clusters['cluster'] == cluster]
            profile = cluster_data[self.features].mean()
            profile['size'] = len(cluster_data)
            profile['percentage'] = len(cluster_data) / len(X) * 100
            profiles.append(profile)
        
        cluster_profiles = pd.DataFrame(profiles)
        cluster_profiles.index = [SEGMENT_LABELS[i] for i in range(CLUSTERING_PARAMS['kmeans']['n_clusters'])]
        
        return cluster_profiles
    
    def segment_clients(self, input_file, output_file):
        """
        Effectue la segmentation complète des clients.
        
        Args:
            input_file (str): Chemin du fichier d'entrée
            output_file (str): Chemin du fichier de sortie
        """
        # Chargement des données
        df = self.load_data(input_file)
        
        # Entraînement du modèle
        self.fit(df)
        
        # Prédiction des segments
        df['segment'] = self.predict(df)
        df['segment_label'] = df['segment'].map(SEGMENT_LABELS)
        
        # Évaluation du modèle
        metrics = self.evaluate(df)
        print("\nMétriques d'évaluation :")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")
        
        # Calcul des profils des segments
        profiles = self.get_cluster_profiles(df)
        print("\nProfils des segments :")
        print(profiles)
        
        # Création du dossier de sortie s'il n'existe pas
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarde des résultats
        df.to_csv(output_file, index=False)
        print(f"\nRésultats de la segmentation sauvegardés dans {output_file}")
        
        return df, profiles, metrics

if __name__ == "__main__":
    # Création et utilisation du segmenteur
    segmenter = CustomerSegmentation()
    df_segmented, profiles, metrics = segmenter.segment_clients(
        PROCESSED_DATA_FILE,
        CLUSTERS_FILE
    ) 