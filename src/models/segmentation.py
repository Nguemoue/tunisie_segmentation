"""
Module de segmentation des clients Tunisie Telecom.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from config import (
    CLUSTERING_PARAMS,
    SEGMENT_LABELS,
    COMMERCIAL_OFFERS
)

class CustomerSegmentation:
    """Classe pour la segmentation des clients."""
    
    def __init__(self, n_clusters: int = 5):
        """
        Initialise le modèle de segmentation.
        
        Parameters
        ----------
        n_clusters : int, default=5
            Nombre de clusters à créer
        """
        self.n_clusters = n_clusters
        self.kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=CLUSTERING_PARAMS['kmeans']['random_state'],
            n_init=CLUSTERING_PARAMS['kmeans']['n_init']
        )
        self.dbscan = DBSCAN(
            eps=CLUSTERING_PARAMS['dbscan']['eps'],
            min_samples=CLUSTERING_PARAMS['dbscan']['min_samples']
        )
        self.pca = PCA(n_components=2)
        self.scaler = StandardScaler()
        self.labels = None
        self.feature_importance = None
        self.feature_names = None
        self.columns_to_exclude = ['customer_id', 'date_abonnement']
        
    def _prepare_data(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Prépare les données pour la segmentation.
        
        Parameters
        ----------
        X : pd.DataFrame
            Données brutes
            
        Returns
        -------
        pd.DataFrame
            Données nettoyées
        """
        return X.drop(columns=[col for col in self.columns_to_exclude if col in X.columns])
        
    def fit(self, X: pd.DataFrame, method: str = 'kmeans') -> None:
        """
        Ajuste le modèle de segmentation.
        
        Parameters
        ----------
        X : pd.DataFrame
            Données à segmenter
        method : str, default='kmeans'
            Méthode de clustering à utiliser ('kmeans' ou 'dbscan')
        """
        # Préparation des données
        X_clean = self._prepare_data(X)
        
        # Sauvegarde des noms des features
        self.feature_names = X_clean.columns.tolist()
        
        # Normalisation des données
        X_scaled = self.scaler.fit_transform(X_clean)
        
        # Réduction de dimensionnalité pour visualisation
        X_pca = self.pca.fit_transform(X_scaled)
        
        # Application du clustering
        if method == 'kmeans':
            self.labels = self.kmeans.fit_predict(X_scaled)
        elif method == 'dbscan':
            self.labels = self.dbscan.fit_predict(X_scaled)
        else:
            raise ValueError("Méthode de clustering non supportée")
            
        # Calcul de l'importance des features
        self._compute_feature_importance(X_clean)
        
    def _compute_feature_importance(self, X: pd.DataFrame) -> None:
        """Calcule l'importance des features pour chaque cluster."""
        feature_importance = {}
        
        for cluster in range(self.n_clusters):
            cluster_data = X[self.labels == cluster]
            importance = cluster_data.std().sort_values(ascending=False)
            feature_importance[cluster] = importance
            
        self.feature_importance = feature_importance
        
    def evaluate_clustering(self, X: pd.DataFrame) -> Dict[str, float]:
        """
        Évalue la qualité du clustering.
        
        Parameters
        ----------
        X : pd.DataFrame
            Données utilisées pour le clustering
            
        Returns
        -------
        Dict[str, float]
            Scores d'évaluation
        """
        # Préparation des données
        X_clean = self._prepare_data(X)
        X_scaled = self.scaler.transform(X_clean)
        
        scores = {
            'silhouette': silhouette_score(X_scaled, self.labels),
            'calinski_harabasz': calinski_harabasz_score(X_scaled, self.labels),
            'davies_bouldin': davies_bouldin_score(X_scaled, self.labels)
        }
        
        return scores
        
    def get_cluster_profiles(self, X: pd.DataFrame) -> Dict[int, Dict]:
        """
        Génère les profils des clusters.
        
        Parameters
        ----------
        X : pd.DataFrame
            Données originales
            
        Returns
        -------
        Dict[int, Dict]
            Profils des clusters
        """
        # Préparation des données
        X_clean = self._prepare_data(X)
        profiles = {}
        
        for cluster in range(self.n_clusters):
            cluster_data = X_clean[self.labels == cluster]
            
            profile = {
                'size': len(cluster_data),
                'percentage': len(cluster_data) / len(X_clean) * 100,
                'mean_values': cluster_data.mean().to_dict(),
                'std_values': cluster_data.std().to_dict(),
                'key_features': self.feature_importance[cluster].head(3).to_dict()
            }
            
            profiles[cluster] = profile
            
        return profiles
        
    def get_commercial_offers(self) -> Dict[int, Dict]:
        """
        Génère les offres commerciales pour chaque segment.
        
        Returns
        -------
        Dict[int, Dict]
            Offres commerciales par segment
        """
        offers = {}
        
        for cluster in range(self.n_clusters):
            segment_name = SEGMENT_LABELS[cluster]
            offers[cluster] = COMMERCIAL_OFFERS[segment_name]
            
        return offers
        
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Prédit les segments pour de nouvelles données.
        
        Parameters
        ----------
        X : pd.DataFrame
            Nouvelles données
            
        Returns
        -------
        np.ndarray
            Labels des segments prédits
        """
        # Préparation des données
        X_clean = self._prepare_data(X)
        X_scaled = self.scaler.transform(X_clean)
        return self.kmeans.predict(X_scaled)
        
    def get_cluster_centers(self) -> pd.DataFrame:
        """
        Retourne les centres des clusters.
        
        Returns
        -------
        pd.DataFrame
            Centres des clusters
        """
        centers = self.kmeans.cluster_centers_
        centers = self.scaler.inverse_transform(centers)
        return pd.DataFrame(centers, columns=self.feature_names) 