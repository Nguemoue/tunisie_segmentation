"""
Module de génération de rapports pour le projet de segmentation Tunisie Telecom.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from config import (
    REPORTS_PATH,
    SEGMENT_LABELS,
    COMMERCIAL_OFFERS,
    KPI_THRESHOLDS
)

class SegmentationReporter:
    """Classe pour la génération de rapports de segmentation."""
    
    def __init__(self):
        """Initialise le générateur de rapports."""
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def generate_segment_report(self, profiles: Dict[int, Dict], save: bool = True) -> str:
        """
        Génère un rapport détaillé sur les segments.
        
        Parameters
        ----------
        profiles : Dict[int, Dict]
            Profils des clusters
        save : bool, default=True
            Si True, sauvegarde le rapport
            
        Returns
        -------
        str
            Contenu du rapport
        """
        report = []
        report.append("# Rapport de Segmentation des Clients Tunisie Telecom\n")
        report.append(f"Date de génération : {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        
        # Résumé général
        report.append("## Résumé Général\n")
        total_clients = sum(profile['size'] for profile in profiles.values())
        report.append(f"Nombre total de clients analysés : {total_clients:,}\n")
        
        # Détails par segment
        report.append("## Détails par Segment\n")
        
        for cluster, profile in profiles.items():
            segment_name = SEGMENT_LABELS[cluster]
            report.append(f"### {segment_name}\n")
            
            # Statistiques de base
            report.append(f"- Taille : {profile['size']:,} clients ({profile['percentage']:.1f}%)")
            
            # Caractéristiques principales
            report.append("\nCaractéristiques principales :")
            for feature, value in profile['mean_values'].items():
                report.append(f"- {feature}: {value:.2f}")
                
            # Features clés
            report.append("\nFeatures clés :")
            for feature, importance in profile['key_features'].items():
                report.append(f"- {feature}: {importance:.2f}")
                
            # Offre commerciale
            offer = COMMERCIAL_OFFERS[segment_name]
            report.append("\nOffre commerciale :")
            report.append(f"- Réduction : {offer['reduction']*100:.0f}%")
            if offer['services_additionnels']:
                report.append(f"- Services additionnels : {', '.join(offer['services_additionnels'])}")
            report.append(f"- Support prioritaire : {'Oui' if offer['priorite_support'] else 'Non'}")
            
            report.append("\n---\n")
            
        # Analyse des KPIs
        report.append("## Analyse des KPIs\n")
        report.append("### Seuils de Performance\n")
        for kpi, thresholds in KPI_THRESHOLDS.items():
            report.append(f"\n{kpi} :")
            for niveau, seuil in thresholds.items():
                report.append(f"- {niveau}: {seuil}")
            
        # Recommandations
        report.append("\n## Recommandations\n")
        report.append("### Actions Prioritaires\n")
        
        # Recommandations basées sur les segments
        for cluster, profile in profiles.items():
            segment_name = SEGMENT_LABELS[cluster]
            if profile['percentage'] < 10:
                report.append(f"- Développer des actions ciblées pour le segment {segment_name}")
            if profile['percentage'] > 30:
                report.append(f"- Optimiser les ressources pour le segment {segment_name}")
                
        # Recommandations marketing
        report.append("\n### Stratégies Marketing\n")
        report.append("- Personnaliser les communications par segment")
        report.append("- Adapter les offres promotionnelles selon les profils")
        report.append("- Mettre en place un suivi des performances par segment")
        
        # Conclusion
        report.append("\n## Conclusion\n")
        report.append("Cette segmentation permet d'identifier clairement les différents profils de clients")
        report.append("et d'adapter les stratégies marketing en conséquence.")
        
        report_content = "\n".join(report)
        
        if save:
            Path(REPORTS_PATH).mkdir(parents=True, exist_ok=True)
            report_path = Path(REPORTS_PATH) / f"rapport_segmentation_{self.timestamp}.md"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"Rapport sauvegardé dans {report_path}")
            
        return report_content
        
    def generate_executive_summary(self, profiles: Dict[int, Dict], save: bool = True) -> str:
        """
        Génère un résumé exécutif de la segmentation.
        
        Parameters
        ----------
        profiles : Dict[int, Dict]
            Profils des clusters
        save : bool, default=True
            Si True, sauvegarde le résumé
            
        Returns
        -------
        str
            Contenu du résumé
        """
        summary = []
        summary.append("# Résumé Exécutif - Segmentation Clients Tunisie Telecom\n")
        summary.append(f"Date : {datetime.now().strftime('%d/%m/%Y')}\n")
        
        # Vue d'ensemble
        summary.append("## Vue d'Ensemble\n")
        total_clients = sum(profile['size'] for profile in profiles.values())
        summary.append(f"Nombre total de clients : {total_clients:,}\n")
        
        # Distribution des segments
        summary.append("## Distribution des Segments\n")
        for cluster, profile in profiles.items():
            segment_name = SEGMENT_LABELS[cluster]
            summary.append(f"- {segment_name}: {profile['percentage']:.1f}%")
            
        # Points clés
        summary.append("\n## Points Clés\n")
        
        # Segment le plus important
        largest_segment = max(profiles.items(), key=lambda x: x[1]['size'])
        summary.append(f"- Segment dominant : {SEGMENT_LABELS[largest_segment[0]]} ({largest_segment[1]['percentage']:.1f}%)")
        
        # Opportunités
        summary.append("\n## Opportunités\n")
        for cluster, profile in profiles.items():
            segment_name = SEGMENT_LABELS[cluster]
            offer = COMMERCIAL_OFFERS[segment_name]
            if offer['reduction'] > 0.1:
                summary.append(f"- Potentiel de fidélisation important pour le segment {segment_name}")
                
        # Actions recommandées
        summary.append("\n## Actions Recommandées\n")
        summary.append("1. Développer des offres personnalisées par segment")
        summary.append("2. Mettre en place un suivi des performances")
        summary.append("3. Adapter les stratégies de communication")
        
        summary_content = "\n".join(summary)
        
        if save:
            Path(REPORTS_PATH).mkdir(parents=True, exist_ok=True)
            summary_path = Path(REPORTS_PATH) / f"resume_executif_{self.timestamp}.md"
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            print(f"Résumé exécutif sauvegardé dans {summary_path}")
            
        return summary_content
        
    def generate_marketing_strategy(self, profiles: Dict[int, Dict], save: bool = True) -> str:
        """
        Génère une stratégie marketing basée sur la segmentation.
        
        Parameters
        ----------
        profiles : Dict[int, Dict]
            Profils des clusters
        save : bool, default=True
            Si True, sauvegarde la stratégie
            
        Returns
        -------
        str
            Contenu de la stratégie
        """
        strategy = []
        strategy.append("# Stratégie Marketing - Segmentation Clients Tunisie Telecom\n")
        strategy.append(f"Date : {datetime.now().strftime('%d/%m/%Y')}\n")
        
        # Objectifs
        strategy.append("## Objectifs\n")
        strategy.append("- Augmenter la fidélisation des clients")
        strategy.append("- Optimiser les campagnes marketing")
        strategy.append("- Améliorer la satisfaction client")
        
        # Stratégies par segment
        strategy.append("\n## Stratégies par Segment\n")
        
        for cluster, profile in profiles.items():
            segment_name = SEGMENT_LABELS[cluster]
            offer = COMMERCIAL_OFFERS[segment_name]
            
            strategy.append(f"### {segment_name}\n")
            strategy.append(f"Taille : {profile['percentage']:.1f}% des clients\n")
            
            # Caractéristiques clés
            strategy.append("Caractéristiques clés :")
            for feature, value in profile['mean_values'].items():
                strategy.append(f"- {feature}: {value:.2f}")
                
            # Stratégie spécifique
            strategy.append("\nStratégie :")
            if offer['reduction'] > 0.1:
                strategy.append("- Focus sur la fidélisation via des offres exclusives")
            if offer['services_additionnels']:
                strategy.append("- Promouvoir les services additionnels")
            if offer['priorite_support']:
                strategy.append("- Mettre en avant le support prioritaire")
                
            strategy.append("\n---\n")
            
        # Plan d'action
        strategy.append("\n## Plan d'Action\n")
        strategy.append("### Court terme (1-3 mois)\n")
        strategy.append("1. Mettre en place les offres personnalisées")
        strategy.append("2. Adapter les communications par segment")
        strategy.append("3. Former l'équipe commerciale")
        
        strategy.append("\n### Moyen terme (3-6 mois)\n")
        strategy.append("1. Évaluer l'impact des actions")
        strategy.append("2. Ajuster les stratégies selon les résultats")
        strategy.append("3. Développer de nouveaux services")
        
        strategy.append("\n### Long terme (6-12 mois)\n")
        strategy.append("1. Optimiser la segmentation")
        strategy.append("2. Développer des partenariats stratégiques")
        strategy.append("3. Mettre en place un système de suivi automatisé")
        
        strategy_content = "\n".join(strategy)
        
        if save:
            Path(REPORTS_PATH).mkdir(parents=True, exist_ok=True)
            strategy_path = Path(REPORTS_PATH) / f"strategie_marketing_{self.timestamp}.md"
            with open(strategy_path, 'w', encoding='utf-8') as f:
                f.write(strategy_content)
            print(f"Stratégie marketing sauvegardée dans {strategy_path}")
            
        return strategy_content 