import pandas as pd
import numpy as np

# Leer el dataset original
df = pd.read_csv('C:\\Users\\adrim\\OneDrive\\Documentos\\Ingenieria informática\\TFM\\2017-2025_LoL_esports_match_data_from_OraclesElixir.csv')

# 1. Estadísticas por campeón
champion_stats = df.groupby('champion').agg({
    'gameid': 'count',  # Número de juegos
    'result': 'mean',   # Winrate
    'kills': 'mean',    # Promedio de kills
    'deaths': 'mean',   # Promedio de muertes
    'assists': 'mean',  # Promedio de asistencias
    'dpm': 'mean',      # Daño por minuto
    'damagetakenperminute': 'mean',  # Daño recibido por minuto
    'goldat10': 'mean', # Oro a los 10 minutos
    'xpat10': 'mean',   # XP a los 10 minutos
}).reset_index()

# Renombrar columnas para claridad
champion_stats.columns = ['champion', 'games_played', 'winrate', 'avg_kills', 'avg_deaths', 
                         'avg_assists', 'avg_dpm', 'avg_damagetaken', 'avg_gold10', 'avg_xp10']

# Filtrar campeones con suficientes juegos (mínimo 20 para tener estadísticas significativas)
champion_stats = champion_stats[champion_stats['games_played'] >= 20]

print("\
Estadísticas por campeón (primeros 5 ejemplos):")
print(champion_stats.head())

# 2. Calcular sinergias entre campeones (winrate cuando juegan juntos)
def get_champion_pairs(row):
    pairs = []
    picks = [f'pick{i}' for i in range(1, 6)]
    for i in range(len(picks)):
        for j in range(i+1, len(picks)):
            if pd.notna(row[picks[i]]) and pd.notna(row[picks[j]]):
                pair = tuple(sorted([row[picks[i]], row[picks[j]]])  )
                pairs.append((pair, row['result']))
    return pairs

# Calcular sinergias
all_pairs = []
for _, row in df.iterrows():
    pairs = get_champion_pairs(row)
    all_pairs.extend(pairs)

pair_stats = pd.DataFrame(all_pairs, columns=['pair', 'result'])
synergy_stats = pair_stats.groupby('pair').agg({
    'result': ['count', 'mean']
}).reset_index()

synergy_stats.columns = ['champion_pair', 'games_together', 'winrate_together']
synergy_stats = synergy_stats[synergy_stats['games_together'] >= 10]

print("\
Sinergias entre campeones (primeros 5 ejemplos):")
print(synergy_stats.head())

# 3. Calcular estadísticas por rol
role_stats = df.groupby('position').agg({
    'gameid': 'count',
    'result': 'mean',
    'kills': 'mean',
    'deaths': 'mean',
    'assists': 'mean',
    'dpm': 'mean'
}).reset_index()

print("\
Estadísticas por rol:")
print(role_stats)

# 4. Crear un dataset enriquecido para el modelo
# Primero, obtener el draft base como antes
draft_columns = ['gameid', 'side', 'result'] + [f'ban{i}' for i in range(1,6)] + [f'pick{i}' for i in range(1,6)]
draft_data = df[draft_columns].copy()
draft_data = draft_data.dropna(subset=[f'pick{i}' for i in range(1,6)])

# Separar por lado
blue_side = draft_data[draft_data['side'] == 'Blue'].set_index('gameid')
red_side = draft_data[draft_data['side'] == 'Red'].set_index('gameid')

# Renombrar columnas
blue_columns = {col: f'blue_{col}' for col in blue_side.columns if col != 'gameid'}
red_columns = {col: f'red_{col}' for col in red_side.columns if col != 'gameid'}

blue_side = blue_side.rename(columns=blue_columns)
red_side = red_side.rename(columns=red_columns)

# Combinar los datos
enriched_drafts = blue_side.join(red_side, how='inner')

# Guardar los diferentes datasets
champion_stats.to_csv('champion_stats.csv')
synergy_stats.to_csv('champion_synergies.csv')
role_stats.to_csv('role_stats.csv')
enriched_drafts.to_csv('enriched_draft_data.csv')

print("\
Datasets guardados con éxito. Dimensiones:")
print(f"Champion stats: {champion_stats.shape}")
print(f"Synergy stats: {synergy_stats.shape}")
print(f"Role stats: {role_stats.shape}")
print(f"Enriched drafts: {enriched_drafts.shape}")
