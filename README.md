# 🏀 NBA Postseason Oracle - AI-Powered Playoff Predictor

## 🌐 Live Demo
**Website:** https://nbaoraclelc.z12.web.core.windows.net/

## 📊 Project Overview
A data-driven web application that uses Azure Machine Learning to predict which NBA teams will make the playoffs. This project clones the look and feel of NBA.com while integrating artificial intelligence to forecast playoff outcomes using real NBA statistics and Azure's AutoML capabilities.

### Key Features
- **Real-time Predictions**: AI model predicts playoff probabilities for all 30 NBA teams
- **91.33% Accuracy**: XGBoost model trained on 5 seasons of historical data (2021-2025)
- **Azure Integration**: Hosted on Azure Static Web Apps with real-time ML endpoint
- **Automated CI/CD**: GitHub Actions pipeline for continuous deployment

## 🏆 Model Performance
- **Algorithm**: XGBoostClassifier with SparseNormalizer preprocessing
- **Accuracy**: 91.33%
- **Training Data**: 150 records (30 teams × 5 seasons)
- **Training Time**: 19m 14s
- **Features**: W, L, ORtg, DRtg, NRtg, Pace, FTr, ThreePAr, TS_Pct

## 🛠️ Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript
- **Azure ML**: AutoML classification
- **Azure Storage**: Static website hosting
- **Azure Endpoint**: Real-time model inference
- **DevOps**: GitHub Actions CI/CD

## 📁 Project Structure
```
LEBRON_NANG_CLOUD_FINALS/
├── index.html                    # Main website
├── styles.css                    # NBA-themed styling
├── app.js                        # Frontend JavaScript
├── predictions.json              # Live ML predictions
├── nba_historical_data.csv       # Training dataset (150 records)
├── merge_nba_data.py            # Data collection
├── get_endpoint_predictions.py   # Azure ML client
├── .gitignore                    
└── README.md                     
```

## 🚀 Live Resources
- **Website**: https://nbaoraclelc.z12.web.core.windows.net/
- **Storage Account**: nbaoraclelc (Korea Central)
- **ML Workspace**: nba-ml-workspace
- **Endpoint**: nba-playoff-predictor-endpoint

## 💻 Local Development
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/LEBRON_NANG_CLOUD_FINALS.git
cd LEBRON_NANG_CLOUD_FINALS

# Install dependencies
pip install pandas requests

# Generate predictions (requires Azure credentials)
python get_endpoint_predictions.py
```

## 👨‍💻 Author
**Lebron Nang**  
Cloud Computing Final Project  
Date: February 19, 2026
