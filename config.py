"""
Configuration du projet de segmentation Tunisie Telecom.
"""

from pathlib import Path

# Chemins des dossiers
BASE_PATH = Path(__file__).parent
DATA_PATH = BASE_PATH / 'data'
RAW_DATA_PATH = DATA_PATH / 'raw'
PROCESSED_DATA_PATH = DATA_PATH / 'processed'
FIGURES_PATH = BASE_PATH / 'figures'
REPORTS_PATH = BASE_PATH / 'reports'

# Paramètres de segmentation
N_CLUSTERS = 5
RANDOM_STATE = 42

# Paramètres de clustering
CLUSTERING_PARAMS = {
    'kmeans': {
        'n_clusters': N_CLUSTERS,
        'random_state': RANDOM_STATE,
        'n_init': 10
    },
    'dbscan': {
        'eps': 0.5,
        'min_samples': 5
    }
}

# Paramètres de prétraitement
PREPROCESSING_PARAMS = {
    'numerical_columns': [
        'age',
        'montant_consommation',
        'nombre_appels',
        'volume_data',
        'nombre_sms',
        'duree_abonnement'
    ],
    'categorical_columns': [
        'sexe',
        'zone_geographique',
        'type_client',
        'type_abonnement'
    ]
}

# Paramètres de validation
VALIDATION_PARAMS = {
    'test_size': 0.2,
    'random_state': RANDOM_STATE,
    'cv': 5
}

# Paramètres de visualisation
COLOR_PALETTE = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
SEGMENT_LABELS = [f'Segment {i+1}' for i in range(N_CLUSTERS)]

# Offres commerciales par segment
COMMERCIAL_OFFERS = {
    'Segment 1': {
        'reduction': 0.15,
        'services_additionnels': ['Data Premium', 'VoD', 'Sport'],
        'priorite_support': True
    },
    'Segment 2': {
        'reduction': 0.10,
        'services_additionnels': ['Appels Illimités'],
        'priorite_support': False
    },
    'Segment 3': {
        'reduction': 0.20,
        'services_additionnels': ['Pack Business', 'Support 24/7'],
        'priorite_support': True
    },
    'Segment 4': {
        'reduction': 0.05,
        'services_additionnels': ['Social Media Pack'],
        'priorite_support': False
    },
    'Segment 5': {
        'reduction': 0.25,
        'services_additionnels': ['International Pack', 'Roaming'],
        'priorite_support': True
    }
}

# Seuils des KPIs
KPI_THRESHOLDS = {
    'montant_consommation': {
        'faible': 50,
        'moyen': 200,
        'élevé': 500
    },
    'volume_data': {
        'faible': 5,
        'moyen': 20,
        'élevé': 50
    },
    'nombre_appels': {
        'faible': 20,
        'moyen': 100,
        'élevé': 300
    }
}