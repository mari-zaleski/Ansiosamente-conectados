import pandas as pd

# 1. Carregar base bruta sem alterar o arquivo original
df_raw = pd.read_csv("respostas.csv")
df = df_raw.copy()

print("=== ANTES DA LIMPEZA ===")
print(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")
print(f"Duplicatas exatas: {df.duplicated().sum()}")
print(f"Total de valores nulos: {df.isnull().sum().sum()}")

# 2. Remover duplicatas exatas (se houver)
df = df.drop_duplicates()

# 3. Padronizar nomes das colunas principais por índice
novos_nomes = {
    df.columns[0]: "data_resposta",
    df.columns[1]: "respondente",
    df.columns[2]: "idade",
    df.columns[3]: "genero",
    df.columns[4]: "tipo_escola",
    df.columns[5]: "serie_escolar",
    df.columns[6]: "diagnostico_saude",
    df.columns[7]: "acompanhamento_mental",
    df.columns[8]: "dispositivos",
    df.columns[9]: "horas_tela_dia",
    df.columns[10]: "atividade_principal",
    df.columns[33]: "tela_antes_dormir",
    df.columns[34]: "tela_atrapalha_sono",
    df.columns[35]: "horas_sono_noite",
    df.columns[36]: "tempo_pegar_sono",
    df.columns[37]: "qualidade_sono",
    df.columns[38]: "acorda_noite",
    df.columns[39]: "adia_sono_por_tela",
    df.columns[40]: "dias_atividade_fisica",
    df.columns[41]: "duracao_atividade_fisica",
    df.columns[42]: "tempo_sentado_sem_tela",
    df.columns[57]: "regras_pais_tela",
    df.columns[59]: "idade_primeiro_celular",
}
df = df.rename(columns=novos_nomes)

# 4. Limpar espaços extras em colunas de texto
for col in df.select_dtypes(include=["object", "string"]).columns:
  df[col] = df[col].str.strip()

# 5. Validar idade como numérica e tratar com mediana se houver problema
df["idade"] = pd.to_numeric(df["idade"], errors="coerce")
if df["idade"].isnull().sum() > 0:
  df["idade"] = df["idade"].fillna(df["idade"].median())

# 6. Preencher eventuais valores nulos restantes com a moda (valor mais frequente)
for col in df.columns:
  if df[col].isnull().sum() > 0:
    df[col] = df[col].fillna(df[col].mode()[0])

# 7. Salvar base limpa
df.to_csv("dados_limpos.csv", index=False)

print("\n=== DEPOIS DA LIMPEZA ===")
print(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")
print(f"Duplicatas exatas restantes: {df.duplicated().sum()}")
print(f"Valores nulos restantes: {df.isnull().sum().sum()}")
print("\nValores únicos em 'qualidade_sono':", df["qualidade_sono"].unique())
print("Valores únicos em 'horas_tela_dia':", df["horas_tela_dia"].unique())
print("\nArquivo 'dados_limpos.csv' salvo com sucesso!")