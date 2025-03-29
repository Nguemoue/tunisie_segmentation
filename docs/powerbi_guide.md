# Guide de Visualisation Power BI pour la Segmentation des Clients

## 1. Préparation des Données

### 1.1 Import des Données
1. Ouvrez Power BI Desktop
2. Cliquez sur "Obtenir les données"
3. Sélectionnez "CSV"
4. Naviguez vers le dossier `data/powerbi`
5. Importez les trois fichiers suivants :
   - clients.csv
   - segment_stats.csv
   - offres_commerciales.csv

### 1.2 Relations entre les Tables
1. Dans la vue "Relations", créez les relations suivantes :
   - clients.segment → offres_commerciales.segment
   - clients.segment → segment_stats.segment

## 2. Création des Visualisations

### 2.1 Page d'Accueil
1. Créez un titre "Tableau de Bord de Segmentation des Clients"
2. Ajoutez les KPIs suivants :
   - Nombre total de clients
   - Nombre de segments
   - Consommation moyenne
   - Nombre moyen d'appels

### 2.2 Distribution des Segments
1. Créez un graphique en camembert :
   - Valeurs : nombre_clients
   - Légende : segment
   - Titre : "Distribution des Segments"
   - Ajoutez des pourcentages dans les étiquettes

### 2.3 Profils des Segments
1. Créez un graphique radar :
   - Valeurs : consommation_moyenne, appels_moyens, data_moyenne, sms_moyens
   - Catégories : segment
   - Titre : "Profils des Segments"

### 2.4 Analyse des Caractéristiques
1. Créez un graphique en boîte :
   - Axe Y : montant_consommation, nombre_appels, volume_data, nombre_sms
   - Axe X : segment
   - Titre : "Distribution des Caractéristiques par Segment"

### 2.5 Offres Commerciales
1. Créez un tableau :
   - Colonnes : segment, nom_offre, description, prix
   - Titre : "Offres Commerciales par Segment"

## 3. Personnalisation

### 3.1 Thème
1. Appliquez un thème cohérent avec l'identité visuelle de Tunisie Telecom
2. Utilisez des couleurs distinctes pour chaque segment

### 3.2 Filtres
1. Ajoutez des filtres pour :
   - Segment
   - Tranche d'âge
   - Niveau de consommation

### 3.3 Interactions
1. Configurez les interactions entre les visualisations
2. Ajoutez des infobulles détaillées

## 4. Publication et Partage

### 4.1 Publication
1. Cliquez sur "Publier"
2. Sélectionnez votre espace de travail Power BI
3. Attendez la fin de la publication

### 4.2 Partage
1. Configurez les permissions d'accès
2. Partagez le tableau de bord avec les utilisateurs concernés

## 5. Maintenance

### 5.1 Actualisation des Données
1. Configurez l'actualisation automatique
2. Testez l'actualisation manuelle

### 5.2 Mises à Jour
1. Documentez les modifications
2. Testez les changements avant la publication

## 6. Bonnes Pratiques

1. Gardez les visualisations simples et claires
2. Utilisez des titres explicites
3. Ajoutez des légendes quand nécessaire
4. Maintenez une cohérence visuelle
5. Optimisez les performances 