"""
Generate NBA Playoff Predictions using Azure ML Real-Time Endpoint
This script calls your deployed model endpoint to get REAL predictions
"""

import json
import requests
import pandas as pd

# Azure ML Real-Time Endpoint credentials
# Get these from Azure ML Studio: Endpoints → nba-playoff-predictor-endpoint → Consume tab
ENDPOINT_URL = "YOUR_ENDPOINT_URL_HERE"  # Replace with your endpoint URL
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your primary key

# 2025-26 NBA season projected statistics (mid-season, February 2026)
nba_2026_data = [
    # Eastern Conference
    {"Team": "Boston Celtics", "Conference": "Eastern", "Season": 2026, "W": 47.0, "L": 13.0, "ORtg": 121.5, "DRtg": 110.2, "NRtg": 11.3, "Pace": 99.1, "FTr": 0.234, "ThreePAr": 0.481, "TS_Pct": 0.609},
    {"Team": "Cleveland Cavaliers", "Conference": "Eastern", "Season": 2026, "W": 44.0, "L": 16.0, "ORtg": 118.7, "DRtg": 108.5, "NRtg": 10.2, "Pace": 97.8, "FTr": 0.265, "ThreePAr": 0.445, "TS_Pct": 0.597},
    {"Team": "New York Knicks", "Conference": "Eastern", "Season": 2026, "W": 38.0, "L": 22.0, "ORtg": 116.3, "DRtg": 109.8, "NRtg": 6.5, "Pace": 96.4, "FTr": 0.289, "ThreePAr": 0.412, "TS_Pct": 0.584},
    {"Team": "Miami Heat", "Conference": "Eastern", "Season": 2026, "W": 34.0, "L": 26.0, "ORtg": 115.1, "DRtg": 111.3, "NRtg": 3.8, "Pace": 98.2, "FTr": 0.243, "ThreePAr": 0.438, "TS_Pct": 0.578},
    {"Team": "Orlando Magic", "Conference": "Eastern", "Season": 2026, "W": 36.0, "L": 24.0, "ORtg": 112.4, "DRtg": 107.6, "NRtg": 4.8, "Pace": 95.7, "FTr": 0.267, "ThreePAr": 0.391, "TS_Pct": 0.571},
    {"Team": "Milwaukee Bucks", "Conference": "Eastern", "Season": 2026, "W": 33.0, "L": 27.0, "ORtg": 117.8, "DRtg": 113.2, "NRtg": 4.6, "Pace": 99.5, "FTr": 0.251, "ThreePAr": 0.456, "TS_Pct": 0.592},
    {"Team": "Indiana Pacers", "Conference": "Eastern", "Season": 2026, "W": 32.0, "L": 28.0, "ORtg": 119.2, "DRtg": 115.7, "NRtg": 3.5, "Pace": 101.3, "FTr": 0.228, "ThreePAr": 0.467, "TS_Pct": 0.601},
    {"Team": "Philadelphia 76ers", "Conference": "Eastern", "Season": 2026, "W": 24.0, "L": 36.0, "ORtg": 113.5, "DRtg": 114.8, "NRtg": -1.3, "Pace": 97.1, "FTr": 0.273, "ThreePAr": 0.423, "TS_Pct": 0.572},
    {"Team": "Detroit Pistons", "Conference": "Eastern", "Season": 2026, "W": 25.0, "L": 35.0, "ORtg": 111.8, "DRtg": 115.4, "NRtg": -3.6, "Pace": 98.6, "FTr": 0.256, "ThreePAr": 0.401, "TS_Pct": 0.563},
    {"Team": "Atlanta Hawks", "Conference": "Eastern", "Season": 2026, "W": 26.0, "L": 34.0, "ORtg": 116.2, "DRtg": 117.9, "NRtg": -1.7, "Pace": 100.2, "FTr": 0.241, "ThreePAr": 0.449, "TS_Pct": 0.586},
    {"Team": "Chicago Bulls", "Conference": "Eastern", "Season": 2026, "W": 23.0, "L": 37.0, "ORtg": 112.3, "DRtg": 115.6, "NRtg": -3.3, "Pace": 97.9, "FTr": 0.248, "ThreePAr": 0.387, "TS_Pct": 0.569},
    {"Team": "Brooklyn Nets", "Conference": "Eastern", "Season": 2026, "W": 21.0, "L": 39.0, "ORtg": 110.7, "DRtg": 116.2, "NRtg": -5.5, "Pace": 98.8, "FTr": 0.239, "ThreePAr": 0.428, "TS_Pct": 0.559},
    {"Team": "Charlotte Hornets", "Conference": "Eastern", "Season": 2026, "W": 13.0, "L": 47.0, "ORtg": 108.9, "DRtg": 118.4, "NRtg": -9.5, "Pace": 99.7, "FTr": 0.233, "ThreePAr": 0.414, "TS_Pct": 0.551},
    {"Team": "Toronto Raptors", "Conference": "Eastern", "Season": 2026, "W": 15.0, "L": 45.0, "ORtg": 109.5, "DRtg": 117.8, "NRtg": -8.3, "Pace": 96.8, "FTr": 0.261, "ThreePAr": 0.396, "TS_Pct": 0.556},
    {"Team": "Washington Wizards", "Conference": "Eastern", "Season": 2026, "W": 9.0, "L": 51.0, "ORtg": 106.8, "DRtg": 119.7, "NRtg": -12.9, "Pace": 98.3, "FTr": 0.244, "ThreePAr": 0.408, "TS_Pct": 0.544},
    
    # Western Conference
    {"Team": "Oklahoma City Thunder", "Conference": "Western", "Season": 2026, "W": 45.0, "L": 15.0, "ORtg": 119.3, "DRtg": 108.7, "NRtg": 10.6, "Pace": 98.4, "FTr": 0.276, "ThreePAr": 0.429, "TS_Pct": 0.603},
    {"Team": "Houston Rockets", "Conference": "Western", "Season": 2026, "W": 37.0, "L": 23.0, "ORtg": 114.6, "DRtg": 109.3, "NRtg": 5.3, "Pace": 99.8, "FTr": 0.298, "ThreePAr": 0.403, "TS_Pct": 0.579},
    {"Team": "Memphis Grizzlies", "Conference": "Western", "Season": 2026, "W": 39.0, "L": 21.0, "ORtg": 116.8, "DRtg": 110.5, "NRtg": 6.3, "Pace": 100.6, "FTr": 0.287, "ThreePAr": 0.384, "TS_Pct": 0.588},
    {"Team": "Denver Nuggets", "Conference": "Western", "Season": 2026, "W": 35.0, "L": 25.0, "ORtg": 118.4, "DRtg": 112.1, "NRtg": 6.3, "Pace": 97.2, "FTr": 0.258, "ThreePAr": 0.441, "TS_Pct": 0.595},
    {"Team": "Los Angeles Lakers", "Conference": "Western", "Season": 2026, "W": 34.0, "L": 26.0, "ORtg": 115.7, "DRtg": 112.4, "NRtg": 3.3, "Pace": 98.9, "FTr": 0.269, "ThreePAr": 0.418, "TS_Pct": 0.581},
    {"Team": "Dallas Mavericks", "Conference": "Western", "Season": 2026, "W": 33.0, "L": 27.0, "ORtg": 117.9, "DRtg": 113.6, "NRtg": 4.3, "Pace": 97.6, "FTr": 0.245, "ThreePAr": 0.472, "TS_Pct": 0.594},
    {"Team": "Los Angeles Clippers", "Conference": "Western", "Season": 2026, "W": 32.0, "L": 28.0, "ORtg": 114.2, "DRtg": 111.8, "NRtg": 2.4, "Pace": 96.9, "FTr": 0.263, "ThreePAr": 0.435, "TS_Pct": 0.576},
    {"Team": "Golden State Warriors", "Conference": "Western", "Season": 2026, "W": 29.0, "L": 31.0, "ORtg": 113.8, "DRtg": 114.2, "NRtg": -0.4, "Pace": 99.3, "FTr": 0.237, "ThreePAr": 0.489, "TS_Pct": 0.582},
    {"Team": "Minnesota Timberwolves", "Conference": "Western", "Season": 2026, "W": 32.0, "L": 28.0, "ORtg": 112.9, "DRtg": 109.4, "NRtg": 3.5, "Pace": 96.3, "FTr": 0.271, "ThreePAr": 0.425, "TS_Pct": 0.573},
    {"Team": "San Antonio Spurs", "Conference": "Western", "Season": 2026, "W": 28.0, "L": 32.0, "ORtg": 113.4, "DRtg": 114.7, "NRtg": -1.3, "Pace": 99.1, "FTr": 0.252, "ThreePAr": 0.398, "TS_Pct": 0.575},
    {"Team": "Phoenix Suns", "Conference": "Western", "Season": 2026, "W": 30.0, "L": 30.0, "ORtg": 115.3, "DRtg": 114.1, "NRtg": 1.2, "Pace": 97.8, "FTr": 0.249, "ThreePAr": 0.447, "TS_Pct": 0.587},
    {"Team": "Sacramento Kings", "Conference": "Western", "Season": 2026, "W": 27.0, "L": 33.0, "ORtg": 114.8, "DRtg": 116.3, "NRtg": -1.5, "Pace": 100.4, "FTr": 0.256, "ThreePAr": 0.433, "TS_Pct": 0.583},
    {"Team": "Portland Trail Blazers", "Conference": "Western", "Season": 2026, "W": 20.0, "L": 40.0, "ORtg": 110.2, "DRtg": 116.9, "NRtg": -6.7, "Pace": 98.7, "FTr": 0.247, "ThreePAr": 0.421, "TS_Pct": 0.562},
    {"Team": "Utah Jazz", "Conference": "Western", "Season": 2026, "W": 18.0, "L": 42.0, "ORtg": 109.6, "DRtg": 117.4, "NRtg": -7.8, "Pace": 97.4, "FTr": 0.259, "ThreePAr": 0.407, "TS_Pct": 0.558},
    {"Team": "New Orleans Pelicans", "Conference": "Western", "Season": 2026, "W": 16.0, "L": 44.0, "ORtg": 111.3, "DRtg": 118.2, "NRtg": -6.9, "Pace": 99.6, "FTr": 0.268, "ThreePAr": 0.394, "TS_Pct": 0.567},
]

def call_endpoint(data):
    """Call Azure ML endpoint with team data"""
    
    # Prepare the data in Azure ML AutoML expected format
    df = pd.DataFrame(data)
    
    # AutoML endpoints expect this specific format
    payload = {
        "input_data": {
            "columns": list(df.columns),
            "data": df.values.tolist()
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    try:
        response = requests.post(ENDPOINT_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error calling endpoint: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}")
        raise

def generate_predictions():
    """Generate predictions for all 30 NBA teams"""
    
    print("🏀 Calling YOUR deployed Azure ML endpoint...")
    print(f"📍 Endpoint: {ENDPOINT_URL[:50]}...")
    
    # Call the endpoint
    result = call_endpoint(nba_2026_data)
    
    # Extract predictions - AutoML returns array of predictions
    if isinstance(result, list):
        predictions_raw = result
    elif 'result' in result:
        predictions_raw = result['result']
    else:
        # Response might be nested differently
        predictions_raw = result
    
    # Build predictions with real model output
    predictions = []
    for i, team_data in enumerate(nba_2026_data):
        # Get prediction - could be class label or probability
        pred = predictions_raw[i]
        
        # If it's a single value (0 or 1), convert to probability
        if isinstance(pred, (int, float)) and pred in [0, 1]:
            playoff_prob = float(pred)
        # If it's a probability value
        elif isinstance(pred, float):
            playoff_prob = pred
        # If it's an array [prob_no_playoff, prob_playoff]
        elif isinstance(pred, list) and len(pred) == 2:
            playoff_prob = pred[1]
        else:
            playoff_prob = float(pred)
        
        prediction = {
            "team": team_data["Team"],
            "conference": team_data["Conference"],
            "playoffProbability": round(playoff_prob * 100, 1),  # Convert to percentage
            "willMakePlayoffs": playoff_prob >= 0.5,
            "stats": {
                "wins": int(team_data["W"]),
                "losses": int(team_data["L"]),
                "offensiveRating": team_data["ORtg"],
                "defensiveRating": team_data["DRtg"],
                "netRating": team_data["NRtg"]
            }
        }
        predictions.append(prediction)
    
    # Sort by conference and probability
    eastern = sorted([p for p in predictions if p["conference"] == "Eastern"], 
                     key=lambda x: x["playoffProbability"], reverse=True)
    western = sorted([p for p in predictions if p["conference"] == "Western"], 
                     key=lambda x: x["playoffProbability"], reverse=True)
    
    # Assign playoff seeds (top 10 in each conference make play-in/playoffs)
    for i, team in enumerate(eastern[:10], 1):
        team["predictedSeed"] = i
    for i, team in enumerate(western[:10], 1):
        team["predictedSeed"] = i
    
    # Combine all predictions
    all_predictions = eastern + western
    
    # Create output JSON
    output = {
        "modelInfo": {
            "name": "NBA Playoff Predictor",
            "algorithm": "XGBoostClassifier (Azure AutoML)",
            "accuracy": "91.33%",
            "trainingDate": "2026-02-19",
            "predictionDate": "2026-02-19",
            "features": ["W", "L", "ORtg", "DRtg", "NRtg", "Pace", "FTr", "ThreePAr", "TS_Pct"]
        },
        "predictions": all_predictions
    }
    
    # Save to file
    with open('predictions.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n✅ Predictions generated using YOUR trained model endpoint!")
    print(f"\n📊 Eastern Conference: {sum(1 for p in eastern if p['willMakePlayoffs'])} teams making playoffs")
    print(f"📊 Western Conference: {sum(1 for p in western if p['willMakePlayoffs'])} teams making playoffs")
    print(f"\n🏆 Top 3 Eastern: {', '.join([p['team'] for p in eastern[:3]])}")
    print(f"🏆 Top 3 Western: {', '.join([p['team'] for p in western[:3]])}")
    print(f"\n💾 Saved to: predictions.json")

if __name__ == "__main__":
    if "YOUR_ENDPOINT_URL_HERE" in ENDPOINT_URL:
        print("❌ ERROR: Please update ENDPOINT_URL and API_KEY in this script first!")
        print("\nGet these values from Azure ML Studio:")
        print("1. Go to Endpoints → nba-playoff-predictor-endpoint")
        print("2. Click 'Consume' tab")
        print("3. Copy REST endpoint URL and Primary key")
    else:
        generate_predictions()
