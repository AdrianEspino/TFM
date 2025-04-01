import pandas as pd

# Cargar el dataset unificado
df = pd.read_csv("C:\\Users\\adrim\\OneDrive\\Documentos\\Ingenieria informática\\TFM\\dataset_unificado.csv", delimiter= ";", error_bad_lines=False)

# Ver las primeras filas
print(df.head())

# Ver información general del dataset
print(df.info())

# Ver valores únicos en cada columna (opcional)
for col in df.columns:
    print(f"Columna: {col}")
    print(df[col].unique()[:10])  # Muestra solo los primeros 10 valores únicos
    print("-" * 30)