// NBA Postseason Oracle - Main Application JavaScript

// Configuration
const PREDICTIONS_URL = './predictions.json'; // Will be hosted in Azure Blob Storage

// Sample fallback data structure (will be replaced by Azure ML predictions)
const fallbackPredictions = {
    "lastUpdated": "2026-02-19T12:00:00Z",
    "modelInfo": {
        "algorithm": "VotingEnsemble",
        "accuracy": 0.89,
        "topFeatures": ["Defensive Rating", "Three Point %", "Win %"]
    },
    "eastern": [
        { "team": "Boston Celtics", "city": "Boston", "probability": 0.95, "wins": 48, "losses": 18 },
        { "team": "Milwaukee Bucks", "city": "Milwaukee", "probability": 0.92, "wins": 46, "losses": 20 },
        { "team": "Philadelphia 76ers", "city": "Philadelphia", "probability": 0.88, "wins": 44, "losses": 22 },
        { "team": "Cleveland Cavaliers", "city": "Cleveland", "probability": 0.85, "wins": 42, "losses": 24 },
        { "team": "New York Knicks", "city": "New York", "probability": 0.78, "wins": 40, "losses": 26 },
        { "team": "Miami Heat", "city": "Miami", "probability": 0.72, "wins": 38, "losses": 28 },
        { "team": "Indiana Pacers", "city": "Indiana", "probability": 0.65, "wins": 36, "losses": 30 },
        { "team": "Orlando Magic", "city": "Orlando", "probability": 0.58, "wins": 34, "losses": 32 },
        { "team": "Atlanta Hawks", "city": "Atlanta", "probability": 0.42, "wins": 32, "losses": 34 },
        { "team": "Chicago Bulls", "city": "Chicago", "probability": 0.38, "wins": 30, "losses": 36 },
        { "team": "Brooklyn Nets", "city": "Brooklyn", "probability": 0.28, "wins": 28, "losses": 38 },
        { "team": "Toronto Raptors", "city": "Toronto", "probability": 0.22, "wins": 26, "losses": 40 },
        { "team": "Charlotte Hornets", "city": "Charlotte", "probability": 0.15, "wins": 24, "losses": 42 },
        { "team": "Washington Wizards", "city": "Washington", "probability": 0.08, "wins": 20, "losses": 46 },
        { "team": "Detroit Pistons", "city": "Detroit", "probability": 0.05, "wins": 18, "losses": 48 }
    ],
    "western": [
        { "team": "Denver Nuggets", "city": "Denver", "probability": 0.96, "wins": 50, "losses": 16 },
        { "team": "Oklahoma City Thunder", "city": "Oklahoma City", "probability": 0.94, "wins": 48, "losses": 18 },
        { "team": "LA Clippers", "city": "Los Angeles", "probability": 0.90, "wins": 46, "losses": 20 },
        { "team": "Phoenix Suns", "city": "Phoenix", "probability": 0.87, "wins": 44, "losses": 22 },
        { "team": "Sacramento Kings", "city": "Sacramento", "probability": 0.81, "wins": 42, "losses": 24 },
        { "team": "Minnesota Timberwolves", "city": "Minnesota", "probability": 0.75, "wins": 40, "losses": 26 },
        { "team": "Dallas Mavericks", "city": "Dallas", "probability": 0.68, "wins": 38, "losses": 28 },
        { "team": "Golden State Warriors", "city": "Golden State", "probability": 0.62, "wins": 36, "losses": 30 },
        { "team": "Los Angeles Lakers", "city": "Los Angeles", "probability": 0.55, "wins": 34, "losses": 32 },
        { "team": "New Orleans Pelicans", "city": "New Orleans", "probability": 0.45, "wins": 32, "losses": 34 },
        { "team": "Houston Rockets", "city": "Houston", "probability": 0.35, "wins": 30, "losses": 36 },
        { "team": "Utah Jazz", "city": "Utah", "probability": 0.25, "wins": 28, "losses": 38 },
        { "team": "Memphis Grizzlies", "city": "Memphis", "probability": 0.18, "wins": 26, "losses": 40 },
        { "team": "Portland Trail Blazers", "city": "Portland", "probability": 0.12, "wins": 22, "losses": 44 },
        { "team": "San Antonio Spurs", "city": "San Antonio", "probability": 0.06, "wins": 18, "losses": 48 }
    ]
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadPredictions();
});

// Load predictions from JSON file
async function loadPredictions() {
    try {
        const response = await fetch(PREDICTIONS_URL);
        
        if (!response.ok) {
            throw new Error('Predictions file not found, using fallback data');
        }
        
        const data = await response.json();
        displayPredictions(data);
    } catch (error) {
        console.log('Loading fallback predictions:', error.message);
        displayPredictions(fallbackPredictions);
    }
}

// Display predictions on the page
function displayPredictions(data) {
    const easternContainer = document.getElementById('eastern-conference');
    const westernContainer = document.getElementById('western-conference');
    
    // Clear loading state
    easternContainer.innerHTML = '';
    westernContainer.innerHTML = '';
    
    // Display Eastern Conference
    data.eastern.forEach(team => {
        const teamCard = createTeamCard(team);
        easternContainer.appendChild(teamCard);
    });
    
    // Display Western Conference
    data.western.forEach(team => {
        const teamCard = createTeamCard(team);
        westernContainer.appendChild(teamCard);
    });
    
    // Update page timestamp if available
    if (data.lastUpdated) {
        updateTimestamp(data.lastUpdated);
    }
}

// Create a team card element
function createTeamCard(team) {
    const card = document.createElement('div');
    card.className = 'team-card';
    
    // Add probability class for styling
    if (team.probability >= 0.70) {
        card.classList.add('high-probability');
    } else if (team.probability >= 0.40) {
        card.classList.add('medium-probability');
    } else {
        card.classList.add('low-probability');
    }
    
    const probabilityPercent = (team.probability * 100).toFixed(1);
    
    card.innerHTML = `
        <div class="team-header">
            <h3>${team.team}</h3>
            <p class="team-info">${team.city}</p>
        </div>
        <div class="probability-bar">
            <div class="probability-fill" style="width: ${probabilityPercent}%"></div>
        </div>
        <p class="probability-text">${probabilityPercent}%</p>
        <div class="team-stats">
            <div class="stat-row">
                <span class="stat-label-small">Record:</span>
                <span class="stat-value">${team.wins}-${team.losses}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label-small">Win %:</span>
                <span class="stat-value">${(team.wins / (team.wins + team.losses) * 100).toFixed(1)}%</span>
            </div>
        </div>
    `;
    
    return card;
}

// Update timestamp display
function updateTimestamp(timestamp) {
    const date = new Date(timestamp);
    const formattedDate = date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    // You can add a timestamp element to your HTML and update it here
    console.log(`Predictions last updated: ${formattedDate}`);
}

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { loadPredictions, displayPredictions, createTeamCard };
}
