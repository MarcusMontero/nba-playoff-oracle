const PREDICTIONS_URL = './predictions.json';


document.addEventListener('DOMContentLoaded', () => {
    loadPredictions();
});


async function loadPredictions() {
    try {
        const response = await fetch(PREDICTIONS_URL);
        
        if (!response.ok) {
            throw new Error('Predictions file not found');
        }
        
        const data = await response.json();
        console.log('Predictions loaded');
        displayPredictions(data);
    } catch (error) {
        console.error('Error loading predictions:', error.message);
        const divisions = ['atlantic-division', 'central-division', 'southeast-division', 
                          'northwest-division', 'pacific-division', 'southwest-division'];
        divisions.forEach(divId => {
            const container = document.getElementById(divId);
            if (container) {
                container.innerHTML = '<tr><td colspan="5" class="error-message">Error loading predictions. Please refresh the page.</td></tr>';
            }
        });
    }
}


function displayPredictions(data) {
    const divisionContainers = {
        'Atlantic': document.getElementById('atlantic-division'),
        'Central': document.getElementById('central-division'),
        'Southeast': document.getElementById('southeast-division'),
        'Northwest': document.getElementById('northwest-division'),
        'Pacific': document.getElementById('pacific-division'),
        'Southwest': document.getElementById('southwest-division')
    };
    
    Object.values(divisionContainers).forEach(container => {
        if (container) container.innerHTML = '';
    });
    
    if (data.predictions) {
        const divisionTeams = {
            'Atlantic': [],
            'Central': [],
            'Southeast': [],
            'Northwest': [],
            'Pacific': [],
            'Southwest': []
        };
        
        data.predictions.forEach(team => {
            const division = team.division;
            if (division && divisionTeams[division]) {
                divisionTeams[division].push({
                    team: team.team,
                    probability: team.playoffProbability / 100,
                    wins: team.stats.wins,
                    losses: team.stats.losses
                });
            }
        });
        
        Object.keys(divisionTeams).forEach(division => {
            divisionTeams[division].sort((a, b) => b.probability - a.probability);
            
            const container = divisionContainers[division];
            if (container) {
                divisionTeams[division].forEach((team, index) => {
                    const teamRow = createTeamRow(team, index + 1);
                    container.appendChild(teamRow);
                });
            }
        });
    }
    
    if (data.modelInfo) {
        console.log(`Model: ${data.modelInfo.algorithm}, Accuracy: ${data.modelInfo.accuracy}`);
    }
    if (data.lastUpdated) {
        updateTimestamp(data.lastUpdated);
    }
}

function createTeamRow(team, rank) {
    const row = document.createElement('tr');
    
    if (team.probability >= 0.70) {
        row.classList.add('high-probability');
    } else if (team.probability >= 0.40) {
        row.classList.add('medium-probability');
    } else {
        row.classList.add('low-probability');
    }
    
    const probabilityPercent = (team.probability * 100).toFixed(1);
    
    row.innerHTML = `
        <td>${rank}</td>
        <td class="team-name">${team.team}</td>
        <td class="team-record">${team.wins}-${team.losses}</td>
        <td class="probability-value">${probabilityPercent}%</td>
        <td>
            <div class="probability-bar-container">
                <div class="probability-bar-fill" data-width="${probabilityPercent}">
                    <span class="probability-bar-text">${probabilityPercent}%</span>
                </div>
            </div>
        </td>
    `;
    
    return row;
}

function updateTimestamp(timestamp) {
    const date = new Date(timestamp);
    const formattedDate = date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    console.log(`Predictions last updated: ${formattedDate}`);
}

function animateProbabilityBars() {
    setTimeout(() => {
        const bars = document.querySelectorAll('.probability-bar-fill');
        bars.forEach(bar => {
            const width = bar.getAttribute('data-width');
            bar.style.width = width + '%';
        });
    }, 100);
}

const originalDisplayPredictions = displayPredictions;
displayPredictions = function(data) {
    originalDisplayPredictions(data);
    animateProbabilityBars();
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { loadPredictions, displayPredictions, createTeamRow };
}
