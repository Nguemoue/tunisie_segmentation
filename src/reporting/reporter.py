import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os
from datetime import datetime

# Ajout du répertoire parent au PYTHONPATH
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root))

from src.config import (
    NUMERIC_FEATURES,
    CLUSTERS_FILE,
    SEGMENT_LABELS,
    COMMERCIAL_OFFERS,
    KPI_THRESHOLDS,
    REPORTS_DIR
)

class SegmentationReporter:
    """
    Classe pour la génération des rapports de segmentation.
    """
    
    def __init__(self):
        self.features = NUMERIC_FEATURES
        self.output_dir = Path(REPORTS_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.date = datetime.now().strftime("%Y-%m-%d")
    
    def load_data(self, input_file):
        """
        Charge les données segmentées depuis un fichier CSV.
        
        Args:
            input_file (str): Chemin du fichier d'entrée
            
        Returns:
            pd.DataFrame: DataFrame contenant les données segmentées
        """
        return pd.read_csv(input_file)
    
    def generate_executive_summary(self, df):
        """
        Génère un résumé exécutif de la segmentation.
        
        Args:
            df (pd.DataFrame): DataFrame contenant les données segmentées
        """
        # Calcul des statistiques globales
        total_clients = len(df)
        segment_distribution = df['segment_label'].value_counts()
        
        # Calcul des KPIs par segment
        segment_kpis = {}
        for segment in SEGMENT_LABELS.values():
            segment_data = df[df['segment_label'] == segment]
            kpis = {
                'nombre_clients': len(segment_data),
                'pourcentage': len(segment_data) / total_clients * 100,
                'consommation_moyenne': segment_data['consommation_mensuelle'].mean(),
                'satisfaction_moyenne': segment_data['satisfaction'].mean(),
                'fidelite_moyenne': segment_data['fidelite'].mean()
            }
            segment_kpis[segment] = kpis
        
        # Génération du rapport
        report = f"""# Résumé Exécutif de la Segmentation des Clients
Date: {self.date}

## Points Clés
- Nombre total de clients : {total_clients:,}
- Nombre de segments : {len(SEGMENT_LABELS)}

## Distribution des Segments
"""
        
        for segment, kpis in segment_kpis.items():
            report += f"""
### {segment}
- Nombre de clients : {kpis['nombre_clients']:,} ({kpis['pourcentage']:.1f}%)
- Consommation moyenne : {kpis['consommation_moyenne']:.2f} €
- Satisfaction moyenne : {kpis['satisfaction_moyenne']:.2f}/10
- Fidélité moyenne : {kpis['fidelite_moyenne']:.2f}/5
"""
        
        # Ajout des recommandations
        report += """
## Recommandations
1. Fidélisation des clients à risque
   - Mettre en place des programmes de fidélisation ciblés
   - Améliorer le service client pour les segments critiques

2. Optimisation des offres
   - Adapter les offres commerciales selon les profils des segments
   - Développer des promotions personnalisées

3. Suivi des KPIs
   - Surveiller l'évolution de la satisfaction client
   - Mesurer l'impact des actions commerciales
"""
        
        # Sauvegarde du rapport
        output_file = self.output_dir / f'executive_summary_{self.date}.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Résumé exécutif sauvegardé dans {output_file}")
    
    def generate_marketing_strategy(self, df):
        """
        Génère une stratégie marketing basée sur la segmentation.
        
        Args:
            df (pd.DataFrame): DataFrame contenant les données segmentées
        """
        # Analyse des segments
        segment_analysis = {}
        for segment in SEGMENT_LABELS.values():
            segment_data = df[df['segment_label'] == segment]
            analysis = {
                'taille': len(segment_data),
                'pourcentage': len(segment_data) / len(df) * 100,
                'profil': {
                    'age_moyen': segment_data['age'].mean(),
                    'revenu_moyen': segment_data['revenu_mensuel'].mean(),
                    'consommation_moyenne': segment_data['consommation_mensuelle'].mean()
                }
            }
            segment_analysis[segment] = analysis
        
        # Génération du rapport
        report = f"""# Stratégie Marketing par Segment
Date: {self.date}

## Vue d'Ensemble du Marché
- Base totale de clients : {len(df):,}
- Segments identifiés : {len(SEGMENT_LABELS)}

## Analyse des Segments et Stratégies
"""
        
        for segment, analysis in segment_analysis.items():
            report += f"""
### {segment}
#### Profil
- Taille du segment : {analysis['taille']:,} clients ({analysis['pourcentage']:.1f}%)
- Âge moyen : {analysis['profil']['age_moyen']:.1f} ans
- Revenu mensuel moyen : {analysis['profil']['revenu_moyen']:.2f} €
- Consommation mensuelle moyenne : {analysis['profil']['consommation_moyenne']:.2f} €

#### Offre Commerciale
- Nom : {COMMERCIAL_OFFERS[segment]['nom']}
- Description : {COMMERCIAL_OFFERS[segment]['description']}
- Réduction : {COMMERCIAL_OFFERS[segment]['reduction']}
- Avantages : {', '.join(COMMERCIAL_OFFERS[segment]['avantages'])}

#### Stratégie
"""
            
            # Ajout des stratégies spécifiques par segment
            if segment == "Clients Fidèles":
                report += """- Programme de récompenses exclusif
- Communications personnalisées
- Accès prioritaire aux nouveaux services
- Programme de parrainage
"""
            elif segment == "Clients à Risque":
                report += """- Programme de rétention proactif
- Enquêtes de satisfaction régulières
- Offres de reconquête attractives
- Support client dédié
"""
            elif segment == "Clients Premium":
                report += """- Service VIP personnalisé
- Événements exclusifs
- Avantages premium
- Gestion de compte dédiée
"""
            else:  # Clients Occasionnels
                report += """- Offres d'essai attractives
- Programme de découverte des services
- Communications régulières sur les nouveautés
- Incitations à l'utilisation
"""
        
        # Ajout du plan d'action
        report += """
## Plan d'Action

### Court Terme (0-3 mois)
1. Lancement des nouvelles offres commerciales
2. Formation des équipes commerciales
3. Mise en place des outils de suivi

### Moyen Terme (3-6 mois)
1. Évaluation des premiers résultats
2. Ajustement des offres si nécessaire
3. Développement des programmes de fidélisation

### Long Terme (6-12 mois)
1. Analyse complète de l'impact des stratégies
2. Optimisation des segments
3. Développement de nouvelles offres

## Indicateurs de Performance
1. Taux de rétention par segment
2. Évolution du chiffre d'affaires
3. Satisfaction client
4. Taux de conversion des offres
"""
        
        # Sauvegarde du rapport
        output_file = self.output_dir / f'marketing_strategy_{self.date}.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Stratégie marketing sauvegardée dans {output_file}")
    
    def generate_reports(self, input_file):
        """
        Génère tous les rapports.
        
        Args:
            input_file (str): Chemin du fichier d'entrée
        """
        # Chargement des données
        df = self.load_data(input_file)
        
        # Génération des rapports
        self.generate_executive_summary(df)
        self.generate_marketing_strategy(df)

if __name__ == "__main__":
    # Création et utilisation du reporter
    reporter = SegmentationReporter()
    reporter.generate_reports(CLUSTERS_FILE) 