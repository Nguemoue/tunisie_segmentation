"""
Script de génération de données de test.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def generate_test_data(n_samples=1000):
    """Génère des données de test pour la segmentation."""
    
    # Création des données aléatoires
    np.random.seed(42)
    
    data = {
        'age': np.random.normal(35, 10, n_samples).astype(int),
        'montant_consommation': np.random.lognormal(3, 0.5, n_samples),
        'nombre_appels': np.random.poisson(50, n_samples),
        'volume_data': np.random.lognormal(2, 0.3, n_samples),
        'nombre_sms': np.random.poisson(30, n_samples)
    }
    
    # Création du DataFrame
    df = pd.DataFrame(data)
    
    # Ajustement des valeurs négatives
    df['age'] = df['age'].clip(18, 80)
    df['montant_consommation'] = df['montant_consommation'].clip(0)
    df['nombre_appels'] = df['nombre_appels'].clip(0)
    df['volume_data'] = df['volume_data'].clip(0)
    df['nombre_sms'] = df['nombre_sms'].clip(0)
    
    # Arrondissement des valeurs
    df['montant_consommation'] = df['montant_consommation'].round(2)
    df['volume_data'] = df['volume_data'].round(2)
    
    return df

def main():
    """Fonction principale."""
    # Création du dossier data/raw s'il n'existe pas
    Path('data/raw').mkdir(parents=True, exist_ok=True)
    
    # Génération des données
    df = generate_test_data()
    
    # Sauvegarde des données
    df.to_csv('data/raw/donnees_clients.csv', index=False)
    print("Données de test générées avec succès dans data/raw/donnees_clients.csv")
    
    # Affichage des statistiques
    print("\nStatistiques des données générées :")
    print(df.describe())

if __name__ == '__main__':
    main() 