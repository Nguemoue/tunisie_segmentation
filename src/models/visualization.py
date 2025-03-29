"""
Module de visualisation pour le projet de segmentation Tunisie Telecom.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
from pathlib import Path
from sklearn.decomposition import PCA

from config import (
    FIGURES_PATH,
    COLOR_PALETTE,
    SEGMENT_LABELS
)

class SegmentationVisualizer:
    """Classe pour la visualisation des résultats de segmentation."""
    
    def __init__(self):
        """Initialise le visualiseur."""
        sns.set_theme(style='whitegrid')  # Utilisation du style Seaborn
        self.pca = PCA(n_components=2)
        self.columns_to_exclude = ['customer_id', 'date_abonnement']
        
    def _prepare_data(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Prépare les données pour la visualisation.
        
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
        
    def plot_cluster_distribution(self, labels: np.ndarray, save: bool = True) -> None:
        """
        Visualise la distribution des clusters.
        
        Parameters
        ----------
        labels : np.ndarray
            Labels des clusters
        save : bool, default=True
            Si True, sauvegarde la figure
        """
        plt.figure(figsize=(10, 6))
        
        # Calcul des proportions
        unique, counts = np.unique(labels, return_counts=True)
        proportions = counts / len(labels) * 100
        
        # Création du graphique
        bars = plt.bar(
            [SEGMENT_LABELS[i] for i in unique],
            proportions,
            color=COLOR_PALETTE
        )
        
        # Ajout des valeurs sur les barres
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{height:.1f}%',
                ha='center',
                va='bottom'
            )
        
        plt.title('Distribution des Segments Clients')
        plt.xlabel('Segment')
        plt.ylabel('Proportion (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save:
            Path(FIGURES_PATH).mkdir(parents=True, exist_ok=True)
            plt.savefig(Path(FIGURES_PATH) / 'cluster_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_cluster_centers(self, centers: pd.DataFrame, save: bool = True) -> None:
        """
        Visualise les centres des clusters.
        
        Parameters
        ----------
        centers : pd.DataFrame
            Centres des clusters
        save : bool, default=True
            Si True, sauvegarde la figure
        """
        plt.figure(figsize=(12, 6))
        
        # Création du heatmap
        sns.heatmap(
            centers,
            annot=True,
            fmt='.2f',
            cmap='YlOrRd',
            center=0
        )
        
        plt.title('Caractéristiques des Centres des Clusters')
        plt.xlabel('Features')
        plt.ylabel('Segment')
        plt.tight_layout()
        
        if save:
            Path(FIGURES_PATH).mkdir(parents=True, exist_ok=True)
            plt.savefig(Path(FIGURES_PATH) / 'cluster_centers.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_feature_importance(self, importance: Dict[int, pd.Series], save: bool = True) -> None:
        """
        Visualise l'importance des features par cluster.
        
        Parameters
        ----------
        importance : Dict[int, pd.Series]
            Importance des features par cluster
        save : bool, default=True
            Si True, sauvegarde la figure
        """
        n_clusters = len(importance)
        n_features = len(importance[0])
        
        plt.figure(figsize=(15, 5*n_clusters))
        
        for i, (cluster, imp) in enumerate(importance.items(), 1):
            plt.subplot(n_clusters, 1, i)
            
            # Création du graphique
            bars = plt.bar(
                imp.index,
                imp.values,
                color=COLOR_PALETTE[i % len(COLOR_PALETTE)]
            )
            
            plt.title(f'Importance des Features - {SEGMENT_LABELS[cluster]}')
            plt.xlabel('Features')
            plt.ylabel('Importance')
            plt.xticks(rotation=45)
            
        plt.tight_layout()
        
        if save:
            Path(FIGURES_PATH).mkdir(parents=True, exist_ok=True)
            plt.savefig(Path(FIGURES_PATH) / 'feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_cluster_profiles(self, profiles: Dict[int, Dict], save: bool = True) -> None:
        """
        Visualise les profils des clusters.
        
        Parameters
        ----------
        profiles : Dict[int, Dict]
            Profils des clusters
        save : bool, default=True
            Si True, sauvegarde la figure
        """
        n_clusters = len(profiles)
        
        plt.figure(figsize=(15, 5*n_clusters))
        
        for i, (cluster, profile) in enumerate(profiles.items(), 1):
            plt.subplot(n_clusters, 1, i)
            
            # Création du graphique
            means = list(profile['mean_values'].values())
            stds = list(profile['std_values'].values())
            features = list(profile['mean_values'].keys())
            
            bars = plt.bar(
                features,
                means,
                yerr=stds,
                color=COLOR_PALETTE[i % len(COLOR_PALETTE)]
            )
            
            plt.title(f'Profil du {SEGMENT_LABELS[cluster]}')
            plt.xlabel('Features')
            plt.ylabel('Valeur')
            plt.xticks(rotation=45)
            
        plt.tight_layout()
        
        if save:
            Path(FIGURES_PATH).mkdir(parents=True, exist_ok=True)
            plt.savefig(Path(FIGURES_PATH) / 'cluster_profiles.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_clustering_results(self, X: pd.DataFrame, labels: np.ndarray, save: bool = True) -> None:
        """
        Visualise les résultats du clustering en 2D.
        
        Parameters
        ----------
        X : pd.DataFrame
            Données originales
        labels : np.ndarray
            Labels des clusters
        save : bool, default=True
            Si True, sauvegarde la figure
        """
        # Préparation des données
        X_clean = self._prepare_data(X)
        
        # Réduction de dimensionnalité
        X_pca = self.pca.fit_transform(X_clean)
        
        plt.figure(figsize=(10, 8))
        
        # Création du scatter plot
        scatter = plt.scatter(
            X_pca[:, 0],
            X_pca[:, 1],
            c=labels,
            cmap='viridis',
            alpha=0.6
        )
        
        # Ajout des centres des clusters
        centers_pca = self.pca.transform(X_clean.groupby(labels).mean())
        plt.scatter(
            centers_pca[:, 0],
            centers_pca[:, 1],
            c='red',
            marker='x',
            s=200,
            linewidths=3,
            label='Centres'
        )
        
        plt.title('Visualisation des Clusters (PCA)')
        plt.xlabel('Première Composante Principale')
        plt.ylabel('Deuxième Composante Principale')
        plt.legend()
        plt.tight_layout()
        
        if save:
            Path(FIGURES_PATH).mkdir(parents=True, exist_ok=True)
            plt.savefig(Path(FIGURES_PATH) / 'clustering_results.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_commercial_offers(self, offers: Dict[int, Dict], save: bool = True) -> None:
        """
        Visualise les offres commerciales par segment.
        
        Parameters
        ----------
        offers : Dict[int, Dict]
            Offres commerciales par segment
        save : bool, default=True
            Si True, sauvegarde la figure
        """
        plt.figure(figsize=(12, 6))
        
        # Préparation des données
        segments = []
        reductions = []
        services = []
        
        for cluster, offer in offers.items():
            segments.append(SEGMENT_LABELS[cluster])
            reductions.append(offer['reduction'] * 100)
            services.append(len(offer['services_additionnels']))
            
        # Création du graphique
        x = np.arange(len(segments))
        width = 0.35
        
        plt.bar(x - width/2, reductions, width, label='Réduction (%)', color=COLOR_PALETTE[0])
        plt.bar(x + width/2, services, width, label='Services Additionnels', color=COLOR_PALETTE[1])
        
        plt.title('Offres Commerciales par Segment')
        plt.xlabel('Segment')
        plt.ylabel('Nombre')
        plt.xticks(x, segments, rotation=45)
        plt.legend()
        plt.tight_layout()
        
        if save:
            Path(FIGURES_PATH).mkdir(parents=True, exist_ok=True)
            plt.savefig(Path(FIGURES_PATH) / 'commercial_offers.png', dpi=300, bbox_inches='tight')
        plt.close() 