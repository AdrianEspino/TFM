import pandas as pd

# Intentar con diferentes delimitadores
df = pd.read_csv("C:\\Users\\adrim\\OneDrive\\Documentos\\Ingenieria informática\\TFM\\OE Public Match Data\\2014_LoL_esports_match_data_from_OraclesElixir.csv", header = None)

# Separar los datos en columnas usando ',' como delimitador
df_separado = df[0].str.split(",", expand=True)

print(df.head())  # Ver los primeros datos

# Guardar en un nuevo archivo corregido
df.to_csv("archivo_corregido.csv", index=False)