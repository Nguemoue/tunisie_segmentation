"""
Script pour générer des données d'exemple pour le projet de segmentation Tunisie Telecom.
"""

import logging
from pathlib import Path
from src.data.data_generator import DataGenerator
from config import RAW_DATA_PATH

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_generation.log'),
        logging.StreamHandler()
    ]
)

def main():
    """Fonction principale pour générer les données."""
    try:
        # Création du dossier de données brutes s'il n'existe pas
        Path(RAW_DATA_PATH).mkdir(parents=True, exist_ok=True)
        
        # Initialisation du générateur de données
        generator = DataGenerator(n_samples=1000, random_state=42)
        
        # Génération et sauvegarde des données
        logging.info("Génération des données d'exemple...")
        df = generator.generate_and_save('donnees_clients.csv')
        
        # Affichage des statistiques
        logging.info("\nStatistiques des données générées :")
        logging.info(f"Nombre total de clients : {len(df)}")
        logging.info("\nDistribution des types de clients :")
        logging.info(df['type_client'].value_counts(normalize=True))
        logging.info("\nDistribution des types d'abonnement :")
        logging.info(df['type_abonnement'].value_counts(normalize=True))
        logging.info("\nStatistiques des variables numériques :")
        logging.info(df.describe())
        
        logging.info("\nGénération des données terminée avec succès !")
        
    except Exception as e:
        logging.error(f"Erreur lors de la génération des données : {str(e)}")
        raise

if __name__ == "__main__":
    main() 