import pandas as pd
import numpy as np

# Leer el dataset original
df = pd.read_csv('C:\\Users\\adrim\\OneDrive\\Documentos\\Ingenieria informática\\TFM\\2017-2025_LoL_esports_match_data_from_OraclesElixir.csv')

# Función para obtener enfrentamientos entre equipos
def get_champion_matchups(row):
    matchups = []
    # Obtener picks del equipo azul
    blue_picks = [row[f'pick{i}'] for i in range(1, 6) if pd.notna(row[f'pick{i}'])]
    # Obtener picks del equipo rojo
    red_picks = [row[f'pick{i}'] for i in range(1, 6) if pd.notna(row[f'pick{i}'])]
    
    # Para cada campeón del equipo azul, enfrentarlo contra cada campeón del equipo rojo
    for blue_champ in blue_picks:
        for red_champ in red_picks:
            # Ordenamos alfabéticamente para consistencia
            matchup = (min(blue_champ, red_champ), max(blue_champ, red_champ))
            # Guardamos el resultado desde la perspectiva del primer campeón
            result = 1 if row['result'] == 1 and blue_champ == matchup[0] else 0
            matchups.append((matchup[0], matchup[1], result))
    return matchups

# Recopilar todos los matchups
all_matchups = []
for _, row in df.iterrows():
    if pd.notna(row['pick1']):  # Asegurarse de que la fila tiene datos válidos
        matchups = get_champion_matchups(row)
        all_matchups.extend(matchups)

# Crear DataFrame de matchups
matchup_df = pd.DataFrame(all_matchups, columns=['champion1', 'champion2', 'result'])

# Calcular estadísticas de matchups
matchup_stats = matchup_df.groupby(['champion1', 'champion2']).agg({
    'result': ['count', 'mean']
}).reset_index()

matchup_stats.columns = ['champion1', 'champion2', 'games_against', 'winrate_vs']

# Filtrar solo matchups con suficientes juegos (mínimo 10 enfrentamientos)
matchup_stats = matchup_stats[matchup_stats['games_against'] >= 10]

# Ordenar por diferencia de winrate para encontrar los mejores y peores matchups
matchup_stats['winrate_difference'] = abs(matchup_stats['winrate_vs'] - 0.5)
matchup_stats = matchup_stats.sort_values('winrate_difference', ascending=False)

# Primero, expandir cada fila para obtener dos perspectivas:
# 1. Desde la perspectiva de champion1
# 2. Desde la perspectiva de champion2

# Creamos dos dataframes

df1 = matchup_stats.copy()
df1.rename(columns={'champion1': 'champion', 'champion2': 'opponent', 'winrate_vs': 'adjusted_winrate', 'games_against': 'games'}, inplace=True)

# Para el otro, ajustar la winrate

df2 = matchup_stats.copy()
df2.rename(columns={'champion2': 'champion', 'champion1': 'opponent', 'games_against': 'games'}, inplace=True)
df2['adjusted_winrate'] = 1 - df2['winrate_vs']

df2.drop(columns=['winrate_vs'], inplace=True)

# Combinar ambos dataframes
combined = pd.concat([df1[['champion','opponent','adjusted_winrate','games']], df2[['champion','opponent','adjusted_winrate','games']]], ignore_index=True)

# Remover registros donde el campeón sea el mismo que su oponente (aunque ya no deberían existir)
combined = combined[combined['champion'] != combined['opponent']]

# Ordenar alfabéticamente por 'champion' y luego por 'opponent'
combined = combined.sort_values(by=['champion', 'opponent']).reset_index(drop=True)

# Guardar el csv
combined.to_csv('champion_counters.csv', index=False)

print("Archivo CSV 'champion_counters.csv' generado con la información de adjusted_winrate para todos los pares de campeones.")