"""
Module de gestion de la base de données SQL.
"""

import sqlite3
import pandas as pd
from pathlib import Path
import os

class DatabaseManager:
    def __init__(self, db_path='data/telecom.db'):
        """Initialise la connexion à la base de données."""
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        """Crée les tables nécessaires si elles n'existent pas."""
        cursor = self.conn.cursor()
        
        # Table des clients
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            montant_consommation FLOAT,
            nombre_appels INTEGER,
            volume_data FLOAT,
            nombre_sms INTEGER,
            segment TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Table des offres commerciales
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS offres_commerciales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            segment TEXT,
            nom_offre TEXT,
            description TEXT,
            prix FLOAT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.conn.commit()
    
    def import_data(self, csv_path):
        """Importe les données depuis un fichier CSV."""
        df = pd.read_csv(csv_path)
        df.to_sql('clients', self.conn, if_exists='replace', index=False)
        print(f"Données importées avec succès depuis {csv_path}")
    
    def get_client_data(self):
        """Récupère toutes les données des clients."""
        return pd.read_sql_query("SELECT * FROM clients", self.conn)
    
    def get_segment_stats(self):
        """Récupère les statistiques par segment."""
        query = '''
        SELECT 
            segment,
            COUNT(*) as nombre_clients,
            AVG(montant_consommation) as consommation_moyenne,
            AVG(nombre_appels) as appels_moyens,
            AVG(volume_data) as data_moyenne,
            AVG(nombre_sms) as sms_moyens
        FROM clients
        GROUP BY segment
        '''
        return pd.read_sql_query(query, self.conn)
    
    def add_commercial_offer(self, segment, nom_offre, description, prix):
        """Ajoute une offre commerciale."""
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO offres_commerciales (segment, nom_offre, description, prix)
        VALUES (?, ?, ?, ?)
        ''', (segment, nom_offre, description, prix))
        self.conn.commit()
    
    def get_commercial_offers(self):
        """Récupère toutes les offres commerciales."""
        return pd.read_sql_query("SELECT * FROM offres_commerciales", self.conn)
    
    def export_to_csv(self, table_name, output_path):
        """Exporte une table vers un fichier CSV."""
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
        df.to_csv(output_path, index=False)
        print(f"Données exportées avec succès vers {output_path}")
    
    def close(self):
        """Ferme la connexion à la base de données."""
        self.conn.close() 