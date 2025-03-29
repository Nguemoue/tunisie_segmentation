"""
Application web pour la visualisation des résultats de segmentation.
"""

import os
from pathlib import Path
from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
from plotly.subplots import make_subplots
import json

from config import (
    RAW_DATA_PATH,
    FIGURES_PATH,
    SEGMENT_LABELS,
    COMMERCIAL_OFFERS
)

app = Flask(__name__)

def load_data():
    """Charge les données brutes."""
    data_path = Path(RAW_DATA_PATH) / 'donnees_clients.csv'
    return pd.read_csv(data_path)

def create_cluster_distribution():
    """Crée le graphique de distribution des clusters."""
    df = load_data()
    # Simulation de segments pour la démonstration
    df['segment'] = pd.qcut(df['montant_consommation'], q=5, labels=SEGMENT_LABELS)
    
    fig = px.pie(
        df,
        names='segment',
        title='Distribution des Segments',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_feature_importance():
    """Crée le graphique d'importance des features."""
    df = load_data()
    # Simulation de segments pour la démonstration
    df['segment'] = pd.qcut(df['montant_consommation'], q=5, labels=SEGMENT_LABELS)
    
    features = ['age', 'montant_consommation', 'nombre_appels', 'volume_data', 'nombre_sms']
    
    fig = go.Figure()
    
    for feature in features:
        fig.add_trace(go.Box(
            y=df[feature],
            x=df['segment'],
            name=feature,
            boxpoints='outliers'
        ))
            
    fig.update_layout(
        height=600,
        title_text="Distribution des Features par Segment",
        xaxis_title="Segment",
        yaxis_title="Valeur",
        showlegend=True,
        boxmode='group'
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_cluster_profiles():
    """Crée le graphique des profils des clusters."""
    df = load_data()
    # Simulation de segments pour la démonstration
    df['segment'] = pd.qcut(df['montant_consommation'], q=5, labels=SEGMENT_LABELS)
    
    features = ['age', 'montant_consommation', 'nombre_appels', 'volume_data', 'nombre_sms']
    
    profiles = df.groupby('segment')[features].mean()
    
    fig = go.Figure()
    
    for segment in profiles.index:
        fig.add_trace(go.Scatterpolar(
            r=profiles.loc[segment],
            theta=features,
            fill='toself',
            name=segment
        ))
        
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, profiles.max().max()])),
        showlegend=True,
        title="Profils des Segments"
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def index():
    """Page d'accueil."""
    return render_template('index.html')

@app.route('/api/cluster_distribution')
def cluster_distribution():
    """API pour la distribution des clusters."""
    return create_cluster_distribution()

@app.route('/api/feature_importance')
def feature_importance():
    """API pour l'importance des features."""
    return create_feature_importance()

@app.route('/api/cluster_profiles')
def cluster_profiles():
    """API pour les profils des clusters."""
    return create_cluster_profiles()

@app.route('/api/segment_details')
def segment_details():
    """API pour les détails des segments."""
    df = load_data()
    # Simulation de segments pour la démonstration
    df['segment'] = pd.qcut(df['montant_consommation'], q=5, labels=SEGMENT_LABELS)
    
    # Colonnes numériques uniquement
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    
    details = {}
    
    for segment in df['segment'].unique():
        segment_data = df[df['segment'] == segment]
        details[str(segment)] = {
            'size': len(segment_data),
            'percentage': len(segment_data) / len(df) * 100,
            'mean_values': segment_data[numeric_columns].mean().to_dict(),
            'offer': COMMERCIAL_OFFERS[segment]
        }
        
    return jsonify(details)

if __name__ == '__main__':
    app.run(debug=True) 