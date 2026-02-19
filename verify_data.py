import pandas as pd

# Load the dataset
df = pd.read_csv('nba_historical_data.csv')

print('=' * 60)
print('✅ NBA HISTORICAL DATA - SUCCESSFULLY CREATED')
print('=' * 60)

print(f'\n📊 DATASET OVERVIEW:')
print(f'   Total Records: {len(df)}')
print(f'   Seasons: {sorted(df["Season"].unique())}')
print(f'   Teams per Season: {len(df) // 5}')
print(f'   Playoff Teams (MadePlayoffs=1): {df["MadePlayoffs"].sum()}')
print(f'   Non-Playoff Teams (MadePlayoffs=0): {len(df) - df["MadePlayoffs"].sum()}')

print(f'\n📋 COLUMNS:')
for i, col in enumerate(df.columns, 1):
    print(f'   {i}. {col}')

print('\n' + '=' * 60)
print('🔍 SAMPLE DATA (First 10 rows):')
print('=' * 60)
print(df.head(10).to_string(index=False))

print('\n' + '=' * 60)
print('🏀 2025 SEASON PLAYOFF TEAMS:')
print('=' * 60)
playoff_2025 = df[(df['Season'] == 2025) & (df['MadePlayoffs'] == 1)].sort_values('Wins', ascending=False)
print(playoff_2025[['Team', 'Wins', 'Losses', 'WinPct', 'DefensiveRating']].to_string(index=False))

print('\n✅ Dataset is ready for Azure Machine Learning!')
