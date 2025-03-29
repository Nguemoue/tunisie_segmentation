import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import NUMERIC_FEATURES, CATEGORICAL_FEATURES

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