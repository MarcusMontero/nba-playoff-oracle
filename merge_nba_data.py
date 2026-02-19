"""
NBA Historical Data Merger
Combines 5 seasons of real Basketball Reference data into ML training dataset
Data Source: Basketball-Reference.com (Sports Reference LLC)
Seasons: 2020-21, 2021-22, 2022-23, 2023-24, 2024-25
"""
import pandas as pd
import re

# Define the season files to merge
import os
downloads_folder = r'C:\Users\marcu\Downloads'

season_files = [
    (os.path.join(downloads_folder, 'nba_2021_advanced.csv'), 2021),
    (os.path.join(downloads_folder, 'nba_2022_advanced.csv'), 2022),
    (os.path.join(downloads_folder, 'nba_2023_advanced.csv'), 2023),
    (os.path.join(downloads_folder, 'nba_2024_advanced.csv'), 2024),
    (os.path.join(downloads_folder, 'nba_2025_advanced.csv'), 2025)
]

# List to hold all processed dataframes
all_seasons = []

print("=" * 60)
print("NBA HISTORICAL DATA MERGER")
print("=" * 60)

for filename, season in season_files:
    print(f"\nProcessing {filename} (Season {season})...")
    
    # Read CSV - Basketball Reference format has citation lines at top
    # Read all lines, find where the data table starts
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the line with "Rk,Team" (the actual header)
    header_line = None
    for i, line in enumerate(lines):
        if line.startswith('Rk,Team'):
            header_line = i
            break
    
    # Read from the header line
    df = pd.read_csv(filename, skiprows=header_line)
    
    # Remove rows where 'Rk' is 'Rk' (duplicate headers in middle of table)
    df = df[df['Rk'] != 'Rk'].copy()
    
    # Remove "League Average" row
    df = df[df['Team'] != 'League Average'].copy()
    
    # Clean team names - remove asterisks and extract playoff status
    df['MadePlayoffs'] = df['Team'].apply(lambda x: 1 if '*' in str(x) else 0)
    df['Team'] = df['Team'].str.replace('*', '', regex=False)
    
    # Add season column
    df['Season'] = season
    
    # Select relevant columns for ML
    columns_to_keep = [
        'Team', 'Season', 'W', 'L', 'ORtg', 'DRtg', 'NRtg', 
        'Pace', 'FTr', '3PAr', 'TS%', 'MadePlayoffs'
    ]
    
    df_selected = df[columns_to_keep].copy()
    
    # Rename TS% to TS_Pct for easier handling
    df_selected.rename(columns={'TS%': 'TS_Pct', '3PAr': 'ThreePAr'}, inplace=True)
    
    # Count playoff/non-playoff teams
    playoff_count = df_selected['MadePlayoffs'].sum()
    non_playoff_count = len(df_selected) - playoff_count
    
    print(f"  ✓ Teams: {len(df_selected)}")
    print(f"  ✓ Playoff teams: {playoff_count}")
    print(f"  ✓ Non-playoff teams: {non_playoff_count}")
    
    all_seasons.append(df_selected)

# Combine all seasons
print("\n" + "=" * 60)
print("MERGING ALL SEASONS...")
print("=" * 60)

combined_df = pd.concat(all_seasons, ignore_index=True)

# Display summary statistics
print(f"\nTotal Records: {len(combined_df)}")
print(f"Total Playoff Teams: {combined_df['MadePlayoffs'].sum()}")
print(f"Total Non-Playoff Teams: {len(combined_df) - combined_df['MadePlayoffs'].sum()}")
print(f"\nColumns: {list(combined_df.columns)}")

# Check for missing values
print("\nMissing Values:")
print(combined_df.isnull().sum())

# Save to CSV
output_file = 'nba_historical_data.csv'
combined_df.to_csv(output_file, index=False)

print(f"\n✅ SUCCESS! Data saved to '{output_file}'")
print("=" * 60)

# Display first few rows
print("\nPreview of merged data:")
print(combined_df.head(10))

print("\nSeason breakdown:")
print(combined_df.groupby('Season').agg({
    'Team': 'count',
    'MadePlayoffs': 'sum'
}).rename(columns={'Team': 'Total_Teams', 'MadePlayoffs': 'Playoff_Teams'}))

print("\n🏀 Dataset ready for Azure Machine Learning AutoML!")
