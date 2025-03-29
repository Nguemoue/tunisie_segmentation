"""
Script principal pour l'analyse et la segmentation des clients.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from pathlib import Path
import logging
from database import DatabaseManager
from powerbi_export import export_to_powerbi

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('segmentation.log'),
        logging.StreamHandler()
    ]
)

def preprocess_data(df):
    """Prétraite les données."""
    logging.info("Début du prétraitement des données")
    
    # Gestion des valeurs manquantes
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
    
    # Normalisation
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(
        scaler.fit_transform(df[numeric_columns]),
        columns=numeric_columns
    )
    
    logging.info("Prétraitement des données terminé")
    return df_scaled

def perform_segmentation(df):
    """Effectue la segmentation des clients."""
    logging.info("Début de la segmentation")
    
    # Application de K-Means
    n_clusters = 5
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['segment'] = kmeans.fit_predict(df)
    
    # Ajout des labels de segments
    segment_labels = {
        0: "Fidèles",
        1: "Nouveaux",
        2: "VIP",
        3: "Risque",
        4: "Inactifs"
    }
    df['segment'] = df['segment'].map(segment_labels)
    
    logging.info("Segmentation terminée")
    return df

def main():
    """Fonction principale."""
    try:
        # Création des dossiers nécessaires
        Path('data/raw').mkdir(parents=True, exist_ok=True)
        Path('data/processed').mkdir(parents=True, exist_ok=True)
        
        # Chargement des données
        logging.info("Chargement des données")
        df = pd.read_csv('data/raw/donnees_clients.csv')
        
        # Prétraitement
        df_scaled = preprocess_data(df)
        
        # Segmentation
        df_segmented = perform_segmentation(df_scaled)
        
        # Sauvegarde des données prétraitées
        df_segmented.to_csv('data/processed/donnees_pretraitees.csv', index=False)
        logging.info("Données prétraitées sauvegardées")
        
        # Import dans la base de données
        db = DatabaseManager()
        db.import_data('data/processed/donnees_pretraitees.csv')
        
        # Ajout des offres commerciales
        offres = {
            "Fidèles": ("Offre Premium", "Offre spéciale pour clients fidèles", 49.99),
            "Nouveaux": ("Offre Découverte", "Offre d'initiation", 29.99),
            "VIP": ("Offre VIP", "Offre exclusive pour clients VIP", 79.99),
            "Risque": ("Offre Standard", "Offre de base", 19.99),
            "Inactifs": ("Offre Relance", "Offre pour réactiver les clients", 24.99)
        }
        
        for segment, (nom, desc, prix) in offres.items():
            db.add_commercial_offer(segment, nom, desc, prix)
        
        # Export vers Power BI
        export_to_powerbi()
        
        logging.info("Processus terminé avec succès")
        
    except Exception as e:
        logging.error(f"Erreur lors de l'exécution : {str(e)}")
        raise

if __name__ == '__main__':
    main() 