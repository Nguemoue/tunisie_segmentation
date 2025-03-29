// Fonctions utilitaires
function showLoading() {
    document.getElementById('loading').classList.remove('d-none');
}

function hideLoading() {
    document.getElementById('loading').classList.add('d-none');
}

function formatNumber(number) {
    return new Intl.NumberFormat('fr-FR').format(Math.round(number));
}

function formatCurrency(number) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'TND'
    }).format(number);
}

// Chargement des données
async function loadData() {
    showLoading();
    try {
        // Charger les détails des segments
        const response = await fetch('/api/segment_details');
        const segmentDetails = await response.json();
        
        // Mettre à jour les cartes de vue d'ensemble
        updateOverviewCards(segmentDetails);
        
        // Charger et afficher les graphiques
        await loadCharts();
        
        // Mettre à jour le tableau des détails
        updateSegmentDetailsTable(segmentDetails);
    } catch (error) {
        console.error('Erreur lors du chargement des données:', error);
        alert('Une erreur est survenue lors du chargement des données.');
    } finally {
        hideLoading();
    }
}

// Mise à jour des cartes de vue d'ensemble
function updateOverviewCards(segmentDetails) {
    let totalClients = 0;
    let totalAge = 0;
    let totalConsumption = 0;
    
    Object.values(segmentDetails).forEach(segment => {
        totalClients += segment.size;
        totalAge += segment.mean_values.age * segment.size;
        totalConsumption += segment.mean_values.montant_consommation * segment.size;
    });
    
    document.getElementById('total-clients').textContent = formatNumber(totalClients);
    document.getElementById('total-segments').textContent = Object.keys(segmentDetails).length;
    document.getElementById('avg-age').textContent = formatNumber(totalAge / totalClients);
    document.getElementById('avg-consumption').textContent = formatCurrency(totalConsumption / totalClients);
}

// Chargement des graphiques
async function loadCharts() {
    try {
        // Distribution des clusters
        const distributionResponse = await fetch('/api/cluster_distribution');
        const distributionData = await distributionResponse.json();
        Plotly.newPlot('cluster-distribution', distributionData.data, distributionData.layout);
        
        // Importance des features
        const importanceResponse = await fetch('/api/feature_importance');
        const importanceData = await importanceResponse.json();
        Plotly.newPlot('feature-importance', importanceData.data, importanceData.layout);
        
        // Profils des clusters
        const profilesResponse = await fetch('/api/cluster_profiles');
        const profilesData = await profilesResponse.json();
        Plotly.newPlot('cluster-profiles', profilesData.data, profilesData.layout);
    } catch (error) {
        console.error('Erreur lors du chargement des graphiques:', error);
        throw error;
    }
}

// Mise à jour du tableau des détails
function updateSegmentDetailsTable(segmentDetails) {
    const tbody = document.querySelector('#segment-details tbody');
    tbody.innerHTML = '';
    
    Object.entries(segmentDetails).forEach(([segment, details]) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>Segment ${segment}</td>
            <td>${formatNumber(details.size)} (${details.percentage.toFixed(1)}%)</td>
            <td>${formatNumber(details.mean_values.age)}</td>
            <td>${formatCurrency(details.mean_values.montant_consommation)}</td>
            <td>
                <div class="d-flex flex-column">
                    <span class="fw-bold">${details.offer.reduction * 100}% de réduction</span>
                    <small class="text-muted">${details.offer.services_additionnels.join(', ')}</small>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Gestion des événements
document.addEventListener('DOMContentLoaded', () => {
    loadData();
    
    // Rafraîchissement automatique toutes les 5 minutes
    setInterval(loadData, 5 * 60 * 1000);
}); 