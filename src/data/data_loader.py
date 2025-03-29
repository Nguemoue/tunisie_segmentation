"""
Module de chargement et de prétraitement des données pour le projet de segmentation Tunisie Telecom.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, List, Dict, Optional
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

from config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    PREPROCESSING_PARAMS,
    VALIDATION_PARAMS
)

class DataLoader:
    """Classe pour charger et prétraiter les données."""
    
    def __init__(self):
        """Initialise le chargeur de données."""
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None
        
    def load_raw_data(self, filename: str, **kwargs) -> pd.DataFrame:
        """
        Charge les données brutes depuis le dossier raw.
        
        Parameters
        ----------
        filename : str
            Nom du fichier à charger
        **kwargs : dict
            Arguments supplémentaires pour pd.read_csv ou pd.read_excel
            
        Returns
        -------
        pd.DataFrame
            Données brutes chargées
        """
        file_path = Path(RAW_DATA_PATH) / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Le fichier {filename} n'existe pas dans {RAW_DATA_PATH}")
            
        if filename.endswith('.csv'):
            return pd.read_csv(file_path, **kwargs)
        elif filename.endswith(('.xls', '.xlsx')):
            return pd.read_excel(file_path, **kwargs)
        else:
            raise ValueError(f"Format de fichier non supporté pour {filename}")
            
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prétraite les données.
        
        Parameters
        ----------
        df : pd.DataFrame
            Données brutes
            
        Returns
        -------
        pd.DataFrame
            Données prétraitées
        """
        # Copie pour éviter la modification des données originales
        df_processed = df.copy()
        
        # Gestion des valeurs manquantes
        df_processed = self._handle_missing_values(df_processed)
        
        # Encodage des variables catégorielles
        df_processed = self._encode_categorical_features(df_processed)
        
        # Normalisation des variables numériques
        df_processed = self._normalize_numerical_features(df_processed)
        
        # Sauvegarde des noms des features
        self.feature_names = df_processed.columns.tolist()
        
        return df_processed
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Gère les valeurs manquantes."""
        # Pour les variables numériques
        for col in PREPROCESSING_PARAMS['numerical_columns']:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].mean())
                
        # Pour les variables catégorielles
        for col in PREPROCESSING_PARAMS['categorical_columns']:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].mode()[0])
                
        return df
    
    def _encode_categorical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encode les variables catégorielles."""
        for col in PREPROCESSING_PARAMS['categorical_columns']:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                self.label_encoders[col] = le
                
        return df
    
    def _normalize_numerical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalise les variables numériques."""
        numerical_cols = [col for col in PREPROCESSING_PARAMS['numerical_columns'] 
                         if col in df.columns]
        
        if numerical_cols:
            df[numerical_cols] = self.scaler.fit_transform(df[numerical_cols])
            
        return df
    
    def split_data(self, df: pd.DataFrame, target_col: Optional[str] = None) -> Dict[str, pd.DataFrame]:
        """
        Divise les données en ensembles d'entraînement et de test.
        
        Parameters
        ----------
        df : pd.DataFrame
            Données prétraitées
        target_col : str, optional
            Colonne cible si disponible
            
        Returns
        -------
        Dict[str, pd.DataFrame]
            Dictionnaire contenant les ensembles d'entraînement et de test
        """
        if target_col and target_col in df.columns:
            X = df.drop(columns=[target_col])
            y = df[target_col]
        else:
            X = df
            y = None
            
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=VALIDATION_PARAMS['test_size'],
            random_state=VALIDATION_PARAMS['random_state']
        )
        
        return {
            'X_train': X_train,
            'X_test': X_test,
            'y_train': y_train,
            'y_test': y_test
        }
    
    def save_processed_data(self, data: pd.DataFrame, filename: str) -> None:
        """
        Sauvegarde les données prétraitées.
        
        Parameters
        ----------
        data : pd.DataFrame
            Données à sauvegarder
        filename : str
            Nom du fichier de sortie
        """
        file_path = Path(PROCESSED_DATA_PATH) / filename
        
        if filename.endswith('.csv'):
            data.to_csv(file_path, index=False)
        elif filename.endswith(('.xls', '.xlsx')):
            data.to_excel(file_path, index=False)
        else:
            raise ValueError(f"Format de fichier non supporté pour {filename}")
            
        print(f"Données sauvegardées dans {file_path}")
        
    def load_processed_data(self, filename: str) -> pd.DataFrame:
        """
        Charge les données prétraitées.
        
        Parameters
        ----------
        filename : str
            Nom du fichier à charger
            
        Returns
        -------
        pd.DataFrame
            Données prétraitées chargées
        """
        file_path = Path(PROCESSED_DATA_PATH) / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Le fichier {filename} n'existe pas dans {PROCESSED_DATA_PATH}")
            
        if filename.endswith('.csv'):
            return pd.read_csv(file_path)
        elif filename.endswith(('.xls', '.xlsx')):
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Format de fichier non supporté pour {filename}")