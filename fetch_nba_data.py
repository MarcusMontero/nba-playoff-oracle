"""
NBA Data Fetcher - Downloads Real NBA Team Statistics (2021-2025)
Fetches data from Basketball Reference and formats it for Azure AutoML
"""

import pandas as pd
import requests
from io import StringIO
import time

# NBA Playoff Teams by Season (Historical Data)
PLAYOFF_TEAMS = {
    2021: [
        # Eastern Conference
        'Philadelphia 76ers', 'Brooklyn Nets', 'Milwaukee Bucks', 'New York Knicks',
        'Atlanta Hawks', 'Miami Heat', 'Boston Celtics', 'Washington Wizards',
        # Western Conference
        'Utah Jazz', 'Phoenix Suns', 'Denver Nuggets', 'Los Angeles Clippers',
        'Dallas Mavericks', 'Portland Trail Blazers', 'Memphis Grizzlies', 'Los Angeles Lakers'
    ],
    2022: [
        # Eastern Conference
        'Miami Heat', 'Boston Celtics', 'Milwaukee Bucks', 'Philadelphia 76ers',
        'Toronto Raptors', 'Chicago Bulls', 'Brooklyn Nets', 'Cleveland Cavaliers',
        # Western Conference
        'Phoenix Suns', 'Memphis Grizzlies', 'Golden State Warriors', 'Dallas Mavericks',
        'Utah Jazz', 'Denver Nuggets', 'Minnesota Timberwolves', 'Los Angeles Clippers'
    ],
    2023: [
        # Eastern Conference
        'Milwaukee Bucks', 'Boston Celtics', 'Philadelphia 76ers', 'Cleveland Cavaliers',
        'New York Knicks', 'Brooklyn Nets', 'Miami Heat', 'Atlanta Hawks',
        # Western Conference
        'Denver Nuggets', 'Memphis Grizzlies', 'Sacramento Kings', 'Phoenix Suns',
        'Los Angeles Clippers', 'Golden State Warriors', 'Los Angeles Lakers', 'Minnesota Timberwolves'
    ],
    2024: [
        # Eastern Conference
        'Boston Celtics', 'New York Knicks', 'Milwaukee Bucks', 'Cleveland Cavaliers',
        'Orlando Magic', 'Indiana Pacers', 'Philadelphia 76ers', 'Miami Heat',
        # Western Conference
        'Oklahoma City Thunder', 'Denver Nuggets', 'Minnesota Timberwolves', 'Los Angeles Clippers',
        'Dallas Mavericks', 'Phoenix Suns', 'New Orleans Pelicans', 'Los Angeles Lakers'
    ],
    2025: [
        # Eastern Conference (2024-25 season - projected based on current standings)
        'Boston Celtics', 'Cleveland Cavaliers', 'New York Knicks', 'Milwaukee Bucks',
        'Orlando Magic', 'Miami Heat', 'Indiana Pacers', 'Philadelphia 76ers',
        # Western Conference
        'Oklahoma City Thunder', 'Denver Nuggets', 'Houston Rockets', 'Memphis Grizzlies',
        'Dallas Mavericks', 'Los Angeles Lakers', 'Golden State Warriors', 'Minnesota Timberwolves'
    ]
}

def fetch_season_data(year):
    """
    Fetch team statistics for a given NBA season from Basketball Reference
    
    Args:
        year: The ending year of the season (e.g., 2023 for 2022-23 season)
    
    Returns:
        DataFrame with team statistics
    """
    print(f"📊 Fetching data for {year-1}-{year} season...")
    
    # Basketball Reference URL pattern
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}.html"
    
    try:
        # Send request with headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML tables using pandas
        tables = pd.read_html(StringIO(response.text))
        
        # Find the team stats table (usually contains 'Team' column and stats)
        team_stats = None
        for table in tables:
            if 'Team' in table.columns and 'W' in table.columns:
                team_stats = table
                break
        
        if team_stats is None:
            raise ValueError("Could not find team statistics table")
        
        # Clean and prepare data
        df = team_stats.copy()
        
        # Remove any rows where Team is NaN or contains "League Average"
        df = df[df['Team'].notna()]
        df = df[~df['Team'].str.contains('League Average|Division|Conference', na=False)]
        
        # Remove asterisks from team names (playoff indicators)
        df['Team'] = df['Team'].str.replace('*', '', regex=False).str.strip()
        
        # Add season year
        df['Season'] = year
        
        # Determine which teams made playoffs
        df['MadePlayoffs'] = df['Team'].apply(
            lambda x: 1 if x in PLAYOFF_TEAMS.get(year, []) else 0
        )
        
        print(f"   ✅ Found {len(df)} teams")
        return df
        
    except Exception as e:
        print(f"   ❌ Error fetching {year} data: {str(e)}")
        return None

def create_nba_dataset():
    """
    Create comprehensive NBA dataset for Azure ML training
    """
    print("=" * 60)
    print("🏀 NBA POSTSEASON ORACLE - DATA COLLECTION")
    print("=" * 60)
    print()
    
    all_seasons = []
    
    # Fetch data for seasons 2021 through 2025
    for year in range(2021, 2026):
        df = fetch_season_data(year)
        if df is not None:
            all_seasons.append(df)
            time.sleep(1)  # Be nice to the server
    
    if not all_seasons:
        print("\n❌ Failed to fetch any data. Please check your internet connection.")
        return None
    
    # Combine all seasons
    print("\n🔄 Combining data from all seasons...")
    combined_df = pd.concat(all_seasons, ignore_index=True)
    
    # Select and rename columns for Azure ML
    print("🔧 Formatting data for Azure Machine Learning...")
    
    # Column mapping (Basketball Reference -> Our Format)
    column_mapping = {
        'Team': 'Team',
        'W': 'Wins',
        'L': 'Losses',
        'W/L%': 'WinPct',
        'ORtg': 'OffensiveRating',
        'DRtg': 'DefensiveRating',
        'NRtg': 'NetRating',
        '3P%': 'ThreePointPct',
        'FT%': 'FreeThrowPct',
        'TRB%': 'ReboundPct',
        'AST%': 'AssistPct',
        'TOV%': 'TurnoverPct',
        'Season': 'Season',
        'MadePlayoffs': 'MadePlayoffs'
    }
    
    # Select available columns
    available_cols = [col for col in column_mapping.keys() if col in combined_df.columns]
    final_df = combined_df[available_cols].copy()
    
    # Rename columns
    rename_dict = {old: column_mapping[old] for old in available_cols}
    final_df.rename(columns=rename_dict, inplace=True)
    
    # Fill missing values with reasonable defaults
    if 'NetRating' not in final_df.columns and 'OffensiveRating' in final_df.columns and 'DefensiveRating' in final_df.columns:
        final_df['NetRating'] = final_df['OffensiveRating'] - final_df['DefensiveRating']
    
    # Convert percentages from decimals to actual percentages if needed
    for col in ['ThreePointPct', 'FreeThrowPct', 'WinPct']:
        if col in final_df.columns:
            # If values are between 0-1, keep as is; if > 1, divide by 100
            if final_df[col].max() > 1:
                final_df[col] = final_df[col] / 100
    
    # Ensure numeric types
    numeric_cols = final_df.columns.drop(['Team', 'Season'])
    for col in numeric_cols:
        final_df[col] = pd.to_numeric(final_df[col], errors='coerce')
    
    # Remove any rows with missing critical data
    final_df.dropna(subset=['Wins', 'Losses', 'MadePlayoffs'], inplace=True)
    
    print(f"✅ Dataset ready: {len(final_df)} team-seasons")
    print(f"   Seasons: {sorted(final_df['Season'].unique())}")
    print(f"   Teams per season: ~{len(final_df) // 5}")
    print(f"   Playoff teams: {final_df['MadePlayoffs'].sum()}")
    print(f"   Non-playoff teams: {len(final_df) - final_df['MadePlayoffs'].sum()}")
    
    return final_df

def main():
    """Main execution function"""
    
    # Create the dataset
    df = create_nba_dataset()
    
    if df is None:
        print("\n⚠️ Data collection failed. Using fallback method...")
        print("Please try again or check your internet connection.")
        return
    
    # Save to CSV
    output_file = 'nba_historical_data.csv'
    print(f"\n💾 Saving to {output_file}...")
    df.to_csv(output_file, index=False)
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! Real NBA data downloaded and formatted")
    print("=" * 60)
    print(f"\n📁 File created: {output_file}")
    print(f"📊 Total records: {len(df)}")
    print("\n🔍 Preview of the data:")
    print(df.head(10).to_string())
    print("\n📈 Column Summary:")
    print(df.describe())
    print("\n✅ Ready for Azure Machine Learning!")
    print("\nNext step: Proceed to Task 1.2 - Create Azure Storage Account")

if __name__ == "__main__":
    main()
