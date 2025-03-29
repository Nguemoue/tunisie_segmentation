"""
Script de génération de données de test.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def generate_test_data(n_samples=1000):
    """
    Génère des données de test pour la segmentation des clients.
    
    Args:
        n_samples (int): Nombre d'échantillons à générer
        
    Returns:
        pd.DataFrame: DataFrame contenant les données générées
    """
    # Création des données aléatoires
    np.random.seed(42)
    
    data = {
        'age': np.random.normal(35, 15, n_samples).astype(int),
        'revenu_mensuel': np.random.normal(2500, 1000, n_samples).astype(int),
        'consommation_mensuelle': np.random.normal(150, 50, n_samples).astype(int),
        'duree_contrat': np.random.normal(24, 12, n_samples).astype(int),
        'nombre_appels': np.random.poisson(50, n_samples),
        'nombre_sms': np.random.poisson(100, n_samples),
        'utilisation_data': np.random.normal(2, 1, n_samples).astype(float),
        'satisfaction': np.random.normal(7, 2, n_samples).astype(float),
        'fidelite': np.random.normal(3, 1, n_samples).astype(float)
    }
    
    # Création du DataFrame
    df = pd.DataFrame(data)
    
    # Ajustement des valeurs pour qu'elles soient réalistes
    df['age'] = df['age'].clip(18, 80)
    df['revenu_mensuel'] = df['revenu_mensuel'].clip(1000, 10000)
    df['consommation_mensuelle'] = df['consommation_mensuelle'].clip(50, 500)
    df['duree_contrat'] = df['duree_contrat'].clip(1, 60)
    df['nombre_appels'] = df['nombre_appels'].clip(0, 200)
    df['nombre_sms'] = df['nombre_sms'].clip(0, 500)
    df['utilisation_data'] = df['utilisation_data'].clip(0, 10)
    df['satisfaction'] = df['satisfaction'].clip(0, 10)
    df['fidelite'] = df['fidelite'].clip(0, 5)
    
    # Ajout d'un identifiant client
    df['client_id'] = range(1, n_samples + 1)
    
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