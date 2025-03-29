import nbformat as nbf
import json

# Créer un nouveau notebook
nb = nbf.v4.new_notebook()

# Créer une cellule markdown pour le titre
title_cell = nbf.v4.new_markdown_cell('''# Visualisation des Résultats de Segmentation

Ce notebook montre comment créer des visualisations détaillées des résultats de segmentation.''')

# Créer une cellule de code pour les imports
imports_cell = nbf.v4.new_code_cell('''# Import des bibliothèques nécessaires
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration de l'affichage
%matplotlib inline
plt.style.use('seaborn')
pd.set_option('display.max_columns', None)''')

# Créer une cellule markdown pour la section de chargement
loading_section = nbf.v4.new_markdown_cell('''## 1. Chargement des données segmentées''')

# Créer une cellule de code pour le chargement
loading_cell = nbf.v4.new_code_cell('''# Chargement des données avec les clusters
df = pd.read_csv('../data/processed/donnees_pretraitees.csv')
df['cluster'] = pd.read_csv('../data/processed/clusters.csv')['cluster']

# Affichage des premières lignes
print("Données segmentées :")
display(df.head())''')

# Créer une cellule markdown pour la section de distribution
distribution_section = nbf.v4.new_markdown_cell('''## 2. Distribution des clusters''')

# Créer une cellule de code pour la distribution
distribution_cell = nbf.v4.new_code_cell('''# Création du graphique de distribution des clusters
fig = px.pie(df, names='cluster', title='Distribution des clusters')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()''')

# Créer une cellule markdown pour la section des profils
profiles_section = nbf.v4.new_markdown_cell('''## 3. Profils des clusters''')

# Créer une cellule de code pour les profils
profiles_cell = nbf.v4.new_code_cell('''# Calcul des moyennes par cluster
cluster_means = df.groupby('cluster').mean()

# Création du heatmap des profils
plt.figure(figsize=(12, 8))
sns.heatmap(cluster_means, annot=True, cmap='YlOrRd', center=0)
plt.title('Profils des clusters')
plt.show()''')

# Créer une cellule markdown pour la section des caractéristiques
features_section = nbf.v4.new_markdown_cell('''## 4. Visualisation interactive des caractéristiques''')

# Créer une cellule de code pour les caractéristiques
features_cell = nbf.v4.new_code_cell('''# Création d'un graphique interactif
fig = make_subplots(rows=2, cols=2, subplot_titles=(
    'Âge par cluster', 'Consommation par cluster',
    'Nombre d\'appels par cluster', 'Volume de données par cluster'
))

# Ajout des traces
fig.add_trace(go.Box(y=df['age'], x=df['cluster'], name='Âge'), row=1, col=1)
fig.add_trace(go.Box(y=df['montant_consommation'], x=df['cluster'], name='Consommation'), row=1, col=2)
fig.add_trace(go.Box(y=df['nombre_appels'], x=df['cluster'], name='Appels'), row=2, col=1)
fig.add_trace(go.Box(y=df['volume_data'], x=df['cluster'], name='Data'), row=2, col=2)

# Mise à jour du layout
fig.update_layout(height=800, showlegend=False)
fig.show()''')

# Créer une cellule markdown pour la section des offres
offers_section = nbf.v4.new_markdown_cell('''## 5. Analyse des offres commerciales par segment''')

# Créer une cellule de code pour les offres
offers_cell = nbf.v4.new_code_cell('''# Création d'un graphique des offres commerciales
offres = pd.DataFrame({
    'cluster': range(5),
    'offre': ['Offre Premium', 'Offre Standard', 'Offre Économique', 'Offre Data', 'Offre Voice']
})

fig = px.bar(offres, x='cluster', y='offre', title='Offres commerciales par segment')
fig.show()''')

# Ajouter toutes les cellules au notebook
nb.cells = [
    title_cell,
    imports_cell,
    loading_section,
    loading_cell,
    distribution_section,
    distribution_cell,
    profiles_section,
    profiles_cell,
    features_section,
    features_cell,
    offers_section,
    offers_cell
]

# Sauvegarder le notebook en format JSON
notebook_path = 'notebooks/04_visualisation.ipynb'
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print(f"Notebook créé avec succès à l'emplacement : {notebook_path}") 