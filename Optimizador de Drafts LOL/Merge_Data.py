import pandas as pd
import os

# Ruta a la carpeta donde están los archivos
ruta = "C:\\Users\\adrim\\OneDrive\\Documentos\\Ingenieria informática\\TFM\\OE Public Match Data"

# Lista todos los archivos CSV en la carpeta
archivos = [f for f in os.listdir(ruta) if f.endswith('.csv')]

# Carga y combina los archivos
dataframes = [pd.read_csv(os.path.join(ruta, file)) for file in archivos]
df_combinado = pd.concat(dataframes, ignore_index=True)

# Guarda el dataset unificado
df_combinado.to_csv("C:\\Users\\adrim\\OneDrive\\Documentos\\Ingenieria informática\\TFM\\2017-2025_LoL_esports_match_data_from_OraclesElixir.csv", index=False)

print(f"Dataset combinado con {df_combinado.shape[0]} filas y {df_combinado.shape[1]} columnas.")