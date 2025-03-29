import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import sys
import os
from pathlib import Path

# Ajout du répertoire parent au PYTHONPATH
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root))

from src.config import (
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    RAW_DATA_FILE,
    PROCESSED_DATA_FILE
)

def check_missing_values(df):
    """
    Check and report missing values in the dataframe.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input data
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with missing value counts and percentages
    """
    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100
    
    missing_info = pd.DataFrame({
        'Missing Values': missing,
        'Percentage': missing_percent
    })
    
    return missing_info[missing_info['Missing Values'] > 0].sort_values('Missing Values', ascending=False)

def preprocess_data(df, numeric_features=NUMERIC_FEATURES, categorical_features=CATEGORICAL_FEATURES):
    """
    Preprocess data for clustering.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input data
    numeric_features : list
        List of numeric feature names
    categorical_features : list
        List of categorical feature names
        
    Returns:
    --------
    tuple
        (preprocessed_df, X_scaled, feature_names)
    """
    # Create a copy to avoid modifying the original dataframe
    processed_df = df.copy()
    
    # Handle missing values in numeric features
    if numeric_features:
        numeric_imputer = SimpleImputer(strategy='median')
        processed_df[numeric_features] = numeric_imputer.fit_transform(processed_df[numeric_features])
    
    # Handle missing values and encode categorical features
    encoded_features = []
    if categorical_features:
        # Impute missing categorical values with the most frequent value
        cat_imputer = SimpleImputer(strategy='most_frequent')
        processed_df[categorical_features] = cat_imputer.fit_transform(processed_df[categorical_features])
        
        # One-hot encode categorical features
        encoder = OneHotEncoder(sparse=False, drop='first')
        encoded_cats = encoder.fit_transform(processed_df[categorical_features])
        
        # Get feature names
        encoded_feature_names = []
        for i, cat in enumerate(categorical_features):
            categories = encoder.categories_[i][1:]  # Skip the first category (dropped)
            encoded_feature_names.extend([f"{cat}_{cat_val}" for cat_val in categories])
        
        # Create dataframe with encoded categorical features
        encoded_df = pd.DataFrame(encoded_cats, columns=encoded_feature_names, index=processed_df.index)
        encoded_features = encoded_feature_names
    else:
        encoded_df = pd.DataFrame(index=processed_df.index)
    
    # Scale numeric features
    X_numeric = processed_df[numeric_features].values if numeric_features else np.array([]).reshape(len(processed_df), 0)
    scaler = StandardScaler()
    X_numeric_scaled = scaler.fit_transform(X_numeric) if numeric_features else X_numeric
    
    # Create dataframe with scaled numeric features
    numeric_df = pd.DataFrame(X_numeric_scaled, columns=numeric_features, index=processed_df.index)
    
    # Combine scaled numeric and encoded categorical features
    X_prepared = pd.concat([numeric_df, encoded_df], axis=1)
    feature_names = numeric_features + encoded_features
    
    # Add ID column if it exists
    id_col = 'customer_id' if 'customer_id' in df.columns else None
    if id_col:
        processed_df = processed_df[[id_col]].join(X_prepared)
    else:
        processed_df = X_prepared.copy()
    
    return processed_df, X_prepared.values, feature_names

class DataPreprocessor:
    """
    Classe pour le prétraitement des données des clients.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.features = NUMERIC_FEATURES
    
    def load_data(self, input_file):
        """
        Charge les données brutes depuis un fichier CSV.
        
        Args:
            input_file (str): Chemin du fichier d'entrée
            
        Returns:
            pd.DataFrame: DataFrame contenant les données brutes
        """
        return pd.read_csv(input_file)
    
    def handle_missing_values(self, df):
        """
        Gère les valeurs manquantes dans le DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame d'entrée
            
        Returns:
            pd.DataFrame: DataFrame avec les valeurs manquantes traitées
        """
        # Remplacer les valeurs manquantes par la médiane pour chaque colonne
        for col in self.features:
            df[col] = df[col].fillna(df[col].median())
        return df
    
    def handle_outliers(self, df):
        """
        Gère les valeurs aberrantes dans le DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame d'entrée
            
        Returns:
            pd.DataFrame: DataFrame avec les valeurs aberrantes traitées
        """
        for col in self.features:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Remplacer les valeurs aberrantes par les bornes
            df[col] = df[col].clip(lower_bound, upper_bound)
        return df
    
    def scale_features(self, df):
        """
        Normalise les caractéristiques numériques.
        
        Args:
            df (pd.DataFrame): DataFrame d'entrée
            
        Returns:
            pd.DataFrame: DataFrame avec les caractéristiques normalisées
        """
        df_scaled = df.copy()
        df_scaled[self.features] = self.scaler.fit_transform(df[self.features])
        return df_scaled
    
    def preprocess(self, input_file, output_file):
        """
        Effectue le prétraitement complet des données.
        
        Args:
            input_file (str): Chemin du fichier d'entrée
            output_file (str): Chemin du fichier de sortie
        """
        # Chargement des données
        df = self.load_data(input_file)
        
        # Traitement des valeurs manquantes
        df = self.handle_missing_values(df)
        
        # Traitement des valeurs aberrantes
        df = self.handle_outliers(df)
        
        # Normalisation des caractéristiques
        df_scaled = self.scale_features(df)
        
        # Création du dossier de sortie s'il n'existe pas
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarde des données prétraitées
        df_scaled.to_csv(output_file, index=False)
        print(f"Données prétraitées sauvegardées dans {output_file}")
        
        return df_scaled

if __name__ == "__main__":
    # Création et utilisation du préprocesseur
    preprocessor = DataPreprocessor()
    df_processed = preprocessor.preprocess(RAW_DATA_FILE, PROCESSED_DATA_FILE)
    
    # Affichage des statistiques des données prétraitées
    print("\nStatistiques des données prétraitées :")
    print(df_processed.describe())