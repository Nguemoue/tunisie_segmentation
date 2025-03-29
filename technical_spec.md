# Spécifications Techniques - Segmentation Clients Tunisie Telecom

## Table des matières
1. [Architecture](#architecture)
2. [Technologies Utilisées](#technologies-utilisées)
3. [Structure du Projet](#structure-du-projet)
4. [API](#api)
5. [Modèles de Données](#modèles-de-données)
6. [Configuration](#configuration)
7. [Déploiement](#déploiement)

## Architecture

### Vue d'ensemble
L'application suit une architecture MVC (Modèle-Vue-Contrôleur) avec :
- Backend : Flask (Python)
- Frontend : HTML/CSS/JavaScript
- Visualisation : Plotly.js
- Traitement des données : Pandas

### Flux de données
1. Chargement des données brutes (CSV)
2. Prétraitement et segmentation
3. Génération des visualisations
4. Exposition via API REST
5. Rendu côté client

## Technologies Utilisées

### Backend
- Python 3.8+
- Flask 2.0+
- Pandas 1.4+
- NumPy 1.20+
- Plotly 5.0+

### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5
- Plotly.js

### Outils de développement
- Git
- VSCode
- Python venv

## Structure du Projet
```
tunisie_telecom_segmentation/
├── src/
│   ├── web/
│   │   ├── app.py
│   │   ├── static/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── img/
│   │   └── templates/
│   ├── models/
│   │   ├── segmentation.py
│   │   └── visualization.py
│   └── utils/
├── data/
│   ├── raw/
│   └── processed/
├── config.py
├── requirements.txt
└── README.md
```

## API

### Endpoints

#### GET /api/cluster_distribution
```json
{
    "data": {
        "values": [...],
        "labels": [...],
        "type": "pie"
    }
}
```

#### GET /api/feature_importance
```json
{
    "data": [
        {
            "feature": "...",
            "values": [...],
            "segments": [...]
        }
    ]
}
```

#### GET /api/cluster_profiles
```json
{
    "data": {
        "profiles": [...],
        "features": [...],
        "segments": [...]
    }
}
```

#### GET /api/segment_details
```json
{
    "segment_id": {
        "size": int,
        "percentage": float,
        "mean_values": {...},
        "offer": string
    }
}
```

## Modèles de Données

### Structure des données d'entrée
```python
{
    'age': int,
    'montant_consommation': float,
    'nombre_appels': int,
    'volume_data': float,
    'nombre_sms': int
}
```

### Configuration des segments
```python
SEGMENT_LABELS = ['S1', 'S2', 'S3', 'S4', 'S5']
```

## Configuration

### Variables d'environnement
- `FLASK_ENV`: development/production
- `FLASK_DEBUG`: 0/1
- `RAW_DATA_PATH`: chemin vers les données brutes
- `FIGURES_PATH`: chemin pour sauvegarder les graphiques

### Fichier config.py
```python
RAW_DATA_PATH = 'data/raw'
FIGURES_PATH = 'data/figures'
SEGMENT_LABELS = ['S1', 'S2', 'S3', 'S4', 'S5']
COMMERCIAL_OFFERS = {...}
```

## Déploiement

### Prérequis
1. Python 3.8+
2. pip
3. virtualenv

### Installation
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement
```bash
python src/web/app.py
```

### Production
Pour le déploiement en production :
1. Utiliser un serveur WSGI (Gunicorn/uWSGI)
2. Configurer un reverse proxy (Nginx/Apache)
3. Mettre en place un système de logs
4. Configurer SSL/TLS

### Sécurité
- Validation des entrées
- Protection CSRF
- Headers de sécurité
- Rate limiting
- Sanitization des données

## Maintenance

### Logs
- Niveau INFO pour les opérations normales
- Niveau ERROR pour les exceptions
- Rotation des logs quotidienne

### Monitoring
- Métriques système
- Temps de réponse API
- Utilisation mémoire
- Erreurs serveur

### Sauvegarde
- Données brutes : quotidienne
- Configuration : à chaque modification
- Base de données : incrémentale 