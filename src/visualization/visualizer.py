import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import os

# Ajout du répertoire parent au PYTHONPATH
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root))

from src.config import (
    NUMERIC_FEATURES,
    CLUSTERS_FILE,
    SEGMENT_LABELS,
    VISUALIZATIONS_DIR
)

class SegmentationVisualizer:
    """
    Classe pour la visualisation des résultats de la segmentation.
    """
    
    def __init__(self):
        self.features = NUMERIC_FEATURES
        self.output_dir = Path(VISUALIZATIONS_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration du style des graphiques
        plt.style.use('default')
        sns.set_theme(style="whitegrid")
    
    def load_data(self, input_file):
        """
        Charge les données segmentées depuis un fichier CSV.
        
        Args:
            input_file (str): Chemin du fichier d'entrée
            
        Returns:
            pd.DataFrame: DataFrame contenant les données segmentées
        """
        return pd.read_csv(input_file)
    
    def plot_cluster_distribution(self, df):
        """
        Crée un graphique de la distribution des segments.
        
        Args:
            df (pd.DataFrame): DataFrame contenant les données segmentées
        """
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x='segment_label')
        plt.title('Distribution des Segments')
        plt.xlabel('Segment')
        plt.ylabel('Nombre de Clients')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Sauvegarde du graphique
        output_file = self.output_dir / 'cluster_distribution.png'
        plt.savefig(output_file)
        plt.close()
        print(f"Distribution des segments sauvegardée dans {output_file}")
    
    def plot_feature_importance(self, df):
        """
        Crée un graphique de l'importance des caractéristiques par segment.
        
        Args:
            df (pd.DataFrame): DataFrame contenant les données segmentées
        """
        plt.figure(figsize=(12, 8))
        
        # Calcul des moyennes par segment
        segment_means = df.groupby('segment_label')[self.features].mean()
        
        # Création du heatmap
        sns.heatmap(segment_means, annot=True, cmap='YlOrRd', fmt='.2f')
        plt.title('Importance des Caractéristiques par Segment')
        plt.xlabel('Caractéristiques')
        plt.ylabel('Segment')
        plt.tight_layout()
        
        # Sauvegarde du graphique
        output_file = self.output_dir / 'feature_importance.png'
        plt.savefig(output_file)
        plt.close()
        print(f"Importance des caractéristiques sauvegardée dans {output_file}")
    
    def plot_segment_profiles(self, df):
        """
        Crée des graphiques des profils des segments.
        
        Args:
            df (pd.DataFrame): DataFrame contenant les données segmentées
        """
        n_features = len(self.features)
        n_cols = 3
        n_rows = (n_features + n_cols - 1) // n_cols
        
        plt.figure(figsize=(15, 5 * n_rows))
        
        for i, feature in enumerate(self.features, 1):
            plt.subplot(n_rows, n_cols, i)
            sns.boxplot(data=df, x='segment_label', y=feature)
            plt.title(f'Distribution de {feature} par Segment')
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Sauvegarde du graphique
        output_file = self.output_dir / 'segment_profiles.png'
        plt.savefig(output_file)
        plt.close()
        print(f"Profils des segments sauvegardés dans {output_file}")
    
    def plot_correlation_matrix(self, df):
        """
        Crée une matrice de corrélation des caractéristiques.
        
        Args:
            df (pd.DataFrame): DataFrame contenant les données segmentées
        """
        plt.figure(figsize=(10, 8))
        
        # Calcul de la matrice de corrélation
        corr_matrix = df[self.features].corr()
        
        # Création du heatmap
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Matrice de Corrélation des Caractéristiques')
        plt.tight_layout()
        
        # Sauvegarde du graphique
        output_file = self.output_dir / 'correlation_matrix.png'
        plt.savefig(output_file)
        plt.close()
        print(f"Matrice de corrélation sauvegardée dans {output_file}")
    
    def create_visualizations(self, input_file):
        """
        Crée toutes les visualisations.
        
        Args:
            input_file (str): Chemin du fichier d'entrée
        """
        # Chargement des données
        df = self.load_data(input_file)
        
        # Création des visualisations
        self.plot_cluster_distribution(df)
        self.plot_feature_importance(df)
        self.plot_segment_profiles(df)
        self.plot_correlation_matrix(df)

if __name__ == "__main__":
    # Création et utilisation du visualiseur
    visualizer = SegmentationVisualizer()
    visualizer.create_visualizations(CLUSTERS_FILE) 