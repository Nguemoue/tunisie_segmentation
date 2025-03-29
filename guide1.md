# Guide du Projet de Segmentation Clients Tunisie Telecom

## Table des matières
1. [Vue d'ensemble du projet](#vue-densemble-du-projet)
2. [Prérequis](#prérequis)
3. [Installation](#installation)
4. [Structure du projet](#structure-du-projet)
5. [Utilisation](#utilisation)
6. [Résultats et visualisations](#résultats-et-visualisations)
7. [Personnalisation](#personnalisation)
8. [Dépannage](#dépannage)

## Vue d'ensemble du projet

Ce projet vise à segmenter les clients de Tunisie Telecom en utilisant des techniques de clustering avancées. L'objectif est d'identifier des groupes de clients homogènes pour :
- Personnaliser les offres commerciales
- Optimiser les campagnes marketing
- Améliorer la satisfaction client
- Augmenter la fidélisation

### Fonctionnalités principales
- Génération de données synthétiques réalistes
- Prétraitement automatique des données
- Segmentation des clients avec K-Means
- Évaluation de la qualité de la segmentation
- Visualisations interactives
- Génération de rapports détaillés
- Stratégies marketing personnalisées

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (optionnel, pour le contrôle de version)

## Installation

1. Cloner le repository (optionnel) :
```bash
git clone https://github.com/votre-username/tunisie_telecom_segmentation.git
cd tunisie_telecom_segmentation
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
```

3. Activer l'environnement virtuel :
- Windows :
```bash
venv\Scripts\activate
```
- Linux/Mac :
```bash
source venv/bin/activate
```

4. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Structure du projet

```
tunisie_telecom_segmentation/
├── data/
│   ├── raw/                 # Données brutes
│   └── processed/           # Données prétraitées
├── figures/                 # Visualisations générées
├── logs/                    # Fichiers de journalisation
├── reports/                 # Rapports générés
├── src/
│   ├── data/               # Modules de gestion des données
│   └── models/             # Modules de modélisation
├── config.py               # Configuration du projet
├── generate_data.py        # Script de génération de données
├── main.py                 # Script principal
├── requirements.txt        # Dépendances du projet
└── guide.md               # Ce guide
```

## Utilisation

### 1. Génération des données

Pour générer des données synthétiques :
```bash
python generate_data.py
```

### 2. Exécution de la segmentation

Pour lancer l'analyse complète :
```bash
python main.py
```

Le script va :
- Charger les données
- Effectuer le prétraitement
- Appliquer la segmentation
- Générer les visualisations
- Créer les rapports

### 3. Visualisation des résultats

Les résultats sont stockés dans les dossiers suivants :
- `figures/` : Graphiques et visualisations
- `reports/` : Rapports détaillés
- `logs/` : Fichiers de journalisation

## Résultats et visualisations

### Visualisations générées
1. **Distribution des segments** (`cluster_distribution.png`)
   - Répartition des clients par segment
   - Pourcentages et tailles des segments

2. **Caractéristiques des centres** (`cluster_centers.png`)
   - Heatmap des caractéristiques moyennes
   - Comparaison entre segments

3. **Importance des features** (`feature_importance.png`)
   - Contribution des variables par segment
   - Identification des caractéristiques clés

4. **Profils des segments** (`cluster_profiles.png`)
   - Caractéristiques détaillées par segment
   - Écart-type et moyennes

5. **Résultats du clustering** (`clustering_results.png`)
   - Visualisation 2D des clusters
   - Distribution spatiale des segments

6. **Offres commerciales** (`commercial_offers.png`)
   - Comparaison des offres par segment
   - Réductions et services additionnels

### Rapports générés
1. **Rapport de segmentation** (`rapport_segmentation_*.md`)
   - Analyse détaillée des segments
   - Statistiques et KPIs
   - Recommandations

2. **Résumé exécutif** (`resume_executif_*.md`)
   - Vue d'ensemble
   - Points clés
   - Actions prioritaires

3. **Stratégie marketing** (`strategie_marketing_*.md`)
   - Objectifs
   - Stratégies par segment
   - Plan d'action

## Personnalisation

### Configuration
Le fichier `config.py` permet de personnaliser :
- Paramètres de segmentation
- Seuils des KPIs
- Offres commerciales
- Chemins des dossiers

### Ajout de nouvelles fonctionnalités
1. Créer un nouveau module dans `src/models/`
2. Importer le module dans `main.py`
3. Ajouter les appels de fonction appropriés

## Dépannage

### Problèmes courants
1. **Erreur de dépendances**
   - Solution : Réinstaller les dépendances avec `pip install -r requirements.txt`

2. **Erreur de chemins**
   - Solution : Vérifier la structure des dossiers
   - Créer les dossiers manquants

3. **Erreur de mémoire**
   - Solution : Réduire la taille des données
   - Optimiser les paramètres de clustering

### Logs
Les logs sont stockés dans le dossier `logs/` pour faciliter le débogage.

## Support

Pour toute question ou problème :
1. Consulter la documentation
2. Vérifier les logs
3. Contacter l'équipe de support

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 