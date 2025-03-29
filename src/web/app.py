"""
Application web pour la visualisation des résultats de segmentation.
"""

import os
from pathlib import Path
from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

from config import (
    PROCESSED_DATA_PATH,
    FIGURES_PATH,
    SEGMENT_LABELS,
    COMMERCIAL_OFFERS
)

app = Flask(__name__)

def load_data():
    """Charge les données prétraitées."""
    data_path = Path(PROCESSED_DATA_PATH) / 'donnees_pretraitees.csv'
    return pd.read_csv(data_path)

def create_cluster_distribution():
    """Crée le graphique de distribution des clusters."""
    df = load_data()
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
    features = ['age', 'montant_consommation', 'nombre_appels', 'volume_data', 'nombre_sms']
    
    fig = make_subplots(rows=2, cols=2, subplot_titles=features)
    
    for i, feature in enumerate(features, 1):
        row = (i-1) // 2 + 1
        col = (i-1) % 2 + 1
        
        for segment in df['segment'].unique():
            segment_data = df[df['segment'] == segment]
            fig.add_trace(
                go.Box(
                    y=segment_data[feature],
                    name=f'Segment {segment}',
                    boxpoints='outliers',
                    showlegend=(i == 1)
                ),
                row=row, col=col
            )
            
    fig.update_layout(height=800, title_text="Distribution des Features par Segment")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_cluster_profiles():
    """Crée le graphique des profils des clusters."""
    df = load_data()
    features = ['age', 'montant_consommation', 'nombre_appels', 'volume_data', 'nombre_sms']
    
    profiles = df.groupby('segment')[features].mean()
    
    fig = go.Figure()
    
    for segment in profiles.index:
        fig.add_trace(go.Scatterpolar(
            r=profiles.loc[segment],
            theta=features,
            fill='toself',
            name=f'Segment {segment}'
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
    details = {}
    
    for segment in df['segment'].unique():
        segment_data = df[df['segment'] == segment]
        details[segment] = {
            'size': len(segment_data),
            'percentage': len(segment_data) / len(df) * 100,
            'mean_values': segment_data.mean().to_dict(),
            'offer': COMMERCIAL_OFFERS[SEGMENT_LABELS[segment]]
        }
        
    return jsonify(details)

if __name__ == '__main__':
    app.run(debug=True) 