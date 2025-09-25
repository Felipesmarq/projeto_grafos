import pandas as pd
import unicodedata

df = pd.read_csv("projeto_grafos/data/bairros_recife.csv", header=None)

microrregioes = df.iloc[0]
df = df.drop(0).reset_index(drop=True)

df.columns = microrregioes

df_melt = df.melt(var_name="microrregiao", value_name="bairro")

df_melt = df_melt.dropna(subset=["bairro"])
df_melt = df_melt[df_melt["bairro"].str.strip() != ""]

def normalizar(texto):
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.strip().title()

df_melt["bairro"] = df_melt["bairro"].apply(normalizar)

bairros_unique = df_melt.drop_duplicates(subset=["bairro"])

bairros_unique.to_csv("projeto_grafos/data/bairros_unique.csv", index=False)

print(" Arquivo 'bairros_unique.csv' gerado")
