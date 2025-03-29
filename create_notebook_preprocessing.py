import nbformat as nbf
import json
import os

# Créer un nouveau notebook
nb = nbf.v4.new_notebook()

# Titre
title = nbf.v4.new_markdown_cell("# Prétraitement des Données\n\nCe notebook contient les étapes de prétraitement des données pour la segmentation des clients.")

# Import des bibliothèques
imports = nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer""")

# Chargement des données
load_data = nbf.v4.new_code_cell("""# Chargement des données brutes
df = pd.read_csv('../data/raw/donnees_clients.csv')

# Affichage des premières lignes
print("Aperçu des données :")
display(df.head())

# Informations sur le dataset
print("\nInformations sur le dataset :")
display(df.info())""")

# Analyse des valeurs manquantes
missing_values = nbf.v4.new_code_cell("""# Analyse des valeurs manquantes
missing_data = df.isnull().sum()
missing_percentages = (missing_data / len(df)) * 100

# Création d'un DataFrame pour l'affichage
missing_df = pd.DataFrame({
    'Valeurs manquantes': missing_data,
    'Pourcentage': missing_percentages
})

# Affichage des résultats
print("Analyse des valeurs manquantes :")
display(missing_df)

# Visualisation des valeurs manquantes
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), yticklabels=False, cbar=False, cmap='viridis')
plt.title('Carte des valeurs manquantes')
plt.show()""")

# Traitement des valeurs manquantes
handle_missing = nbf.v4.new_code_cell("""# Création de l'imputer
imputer = SimpleImputer(strategy='mean')

# Sélection des colonnes numériques
numeric_columns = df.select_dtypes(include=[np.number]).columns

# Imputation des valeurs manquantes
df[numeric_columns] = imputer.fit_transform(df[numeric_columns])

# Vérification qu'il n'y a plus de valeurs manquantes
print("Vérification des valeurs manquantes après imputation :")
display(df.isnull().sum())""")

# Normalisation des données
normalize = nbf.v4.new_code_cell("""# Création du scaler
scaler = StandardScaler()

# Normalisation des données
df_scaled = pd.DataFrame(
    scaler.fit_transform(df[numeric_columns]),
    columns=numeric_columns
)

# Affichage des statistiques avant et après normalisation
print("Statistiques avant normalisation :")
display(df[numeric_columns].describe())

print("\nStatistiques après normalisation :")
display(df_scaled.describe())""")

# Sauvegarde des données prétraitées
save_data = nbf.v4.new_code_cell("""# Sauvegarde des données prétraitées
df_scaled.to_csv('../data/processed/donnees_pretraitees.csv', index=False)
print("Données prétraitées sauvegardées avec succès !")""")

# Ajout des cellules au notebook
nb.cells = [title, imports, load_data, missing_values, handle_missing, normalize, save_data]

# Création du dossier notebooks s'il n'existe pas
os.makedirs('notebooks', exist_ok=True)

# Sauvegarde du notebook
with open('notebooks/02_preprocessing.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook de prétraitement créé avec succès !") 