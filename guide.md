# Guide d'Installation et d'Utilisation - Segmentation Clients Tunisie Telecom

## Table des matières
1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Structure du Projet](#structure-du-projet)
5. [Lancement de l'Application](#lancement-de-lapplication)
6. [Utilisation](#utilisation)
7. [Dépannage](#dépannage)

## Prérequis

Avant de commencer l'installation, assurez-vous d'avoir :
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (optionnel, pour cloner le projet)
- Au moins 4 Go de RAM disponible
- Espace disque : minimum 1 Go

### Dépendances principales
- scikit-learn>=1.0.2
- pandas>=1.4.0
- numpy>=1.21.0
- matplotlib>=3.5.0
- seaborn>=0.11.2
- flask>=2.0.0
- plotly>=5.5.0

## Installation

1. **Cloner le projet** (si vous utilisez Git) :
```bash
git clone [URL_DU_PROJET]
cd tunisie_telecom_segmentation
```

2. **Créer un environnement virtuel** :
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel** :
- Windows :
```bash
.\venv\Scripts\activate
```
- Linux/Mac :
```bash
source venv/bin/activate
```

4. **Installer les dépendances** :
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

1. **Configuration des données** :
- Placez vos fichiers de données dans le dossier `data/raw/`
- Format attendu : fichiers CSV avec les colonnes suivantes :
  - id_client
  - age
  - montant_consommation
  - frequence_appels
  - duree_appels
  - services_souscrits

2. **Configuration de l'environnement** :
- Copiez le fichier `.env.example` vers `.env`
- Modifiez les variables selon votre environnement :
```bash
DEBUG=True
PORT=5000
HOST=localhost
DATA_PATH=data/raw/donnees_clients.csv
```

3. **Configuration du modèle** :
Dans `config.py`, vous pouvez ajuster :
- `N_CLUSTERS` : nombre de segments (par défaut : 5)
- `RANDOM_STATE` : graine aléatoire (par défaut : 42)
- `FEATURES` : liste des caractéristiques à utiliser

## Structure du Projet

```
tunisie_telecom_segmentation/
├── data/
│   ├── raw/                 # Données brutes
│   └── processed/           # Données prétraitées
├── src/
│   ├── data/               # Modules de chargement et prétraitement
│   ├── models/             # Modules de segmentation et visualisation
│   └── web/                # Application web
├── notebooks/              # Notebooks Jupyter
├── logs/                   # Fichiers de logs
├── reports/                # Rapports générés
├── figures/                # Visualisations générées
├── requirements.txt        # Dépendances du projet
├── .env                    # Variables d'environnement
└── config.py              # Configuration du projet
```

## Lancement de l'Application

1. **Vérification de l'environnement** :
```bash
python check_environment.py
```

2. **Préparation des données** :
```bash
python main.py
```
Cette commande va :
- Charger les données brutes
- Effectuer le prétraitement
- Appliquer la segmentation
- Générer les visualisations
- Créer les rapports

3. **Lancer l'application web** :
```bash
python src/web/app.py
```

4. **Accéder à l'interface** :
- Ouvrez votre navigateur
- Accédez à : `http://localhost:5000`
- Identifiants par défaut :
  - Utilisateur : admin
  - Mot de passe : admin123

## Utilisation

### Interface Web

L'application web offre les fonctionnalités suivantes :

1. **Vue d'ensemble** :
   - Nombre total de clients
   - Nombre de segments
   - Âge moyen
   - Consommation moyenne
   - KPIs principaux

2. **Visualisations** :
   - Distribution des segments
   - Profils des segments
   - Importance des caractéristiques
   - Détails des offres commerciales
   - Évolution temporelle

3. **Tableau détaillé** :
   - Informations par segment
   - Statistiques clés
   - Offres commerciales recommandées
   - Taux de conversion estimé

### Fonctionnalités

- **Rafraîchissement automatique** : Les données sont mises à jour toutes les 5 minutes
- **Graphiques interactifs** : Possibilité de zoomer, filtrer et exporter
- **Responsive design** : Interface adaptée aux mobiles et tablettes
- **Export des données** : Format CSV, Excel et PDF
- **Filtres avancés** : Par segment, période et caractéristiques

## Dépannage

### Problèmes courants

1. **Erreur de dépendances** :
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

2. **Erreur de port** :
- Si le port 5000 est déjà utilisé :
```bash
# Dans .env
PORT=5001
```
Ou dans la ligne de commande :
```bash
python src/web/app.py --port 5001
```

3. **Erreur de données** :
- Vérifiez que les fichiers de données sont présents dans le dossier `data/raw/`
- Assurez-vous que les données sont au format CSV
- Vérifiez l'encodage (UTF-8 recommandé)
- Validez la structure des colonnes

4. **Erreur de mémoire** :
- Augmentez la limite de mémoire Python :
```bash
export PYTHONMEM=4096
```

### Logs

Les logs sont disponibles dans le dossier `logs/` :
- Format : `segmentation_YYYYMMDD_HHMMSS.log`
- Niveau de détail : INFO, WARNING, ERROR
- Rotation quotidienne des logs
- Conservation : 30 derniers jours

### Sauvegarde

- Les modèles sont sauvegardés dans `models/saved/`
- Sauvegarde automatique toutes les 24h
- Conservation des 5 dernières versions

## Support

Pour toute question ou problème :
1. Consultez la documentation dans le dossier `docs/`
2. Vérifiez les logs dans le dossier `logs/`
3. Consultez les notebooks d'exemple
4. Contactez l'équipe de support :
   - Email : support@tunisietelecom.tn
   - Téléphone : +216 XX XXX XXX

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 