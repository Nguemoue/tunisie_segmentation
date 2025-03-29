"""
Script principal pour le projet de segmentation Tunisie Telecom.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Optional
import logging
from datetime import datetime

from src.data.data_loader import DataLoader
from src.models.segmentation import CustomerSegmentation
from src.models.visualization import SegmentationVisualizer
from src.models.reporting import SegmentationReporter

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/segmentation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

def main():
    """Fonction principale du script."""
    try:
        # Initialisation des composants
        data_loader = DataLoader()
        segmentation = CustomerSegmentation()
        visualizer = SegmentationVisualizer()
        reporter = SegmentationReporter()
        
        # Chargement des données
        logging.info("Chargement des données...")
        raw_data = data_loader.load_raw_data('donnees_clients.csv')
        
        # Prétraitement des données
        logging.info("Prétraitement des données...")
        processed_data = data_loader.preprocess_data(raw_data)
        
        # Sauvegarde des données prétraitées
        data_loader.save_processed_data(processed_data, 'donnees_pretraitees.csv')
        
        # Segmentation des clients
        logging.info("Application de la segmentation...")
        segmentation.fit(processed_data)
        
        # Évaluation de la segmentation
        logging.info("Évaluation de la segmentation...")
        scores = segmentation.evaluate_clustering(processed_data)
        logging.info(f"Scores d'évaluation : {scores}")
        
        # Génération des profils
        logging.info("Génération des profils des segments...")
        profiles = segmentation.get_cluster_profiles(processed_data)
        
        # Génération des offres commerciales
        logging.info("Génération des offres commerciales...")
        offers = segmentation.get_commercial_offers()
        
        # Visualisations
        logging.info("Génération des visualisations...")
        visualizer.plot_cluster_distribution(segmentation.labels)
        visualizer.plot_cluster_centers(segmentation.get_cluster_centers())
        visualizer.plot_feature_importance(segmentation.feature_importance)
        visualizer.plot_cluster_profiles(profiles)
        visualizer.plot_clustering_results(processed_data, segmentation.labels)
        visualizer.plot_commercial_offers(offers)
        
        # Génération des rapports
        logging.info("Génération des rapports...")
        reporter.generate_segment_report(profiles)
        reporter.generate_executive_summary(profiles)
        reporter.generate_marketing_strategy(profiles)
        
        logging.info("Processus de segmentation terminé avec succès!")
        
    except Exception as e:
        logging.error(f"Erreur lors du processus de segmentation : {str(e)}")
        raise

if __name__ == "__main__":
    main()