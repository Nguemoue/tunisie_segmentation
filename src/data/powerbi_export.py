"""
Script d'export des données vers Power BI.
"""

import pandas as pd
from pathlib import Path
from database import DatabaseManager
import os

def export_to_powerbi():
    """Exporte les données vers le format Power BI."""
    # Création du dossier Power BI s'il n'existe pas
    powerbi_dir = Path('data/powerbi')
    powerbi_dir.mkdir(parents=True, exist_ok=True)
    
    # Connexion à la base de données
    db = DatabaseManager()
    
    try:
        # Export des données des clients
        clients_df = db.get_client_data()
        clients_df.to_csv(powerbi_dir / 'clients.csv', index=False)
        
        # Export des statistiques par segment
        segment_stats = db.get_segment_stats()
        segment_stats.to_csv(powerbi_dir / 'segment_stats.csv', index=False)
        
        # Export des offres commerciales
        offres_df = db.get_commercial_offers()
        offres_df.to_csv(powerbi_dir / 'offres_commerciales.csv', index=False)
        
        print("Données exportées avec succès vers Power BI")
        
    finally:
        db.close()

if __name__ == '__main__':
    export_to_powerbi() 