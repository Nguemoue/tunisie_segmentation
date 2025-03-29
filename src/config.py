"""
Configuration du projet de segmentation des clients Tunisie Telecom.
"""

# Chemins des dossiers
DATA_DIR = "data"
RAW_DATA_DIR = f"{DATA_DIR}/raw"
PROCESSED_DATA_DIR = f"{DATA_DIR}/processed"
MODELS_DIR = "models"
REPORTS_DIR = "reports"
VISUALIZATIONS_DIR = "visualizations"

# Fichiers de données
RAW_DATA_FILE = f"{RAW_DATA_DIR}/donnees_clients.csv"
PROCESSED_DATA_FILE = f"{PROCESSED_DATA_DIR}/donnees_pretraitees.csv"
CLUSTERS_FILE = f"{PROCESSED_DATA_DIR}/clusters.csv"

# Caractéristiques des données
NUMERIC_FEATURES = [
    'age',
    'revenu_mensuel',
    'consommation_mensuelle',
    'duree_contrat',
    'nombre_appels',
    'nombre_sms',
    'utilisation_data',
    'satisfaction',
    'fidelite'
]

CATEGORICAL_FEATURES = []

# Paramètres de segmentation
N_CLUSTERS = 4
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

# Seuils des KPIs
KPI_THRESHOLDS = {
    'consommation_min': 100,
    'satisfaction_min': 7,
    'fidelite_min': 3
}

# Labels des segments
SEGMENT_LABELS = {
    0: "Clients Fidèles",
    1: "Clients à Risque",
    2: "Clients Premium",
    3: "Clients Occasionnels"
}

# Offres commerciales par segment
COMMERCIAL_OFFERS = {
    "Clients Fidèles": {
        "nom": "Offre Fidélité Plus",
        "description": "Offre spéciale pour récompenser la fidélité",
        "reduction": "20% sur l'abonnement",
        "avantages": ["Data illimité", "Appels illimités", "SMS illimités"]
    },
    "Clients à Risque": {
        "nom": "Offre Reconquête",
        "description": "Offre attractive pour fidéliser",
        "reduction": "30% sur l'abonnement",
        "avantages": ["Data 10GB", "Appels illimités", "SMS illimités"]
    },
    "Clients Premium": {
        "nom": "Offre Premium",
        "description": "Offre haut de gamme",
        "reduction": "10% sur l'abonnement",
        "avantages": ["Data illimité", "Appels illimités", "SMS illimités", "Support prioritaire"]
    },
    "Clients Occasionnels": {
        "nom": "Offre Découverte",
        "description": "Offre adaptée aux besoins basiques",
        "reduction": "15% sur l'abonnement",
        "avantages": ["Data 5GB", "Appels illimités", "SMS illimités"]
    }
} 