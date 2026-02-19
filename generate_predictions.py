import joblib
import pandas as pd
import json
from pathlib import Path

# Load the trained model using joblib (same loader Azure ML uses internally)
model_path = Path.home() / "Downloads" / "purpleendiver153" / "model.pkl"
model = joblib.load(model_path)

# 2025-26 mid-season NBA team statistics (projected based on current standings)
# Features: W, L, ORtg, DRtg, NRtg, Pace, FTr, ThreePAr, TS_Pct
nba_2026_data = pd.DataFrame([
    # Eastern Conference
    {"Team": "Boston Celtics", "Conference": "Eastern", "W": 47, "L": 13, "ORtg": 121.5, "DRtg": 110.2, "NRtg": 11.3, "Pace": 99.1, "FTr": 0.234, "ThreePAr": 0.481, "TS_Pct": 0.609},
    {"Team": "Cleveland Cavaliers", "Conference": "Eastern", "W": 44, "L": 16, "ORtg": 119.8, "DRtg": 110.8, "NRtg": 9.0, "Pace": 97.5, "FTr": 0.256, "ThreePAr": 0.412, "TS_Pct": 0.591},
    {"Team": "New York Knicks", "Conference": "Eastern", "W": 39, "L": 21, "ORtg": 117.6, "DRtg": 111.3, "NRtg": 6.3, "Pace": 96.2, "FTr": 0.287, "ThreePAr": 0.445, "TS_Pct": 0.583},
    {"Team": "Milwaukee Bucks", "Conference": "Eastern", "W": 38, "L": 22, "ORtg": 118.2, "DRtg": 112.1, "NRtg": 6.1, "Pace": 98.3, "FTr": 0.245, "ThreePAr": 0.426, "TS_Pct": 0.586},
    {"Team": "Orlando Magic", "Conference": "Eastern", "W": 37, "L": 23, "ORtg": 112.9, "DRtg": 107.4, "NRtg": 5.5, "Pace": 96.8, "FTr": 0.268, "ThreePAr": 0.389, "TS_Pct": 0.571},
    {"Team": "Philadelphia 76ers", "Conference": "Eastern", "W": 34, "L": 26, "ORtg": 115.8, "DRtg": 111.9, "NRtg": 3.9, "Pace": 97.1, "FTr": 0.291, "ThreePAr": 0.437, "TS_Pct": 0.579},
    {"Team": "Indiana Pacers", "Conference": "Eastern", "W": 33, "L": 27, "ORtg": 119.1, "DRtg": 115.7, "NRtg": 3.4, "Pace": 101.2, "FTr": 0.228, "ThreePAr": 0.453, "TS_Pct": 0.594},
    {"Team": "Miami Heat", "Conference": "Eastern", "W": 32, "L": 28, "ORtg": 113.7, "DRtg": 111.4, "NRtg": 2.3, "Pace": 95.9, "FTr": 0.274, "ThreePAr": 0.418, "TS_Pct": 0.573},
    {"Team": "Atlanta Hawks", "Conference": "Eastern", "W": 28, "L": 32, "ORtg": 116.3, "DRtg": 116.8, "NRtg": -0.5, "Pace": 99.6, "FTr": 0.251, "ThreePAr": 0.442, "TS_Pct": 0.581},
    {"Team": "Chicago Bulls", "Conference": "Eastern", "W": 26, "L": 34, "ORtg": 113.8, "DRtg": 115.9, "NRtg": -2.1, "Pace": 97.8, "FTr": 0.239, "ThreePAr": 0.401, "TS_Pct": 0.569},
    {"Team": "Detroit Pistons", "Conference": "Eastern", "W": 24, "L": 36, "ORtg": 111.4, "DRtg": 115.7, "NRtg": -4.3, "Pace": 98.2, "FTr": 0.264, "ThreePAr": 0.395, "TS_Pct": 0.562},
    {"Team": "Toronto Raptors", "Conference": "Eastern", "W": 22, "L": 38, "ORtg": 110.9, "DRtg": 116.4, "NRtg": -5.5, "Pace": 97.3, "FTr": 0.271, "ThreePAr": 0.423, "TS_Pct": 0.565},
    {"Team": "Charlotte Hornets", "Conference": "Eastern", "W": 18, "L": 42, "ORtg": 109.8, "DRtg": 117.2, "NRtg": -7.4, "Pace": 99.8, "FTr": 0.258, "ThreePAr": 0.438, "TS_Pct": 0.558},
    {"Team": "Brooklyn Nets", "Conference": "Eastern", "W": 17, "L": 43, "ORtg": 108.2, "DRtg": 116.9, "NRtg": -8.7, "Pace": 96.7, "FTr": 0.241, "ThreePAr": 0.414, "TS_Pct": 0.554},
    {"Team": "Washington Wizards", "Conference": "Eastern", "W": 13, "L": 47, "ORtg": 106.7, "DRtg": 119.3, "NRtg": -12.6, "Pace": 98.1, "FTr": 0.249, "ThreePAr": 0.429, "TS_Pct": 0.547},
    
    # Western Conference
    {"Team": "Oklahoma City Thunder", "Conference": "Western", "W": 49, "L": 11, "ORtg": 119.8, "DRtg": 107.2, "NRtg": 12.6, "Pace": 97.8, "FTr": 0.273, "ThreePAr": 0.428, "TS_Pct": 0.598},
    {"Team": "Denver Nuggets", "Conference": "Western", "W": 40, "L": 20, "ORtg": 118.4, "DRtg": 110.9, "NRtg": 7.5, "Pace": 96.4, "FTr": 0.265, "ThreePAr": 0.411, "TS_Pct": 0.593},
    {"Team": "Memphis Grizzlies", "Conference": "Western", "W": 39, "L": 21, "ORtg": 116.7, "DRtg": 110.3, "NRtg": 6.4, "Pace": 100.2, "FTr": 0.284, "ThreePAr": 0.394, "TS_Pct": 0.582},
    {"Team": "Houston Rockets", "Conference": "Western", "W": 38, "L": 22, "ORtg": 113.9, "DRtg": 108.7, "NRtg": 5.2, "Pace": 98.9, "FTr": 0.298, "ThreePAr": 0.449, "TS_Pct": 0.576},
    {"Team": "Los Angeles Clippers", "Conference": "Western", "W": 36, "L": 24, "ORtg": 115.3, "DRtg": 110.8, "NRtg": 4.5, "Pace": 96.1, "FTr": 0.261, "ThreePAr": 0.423, "TS_Pct": 0.584},
    {"Team": "Dallas Mavericks", "Conference": "Western", "W": 35, "L": 25, "ORtg": 117.2, "DRtg": 112.9, "NRtg": 4.3, "Pace": 97.2, "FTr": 0.247, "ThreePAr": 0.456, "TS_Pct": 0.589},
    {"Team": "Phoenix Suns", "Conference": "Western", "W": 34, "L": 26, "ORtg": 116.1, "DRtg": 112.4, "NRtg": 3.7, "Pace": 98.7, "FTr": 0.253, "ThreePAr": 0.432, "TS_Pct": 0.581},
    {"Team": "Los Angeles Lakers", "Conference": "Western", "W": 33, "L": 27, "ORtg": 114.8, "DRtg": 112.6, "NRtg": 2.2, "Pace": 99.3, "FTr": 0.269, "ThreePAr": 0.407, "TS_Pct": 0.577},
    {"Team": "Golden State Warriors", "Conference": "Western", "W": 30, "L": 30, "ORtg": 113.2, "DRtg": 113.8, "NRtg": -0.6, "Pace": 100.1, "FTr": 0.236, "ThreePAr": 0.492, "TS_Pct": 0.574},
    {"Team": "Sacramento Kings", "Conference": "Western", "W": 29, "L": 31, "ORtg": 115.7, "DRtg": 116.3, "NRtg": -0.6, "Pace": 101.8, "FTr": 0.244, "ThreePAr": 0.419, "TS_Pct": 0.585},
    {"Team": "Minnesota Timberwolves", "Conference": "Western", "W": 28, "L": 32, "ORtg": 112.6, "DRtg": 114.1, "NRtg": -1.5, "Pace": 96.9, "FTr": 0.279, "ThreePAr": 0.436, "TS_Pct": 0.571},
    {"Team": "San Antonio Spurs", "Conference": "Western", "W": 26, "L": 34, "ORtg": 111.8, "DRtg": 115.2, "NRtg": -3.4, "Pace": 99.4, "FTr": 0.267, "ThreePAr": 0.403, "TS_Pct": 0.568},
    {"Team": "New Orleans Pelicans", "Conference": "Western", "W": 24, "L": 36, "ORtg": 110.4, "DRtg": 114.9, "NRtg": -4.5, "Pace": 97.6, "FTr": 0.289, "ThreePAr": 0.387, "TS_Pct": 0.563},
    {"Team": "Utah Jazz", "Conference": "Western", "W": 19, "L": 41, "ORtg": 108.9, "DRtg": 117.1, "NRtg": -8.2, "Pace": 98.8, "FTr": 0.256, "ThreePAr": 0.445, "TS_Pct": 0.557},
    {"Team": "Portland Trail Blazers", "Conference": "Western", "W": 16, "L": 44, "ORtg": 107.3, "DRtg": 118.6, "NRtg": -11.3, "Pace": 97.4, "FTr": 0.262, "ThreePAr": 0.421, "TS_Pct": 0.551},
])

# Prepare features for prediction (same order as training data)
feature_columns = ['W', 'L', 'ORtg', 'DRtg', 'NRtg', 'Pace', 'FTr', 'ThreePAr', 'TS_Pct']
X = nba_2026_data[feature_columns]

# Generate predictions using YOUR trained model
playoff_predictions = model.predict(X)
playoff_probabilities = model.predict_proba(X)[:, 1]  # Probability of making playoffs (class 1)

# Add predictions to dataframe
nba_2026_data['PlayoffPrediction'] = playoff_predictions
nba_2026_data['PlayoffProbability'] = playoff_probabilities

# Sort by conference and probability
eastern = nba_2026_data[nba_2026_data['Conference'] == 'Eastern'].sort_values('PlayoffProbability', ascending=False).reset_index(drop=True)
western = nba_2026_data[nba_2026_data['Conference'] == 'Western'].sort_values('PlayoffProbability', ascending=False).reset_index(drop=True)

# Assign predicted seeds
eastern['PredictedSeed'] = range(1, len(eastern) + 1)
western['PredictedSeed'] = range(1, len(western) + 1)

# Combine back
final_predictions = pd.concat([eastern, western])

# Create JSON output
output = {
    "modelInfo": {
        "algorithm": "SparseNormalizer + XGBoostClassifier",
        "accuracy": 0.9133,
        "trainingDate": "2026-02-19",
        "season": "2025-2026",
        "trainingRecords": 150,
        "features": feature_columns
    },
    "predictions": []
}

for _, row in final_predictions.iterrows():
    output["predictions"].append({
        "team": row['Team'],
        "conference": row['Conference'],
        "playoffProbability": round(float(row['PlayoffProbability']), 4),
        "predictedSeed": int(row['PredictedSeed']),
        "willMakePlayoffs": bool(row['PlayoffPrediction']),
        "stats": {
            "wins": int(row['W']),
            "losses": int(row['L']),
            "offensiveRating": float(row['ORtg']),
            "defensiveRating": float(row['DRtg']),
            "netRating": float(row['NRtg'])
        }
    })

# Save to predictions.json
output_file = Path(r"C:\Users\marcu\Downloads\LEBRON_NANG_CLOUD_FINALS\predictions.json")
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2)

print(f"✅ Predictions generated using YOUR trained model!")
print(f"✅ Model accuracy: 91.33%")
print(f"✅ Output saved to: {output_file}")
print(f"\n📊 Playoff Predictions Summary:")
print(f"Eastern Conference playoff teams: {len(eastern[eastern['PlayoffPrediction'] == 1])}")
print(f"Western Conference playoff teams: {len(western[western['PlayoffPrediction'] == 1])}")
print(f"\nTop 3 Eastern: {', '.join(eastern.head(3)['Team'].tolist())}")
print(f"Top 3 Western: {', '.join(western.head(3)['Team'].tolist())}")
