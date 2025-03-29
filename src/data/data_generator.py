"""
Module de génération de données d'exemple pour le projet de segmentation Tunisie Telecom.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from config import RAW_DATA_PATH

class DataGenerator:
    """Classe pour générer des données d'exemple."""
    
    def __init__(self, n_samples: int = 1000, random_state: int = 42):
        """
        Initialise le générateur de données.
        
        Parameters
        ----------
        n_samples : int, default=1000
            Nombre d'échantillons à générer
        random_state : int, default=42
            Graine aléatoire pour la reproductibilité
        """
        self.n_samples = n_samples
        self.random_state = random_state
        np.random.seed(random_state)
        
    def generate_customer_data(self) -> pd.DataFrame:
        """
        Génère des données clients synthétiques.
        
        Returns
        -------
        pd.DataFrame
            Données clients générées
        """
        # Génération des identifiants clients
        customer_ids = [f'CUST_{i:05d}' for i in range(1, self.n_samples + 1)]
        
        # Génération des données démographiques
        data = {
            'customer_id': customer_ids,
            'age': np.random.normal(35, 12, self.n_samples),
            'sexe': np.random.choice(['M', 'F'], self.n_samples, p=[0.55, 0.45]),
            'zone_geographique': np.random.choice(
                ['Tunis', 'Sfax', 'Sousse', 'Bizerte', 'Autre'],
                self.n_samples,
                p=[0.3, 0.2, 0.15, 0.15, 0.2]
            ),
            'type_client': np.random.choice(
                ['Particulier', 'Entreprise'],
                self.n_samples,
                p=[0.8, 0.2]
            )
        }
        
        # Génération des données de consommation
        data.update({
            'montant_consommation': np.random.gamma(5, 10, self.n_samples),
            'nombre_appels': np.random.poisson(50, self.n_samples),
            'volume_data': np.random.gamma(3, 2, self.n_samples),
            'nombre_sms': np.random.poisson(20, self.n_samples)
        })
        
        # Génération des données d'abonnement
        data.update({
            'type_abonnement': np.random.choice(
                ['Prépayé', 'Postpayé', 'Hybride'],
                self.n_samples,
                p=[0.4, 0.5, 0.1]
            ),
            'duree_abonnement': np.random.gamma(20, 2, self.n_samples),
            'date_abonnement': [
                (datetime.now() - timedelta(days=np.random.randint(0, 365*3))).strftime('%Y-%m-%d')
                for _ in range(self.n_samples)
            ]
        })
        
        # Création du DataFrame
        df = pd.DataFrame(data)
        
        # Ajout de corrélations réalistes
        self._add_correlations(df)
        
        # Application de contraintes réalistes
        self._apply_constraints(df)
        
        # Ajout de valeurs manquantes
        self._add_missing_values(df)
        
        return df
        
    def _add_correlations(self, df: pd.DataFrame) -> None:
        """Ajoute des corrélations réalistes entre les variables."""
        # Corrélation entre type d'abonnement et montant de consommation
        df.loc[df['type_abonnement'] == 'Postpayé', 'montant_consommation'] *= 1.5
        df.loc[df['type_abonnement'] == 'Prépayé', 'montant_consommation'] *= 0.7
        
        # Corrélation entre type de client et volume de données
        df.loc[df['type_client'] == 'Entreprise', 'volume_data'] *= 2.0
        
        # Corrélation entre durée d'abonnement et nombre d'appels
        df['nombre_appels'] *= (1 + df['duree_abonnement'] / 100)
        
    def _apply_constraints(self, df: pd.DataFrame) -> None:
        """Applique des contraintes réalistes aux données."""
        # Contraintes sur l'âge
        df['age'] = np.clip(df['age'], 18, 90)
        
        # Contraintes sur les montants
        df['montant_consommation'] = np.clip(df['montant_consommation'], 0, 500)
        df['volume_data'] = np.clip(df['volume_data'], 0, 100)
        
        # Contraintes sur les durées
        df['duree_abonnement'] = np.clip(df['duree_abonnement'], 1, 60)
        
        # Contraintes sur les compteurs
        df['nombre_appels'] = np.clip(df['nombre_appels'], 0, 500)
        df['nombre_sms'] = np.clip(df['nombre_sms'], 0, 200)
        
    def _add_missing_values(self, df: pd.DataFrame) -> None:
        """Ajoute des valeurs manquantes de manière réaliste."""
        # 5% de valeurs manquantes dans le volume de données
        mask = np.random.random(self.n_samples) < 0.05
        df.loc[mask, 'volume_data'] = np.nan
        
        # 3% de valeurs manquantes dans le nombre de SMS
        mask = np.random.random(self.n_samples) < 0.03
        df.loc[mask, 'nombre_sms'] = np.nan
        
        # 2% de valeurs manquantes dans la zone géographique
        mask = np.random.random(self.n_samples) < 0.02
        df.loc[mask, 'zone_geographique'] = np.nan
        
    def save_data(self, df: pd.DataFrame, filename: str = 'donnees_clients.csv') -> None:
        """
        Sauvegarde les données générées.
        
        Parameters
        ----------
        df : pd.DataFrame
            Données à sauvegarder
        filename : str, default='donnees_clients.csv'
            Nom du fichier de sortie
        """
        file_path = Path(RAW_DATA_PATH) / filename
        df.to_csv(file_path, index=False)
        print(f"Données sauvegardées dans {file_path}")
        
    def generate_and_save(self, filename: str = 'donnees_clients.csv') -> pd.DataFrame:
        """
        Génère et sauvegarde les données.
        
        Parameters
        ----------
        filename : str, default='donnees_clients.csv'
            Nom du fichier de sortie
            
        Returns
        -------
        pd.DataFrame
            Données générées
        """
        df = self.generate_customer_data()
        self.save_data(df, filename)
        return df 