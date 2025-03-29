# Projet de Segmentation Tunisie Telecom

Ce projet vise à réaliser une analyse de segmentation des clients de Tunisie Telecom en utilisant des techniques d'analyse de données et d'apprentissage automatique.

## Table des matières
1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Structure du Projet](#structure-du-projet)
4. [Configuration de l'Environnement](#configuration-de-lenvironnement)
5. [Utilisation des Notebooks](#utilisation-des-notebooks)
6. [Dépannage](#dépannage)

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (optionnel, pour le contrôle de version)
- Un éditeur de texte (VS Code recommandé)

## Installation

1. **Cloner le projet** (si vous utilisez Git) :
   ```bash
   git clone https://github.com/votre-compte/tunisie_telecom_segmentation.git
   cd tunisie_telecom_segmentation
   ```

2. **Créer un environnement virtuel** :
   ```bash
   # Sur Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Sur Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installer les dépendances** :
   ```bash
   # Mettre à jour pip
   python -m pip install --upgrade pip

   # Installer les dépendances
   pip install -r requirements.txt
   ```

4. **Configurer Jupyter** :
   ```bash
   # Installer le kernel Jupyter pour le projet
   python -m ipykernel install --user --name=tunisie_telecom --display-name="Python (Tunisie Telecom)"
   ```

## Structure du Projet

```
tunisie_telecom_segmentation/
│
├── data/                    # Dossier des données
│   ├── raw/                # Données brutes
│   └── processed/          # Données traitées
│
├── notebooks/              # Notebooks Jupyter
│   ├── 01_exploration_donnees.ipynb    # Exploration des données
│   ├── 02_preparation_donnees.ipynb    # Préparation des données
│   └── 03_analyse_segmentation.ipynb   # Analyse de segmentation
│
├── src/                    # Code source
│   ├── data/              # Scripts de manipulation des données
│   └── models/            # Scripts des modèles
│
├── reports/               # Rapports et visualisations
├── venv/                 # Environnement virtuel Python
├── requirements.txt      # Dépendances du projet
└── README.md            # Ce fichier
```

## Configuration de l'Environnement

1. **Activer l'environnement virtuel** :
   ```bash
   # Sur Windows
   .\venv\Scripts\activate

   # Sur Linux/Mac
   source venv/bin/activate
   ```

2. **Lancer Jupyter Notebook** :
   ```bash
   jupyter notebook
   ```

3. **Accéder à l'interface web** :
   - Ouvrez votre navigateur
   - Accédez à l'URL affichée dans le terminal (généralement http://localhost:8888)
   - Si un token est demandé, copiez-le depuis le terminal

## Utilisation des Notebooks

### 1. Notebook d'Exploration des Données (01_exploration_donnees.ipynb)
- Vue d'ensemble des données
- Statistiques descriptives
- Visualisations initiales
- Identification des valeurs manquantes

Pour utiliser :
1. Ouvrez le notebook dans Jupyter
2. Sélectionnez le kernel "Python (Tunisie Telecom)"
3. Exécutez les cellules une par une (Shift + Enter)

### 2. Notebook de Préparation des Données (02_preparation_donnees.ipynb)
- Nettoyage des données
- Traitement des valeurs manquantes
- Encodage des variables catégorielles
- Normalisation des données

### 3. Notebook d'Analyse de Segmentation (03_analyse_segmentation.ipynb)
- Analyse en composantes principales
- Clustering K-means
- Évaluation des segments
- Visualisation des résultats

## Dépannage

### Problèmes courants et solutions

1. **Le kernel ne démarre pas** :
   ```bash
   # Réinstaller le kernel
   python -m ipykernel install --user --name=tunisie_telecom --display-name="Python (Tunisie Telecom)"
   ```

2. **Modules non trouvés** :
   ```bash
   # Vérifier l'activation de l'environnement virtuel
   # Réinstaller les dépendances
   pip install -r requirements.txt
   ```

3. **Erreur de mémoire** :
   - Redémarrer le kernel
   - Fermer les autres applications
   - Réduire la taille des données traitées

### Support

Pour toute question ou problème :
1. Consultez la documentation des bibliothèques utilisées
2. Vérifiez les messages d'erreur dans les logs
3. Contactez l'équipe de support

---
Pour plus d'informations ou en cas de problème, contactez [lucchuala@gmail.com]

# Demarer la version web du projet 
```
$env:PYTHONPATH = "."; python src/web/app.py
```

# Demare la version code 
```python
python main.py
```