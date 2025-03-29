# Documentation Utilisateur - Segmentation Clients Tunisie Telecom

## Table des matières
1. [Introduction](#introduction)
2. [Accès à l'Application](#accès-à-lapplication)
3. [Utilisation de Jupyter](#utilisation-de-jupyter)
4. [Fonctionnalités](#fonctionnalités)
5. [Guide d'Utilisation](#guide-dutilisation)
6. [Interprétation des Résultats](#interprétation-des-résultats)
7. [FAQ](#faq)
8. [Exemples d'Utilisation](#exemples-dutilisation)
9. [Cas d'Usage Courants](#cas-dusage-courants)

## Introduction
Cette application web permet de visualiser et d'analyser la segmentation des clients de Tunisie Telecom. Elle offre une interface intuitive pour explorer les différents segments de clients et comprendre leurs caractéristiques principales.

## Accès à l'Application
1. Ouvrez votre terminal
2. Naviguez vers le dossier du projet
3. Exécutez la commande : `python src/web/app.py`
4. Accédez à l'application via votre navigateur à l'adresse : `http://localhost:5000`

## Utilisation de Jupyter

### Installation de Jupyter
1. Assurez-vous d'être dans votre environnement virtuel :
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. Installez Jupyter :
```bash
pip install jupyter notebook
```

### Lancement de Jupyter
1. Dans le terminal, naviguez vers le dossier du projet
2. Lancez Jupyter Notebook :
```bash
jupyter notebook
```
3. Votre navigateur s'ouvrira automatiquement sur l'interface Jupyter

### Structure des Notebooks
Les notebooks sont organisés dans le dossier `notebooks/` :
- `01_chargement_donnees.ipynb` : Chargement et exploration des données
- `02_preprocessing.ipynb` : Prétraitement des données
- `03_segmentation.ipynb` : Analyse de segmentation
- `04_visualisation.ipynb` : Création des visualisations
- `05_rapports.ipynb` : Génération des rapports

### Avantages de Jupyter
- **Interactivité** : Exécutez le code cellule par cellule
- **Documentation** : Mélangez code et explications
- **Visualisation** : Affichez les graphiques directement
- **Export** : Exportez en PDF ou HTML

### Exemple d'Utilisation
```python
# Dans un notebook
import pandas as pd
from src.models.segmentation import CustomerSegmentation
from src.models.visualization import SegmentationVisualizer

# Chargement des données
df = pd.read_csv('data/raw/donnees_clients.csv')

# Création du modèle
model = CustomerSegmentation()
model.fit(df)

# Visualisation
visualizer = SegmentationVisualizer(model)
visualizer.plot_cluster_distribution()
```

### Bonnes Pratiques
1. **Organisation** :
   - Créez un nouveau notebook pour chaque analyse
   - Nommez clairement vos notebooks
   - Gardez une copie de sauvegarde

2. **Documentation** :
   - Ajoutez des cellules Markdown pour expliquer
   - Documentez vos hypothèses
   - Incluez des exemples d'utilisation

3. **Performance** :
   - Nettoyez les outputs régulièrement
   - Redémarrez le kernel si nécessaire
   - Sauvegardez les résultats importants

### Intégration avec l'Application Web
Vous pouvez :
1. Développer vos analyses dans Jupyter
2. Exporter les visualisations
3. Utiliser le code dans l'application web
4. Partager les résultats via l'interface

### Astuces
- Utilisez `%matplotlib inline` pour les graphiques
- Activez les extensions Jupyter utiles
- Utilisez les raccourcis clavier pour plus d'efficacité
- Sauvegardez régulièrement votre travail

## Fonctionnalités

### 1. Distribution des Segments
- Visualisation de la répartition des clients par segment
- Graphique circulaire interactif
- Pourcentages et nombres de clients par segment

### 2. Analyse des Caractéristiques
- Visualisation des distributions par caractéristique
- Comparaison entre segments
- Identification des valeurs aberrantes

### 3. Profils des Segments
- Vue radar des caractéristiques moyennes par segment
- Comparaison facile entre segments
- Identification des points forts de chaque segment

### 4. Détails des Segments
- Statistiques détaillées par segment
- Offres commerciales recommandées
- Indicateurs clés de performance

## Guide d'Utilisation

### Navigation
- Utilisez le menu principal pour accéder aux différentes visualisations
- Survolez les graphiques pour voir les détails
- Cliquez sur les légendes pour filtrer les données

### Filtres et Interactions
- Double-cliquez sur les légendes pour isoler un segment
- Utilisez les boutons de zoom pour explorer les détails
- Exportez les graphiques en format PNG si nécessaire

## Interprétation des Résultats

### Distribution des Segments
- Les segments sont nommés de S1 à S5
- La taille des segments indique leur importance relative
- Les couleurs différencient clairement chaque segment

### Caractéristiques des Segments
- Les boîtes à moustaches montrent la distribution des valeurs
- Les points isolés représentent les valeurs aberrantes
- La médiane est indiquée par la ligne centrale

### Profils Types
- Chaque axe représente une caractéristique différente
- Plus la valeur est élevée, plus elle est importante
- Les formes permettent une comparaison rapide des profils

## FAQ

### Q: Comment interpréter les boîtes à moustaches ?
R: Les boîtes montrent la distribution des valeurs avec :
- La ligne centrale = médiane
- Les bords de la boîte = quartiles (25% et 75%)
- Les moustaches = valeurs min/max (hors aberrations)
- Les points = valeurs aberrantes

### Q: Comment utiliser les profils pour le marketing ?
R: Les profils permettent de :
- Identifier les caractéristiques dominantes de chaque segment
- Adapter les offres commerciales
- Cibler les communications marketing

### Q: Comment exporter les données ?
R: Vous pouvez :
- Capturer les graphiques en PNG
- Utiliser les API pour récupérer les données brutes
- Générer des rapports via l'interface

## Exemples d'Utilisation

### Exemple 1 : Analyse d'un Segment Spécifique
1. Sur la page d'accueil, localisez le graphique circulaire de distribution
2. Cliquez sur le segment "S1" dans la légende
3. Observez que :
   - Le pourcentage exact du segment s'affiche
   - Le nombre de clients dans ce segment apparaît
   - Les offres recommandées pour ce segment sont mises en évidence

### Exemple 2 : Comparaison de Caractéristiques
1. Accédez à la section "Analyse des Caractéristiques"
2. Pour comparer la consommation entre segments :
   - Survolez les boîtes à moustaches pour voir les valeurs exactes
   - Notez la médiane (ligne centrale) pour chaque segment
   - Identifiez les segments avec la plus forte/faible consommation

### Exemple 3 : Identification des Opportunités Marketing
1. Consultez le graphique des profils types
2. Pour le segment "S3" par exemple :
   - Notez une forte consommation de données
   - Faible utilisation des SMS
   - Âge moyen plus jeune
3. Conclusion : Opportunité pour des forfaits data premium

### Exemple 4 : Export et Partage des Résultats
1. Pour exporter un graphique :
   - Survolez le coin supérieur droit du graphique
   - Cliquez sur l'icône appareil photo
   - Choisissez le format (PNG recommandé)
   - Sauvegardez l'image

### Exemple 5 : Analyse des Valeurs Aberrantes
1. Dans le graphique des caractéristiques :
   - Repérez les points au-delà des moustaches
   - Survolez ces points pour voir les valeurs exactes
2. Utilisez ces informations pour :
   - Identifier les clients exceptionnels
   - Détecter des anomalies potentielles
   - Planifier des actions commerciales spécifiques

### Exemple 6 : Utilisation pour le Marketing Ciblé
Cas pratique : Lancement d'une nouvelle offre data
1. Identifiez les segments cibles :
   - Consultez le graphique radar des profils
   - Repérez les segments avec forte consommation data
2. Analysez les caractéristiques :
   - Vérifiez l'âge moyen
   - Examinez les habitudes de consommation
3. Personnalisez l'offre :
   - Adaptez le volume de données
   - Ajustez le prix selon le profil
   - Choisissez les canaux de communication appropriés

## Cas d'Usage Courants

### Pour l'Équipe Marketing
- **Objectif** : Création de nouvelles offres
- **Utilisation** : 
  1. Analyser les profils des segments
  2. Identifier les besoins non satisfaits
  3. Concevoir des offres adaptées
  4. Mesurer l'impact potentiel

### Pour l'Équipe Commerciale
- **Objectif** : Optimisation des ventes
- **Utilisation** :
  1. Consulter les détails des segments
  2. Préparer des arguments de vente ciblés
  3. Identifier les opportunités de cross-selling

### Pour la Direction
- **Objectif** : Prise de décision stratégique
- **Utilisation** :
  1. Visualiser la répartition globale
  2. Évaluer la performance par segment
  3. Identifier les tendances principales

## Support
Pour toute question ou assistance supplémentaire, contactez l'équipe technique à [adresse.email@tunisietelecom.tn] 