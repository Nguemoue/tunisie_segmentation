import nbformat as nbf
import json

# Créer un nouveau notebook
nb = nbf.v4.new_notebook()

# Créer une cellule markdown pour le titre
title_cell = nbf.v4.new_markdown_cell('''# Segmentation des Clients

Ce notebook montre l'application des techniques de clustering pour segmenter les clients de Tunisie Telecom.''')

# Créer une cellule de code pour les imports
imports_cell = nbf.v4.new_code_cell('''# Import des bibliothèques nécessaires
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

# Configuration de l'affichage
%matplotlib inline
plt.style.use('seaborn')
pd.set_option('display.max_columns', None)''')

# Créer une cellule markdown pour la section de chargement
loading_section = nbf.v4.new_markdown_cell('''## 1. Chargement des données prétraitées''')

# Créer une cellule de code pour le chargement
loading_cell = nbf.v4.new_code_cell('''# Chargement des données prétraitées
df = pd.read_csv('../data/processed/donnees_pretraitees.csv')

# Affichage des premières lignes
print("Données prétraitées :")
display(df.head())''')

# Créer une cellule markdown pour la section du nombre optimal de clusters
n_clusters_section = nbf.v4.new_markdown_cell('''## 2. Détermination du nombre optimal de clusters''')

# Créer une cellule de code pour le nombre optimal de clusters
n_clusters_cell = nbf.v4.new_code_cell('''# Test de différents nombres de clusters
n_clusters_range = range(2, 11)
silhouette_scores = []
calinski_scores = []

for n_clusters in n_clusters_range:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(df)
    
    silhouette_scores.append(silhouette_score(df, cluster_labels))
    calinski_scores.append(calinski_harabasz_score(df, cluster_labels))

# Visualisation des scores
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

ax1.plot(list(n_clusters_range), silhouette_scores, 'bo-')
ax1.set_xlabel('Nombre de clusters')
ax1.set_ylabel('Score de silhouette')
ax1.set_title('Score de silhouette par nombre de clusters')

ax2.plot(list(n_clusters_range), calinski_scores, 'ro-')
ax2.set_xlabel('Nombre de clusters')
ax2.set_ylabel('Score de Calinski-Harabasz')
ax2.set_title('Score de Calinski-Harabasz par nombre de clusters')

plt.tight_layout()
plt.show()''')

# Créer une cellule markdown pour la section de clustering
clustering_section = nbf.v4.new_markdown_cell('''## 3. Application du clustering''')

# Créer une cellule de code pour le clustering
clustering_cell = nbf.v4.new_code_cell('''# Application du K-means avec le nombre optimal de clusters
n_clusters = 5  # À ajuster selon les résultats précédents
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(df)

# Affichage des centres des clusters
print("Centres des clusters :")
display(pd.DataFrame(kmeans.cluster_centers_, columns=df.columns[:-1]))''')

# Créer une cellule markdown pour la section de visualisation
viz_section = nbf.v4.new_markdown_cell('''## 4. Visualisation des clusters''')

# Créer une cellule de code pour la visualisation
viz_cell = nbf.v4.new_code_cell('''# Réduction de dimensionnalité avec PCA
pca = PCA(n_components=2)
df_pca = pca.fit_transform(df.drop('cluster', axis=1))

# Visualisation des clusters en 2D
plt.figure(figsize=(10, 8))
scatter = plt.scatter(df_pca[:, 0], df_pca[:, 1], c=df['cluster'], cmap='viridis')
plt.xlabel('Première composante principale')
plt.ylabel('Deuxième composante principale')
plt.title('Visualisation des clusters en 2D')
plt.colorbar(scatter)
plt.show()''')

# Créer une cellule markdown pour la section des profils
profiles_section = nbf.v4.new_markdown_cell('''## 5. Analyse des profils des clusters''')

# Créer une cellule de code pour les profils
profiles_cell = nbf.v4.new_code_cell('''# Statistiques par cluster
print("Statistiques par cluster :")
display(df.groupby('cluster').mean())

# Taille des clusters
print("\\nTaille des clusters :")
display(df['cluster'].value_counts().sort_index())''')

# Ajouter toutes les cellules au notebook
nb.cells = [
    title_cell,
    imports_cell,
    loading_section,
    loading_cell,
    n_clusters_section,
    n_clusters_cell,
    clustering_section,
    clustering_cell,
    viz_section,
    viz_cell,
    profiles_section,
    profiles_cell
]

# Sauvegarder le notebook en format JSON
notebook_path = 'notebooks/03_segmentation.ipynb'
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print(f"Notebook créé avec succès à l'emplacement : {notebook_path}") 