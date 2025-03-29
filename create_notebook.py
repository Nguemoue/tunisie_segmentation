import nbformat as nbf

# Créer un nouveau notebook
nb = nbf.v4.new_notebook()

# Créer une cellule markdown pour le titre
title_cell = nbf.v4.new_markdown_cell('''# Chargement et Exploration des Données

Ce notebook montre comment charger et explorer les données des clients de Tunisie Telecom.''')

# Créer une cellule de code pour les imports
imports_cell = nbf.v4.new_code_cell('''# Import des bibliothèques nécessaires
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Configuration de l'affichage
%matplotlib inline
plt.style.use('seaborn')
pd.set_option('display.max_columns', None)''')

# Créer une cellule markdown pour la section de chargement
loading_section = nbf.v4.new_markdown_cell('''## 1. Chargement des données''')

# Créer une cellule de code pour le chargement
loading_cell = nbf.v4.new_code_cell('''# Chargement des données
df = pd.read_csv('../data/raw/donnees_clients.csv')

# Affichage des premières lignes
print("Aperçu des données :")
display(df.head())

# Informations sur le dataset
print("\\nInformations sur le dataset :")
display(df.info())''')

# Créer une cellule markdown pour la section des statistiques
stats_section = nbf.v4.new_markdown_cell('''## 2. Statistiques descriptives''')

# Créer une cellule de code pour les statistiques
stats_cell = nbf.v4.new_code_cell('''# Statistiques descriptives
print("Statistiques descriptives :")
display(df.describe())''')

# Créer une cellule markdown pour la section des visualisations
viz_section = nbf.v4.new_markdown_cell('''## 3. Visualisations initiales''')

# Créer une cellule de code pour les visualisations
viz_cell = nbf.v4.new_code_cell('''# Création d'une figure avec plusieurs sous-graphiques
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Distribution de l'âge
sns.histplot(data=df, x='age', bins=30, ax=axes[0,0])
axes[0,0].set_title('Distribution de l\'âge')

# Distribution de la consommation
sns.histplot(data=df, x='montant_consommation', bins=30, ax=axes[0,1])
axes[0,1].set_title('Distribution de la consommation')

# Nombre d'appels par âge
sns.scatterplot(data=df, x='age', y='nombre_appels', ax=axes[1,0])
axes[1,0].set_title('Nombre d\'appels par âge')

# Volume de données par consommation
sns.scatterplot(data=df, x='montant_consommation', y='volume_data', ax=axes[1,1])
axes[1,1].set_title('Volume de données par consommation')

plt.tight_layout()
plt.show()''')

# Créer une cellule markdown pour la section des corrélations
corr_section = nbf.v4.new_markdown_cell('''## 4. Analyse des corrélations''')

# Créer une cellule de code pour les corrélations
corr_cell = nbf.v4.new_code_cell('''# Matrice de corrélation
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Matrice de corrélation')
plt.show()''')

# Ajouter toutes les cellules au notebook
nb.cells = [
    title_cell,
    imports_cell,
    loading_section,
    loading_cell,
    stats_section,
    stats_cell,
    viz_section,
    viz_cell,
    corr_section,
    corr_cell
]

# Sauvegarder le notebook
with open('notebooks/01_chargement_donnees.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook créé avec succès !") 