import pandas as pd

# Deixa todas as colunas visíveis no terminal sem cortar no meio
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

# 1. Carregar base limpa
df = pd.read_csv("dados_limpos.csv")
total = len(df)

print("=" * 60)
print(f"ANÁLISE EXPLORATÓRIA COMPLETA (N = {total} respostas)")
print("=" * 60)


def resumo_categoria(coluna, titulo):
    print(f"\n--- {titulo} ---")
    contagem = df[coluna].value_counts(dropna=False)
    percentual = (
        df[coluna].value_counts(normalize=True, dropna=False) * 100
    ).round(1)
    tabela = pd.DataFrame({"Qtd": contagem, "%": percentual})
    print(tabela)


# 2. BLOCO 1: PERFIL E CONTEXTO
resumo_categoria("respondente", "Quem respondeu o formulário")

print("\n--- Idade (estatísticas descritivas) ---")
print(df["idade"].describe().round(2))

resumo_categoria("genero", "Gênero")
resumo_categoria("tipo_escola", "Tipo de instituição de ensino")
resumo_categoria("diagnostico_saude", "Diagnóstico de saúde")
resumo_categoria("acompanhamento_mental", "Acompanhamento/medicação mental")

# 3. BLOCO 2: HÁBITOS DE TELA E REGRAS
resumo_categoria("horas_tela_dia", "Média diária de horas de tela")
resumo_categoria("atividade_principal", "Atividade em que gasta mais tempo")
resumo_categoria("tela_antes_dormir", "Usa telas 2h antes de dormir")
resumo_categoria("adia_sono_por_tela", "Adia a hora de dormir por causa de telas")
resumo_categoria("regras_pais_tela", "Existem regras dos pais para uso de telas")

# 4. BLOCO 3: SONO E ATIVIDADE FÍSICA
resumo_categoria("qualidade_sono", "Qualidade do sono na maioria das noites")
resumo_categoria(
    "dias_atividade_fisica", "Dias de atividade física / ao ar livre na semana"
)

# 5. BLOCO 4: ESCORE DE ANSIEDADE (COLUNAS 11 A 17)
colunas_ansiedade = df.columns[11:18]
print("\n--- Colunas de ansiedade selecionadas (índices 11 a 17) ---")
for i, col in enumerate(colunas_ansiedade, start=11):
    print(f"[{i}] {col}")

# Mostra os valores únicos existentes nessas colunas para garantir precisão no mapeamento
valores_unicos_ans = sorted(
    pd.unique(df[colunas_ansiedade].astype(str).values.ravel())
)
print(
    "\nValores únicos encontrados nas colunas de ansiedade:",
    valores_unicos_ans,
)

# Mapeamento padrão (0 a 3) com variações comuns em português
mapa_ansiedade = {
    "nenhuma vez": 0,
    "nunca": 0,
    "vários dias": 1,
    "alguns dias": 1,
    "mais da metade dos dias": 2,
    "mais de metade dos dias": 2,
    "quase todos os dias": 3,
    "todos os dias": 3,
}

df_ans_num = df[colunas_ansiedade].apply(
    lambda col: col.astype(str).str.strip().str.lower().map(mapa_ansiedade)
)

nulos_mapeamento = df_ans_num.isnull().sum().sum()
if nulos_mapeamento > 0:
    print(
        f"\n[Atenção] {nulos_mapeamento} célula(s) de ansiedade não bateram com"
        " o mapa padrão."
    )
    print(
        "Valores não mapeados:",
        df[colunas_ansiedade].values[df_ans_num.isnull()],
    )
    # Preenche eventuais não mapeados com 0 para não quebrar o cálculo
    df_ans_num = df_ans_num.fillna(0)

df["escore_ansiedade"] = df_ans_num.sum(axis=1)

print(
    "\n--- Escore de Ansiedade (soma das 7 perguntas, escala 0 a 21) ---"
)
print(df["escore_ansiedade"].describe().round(2))
print("\nDistribuição do escore de ansiedade:")
print(df["escore_ansiedade"].value_counts().sort_index())

# 6. BLOCO 5: TABELAS CRUZADAS (CONTAGEM E %)
print(
    "\n--- Cruzamento: Horas de tela por dia vs. Qualidade do sono"
    " (contagem) ---"
)
cruz_sono = pd.crosstab(df["horas_tela_dia"], df["qualidade_sono"])
print(cruz_sono)

print(
    "\n--- Cruzamento: Horas de tela por dia vs. Regras dos pais (contagem)"
    " ---"
)
cruz_regras = pd.crosstab(df["horas_tela_dia"], df["regras_pais_tela"])
print(cruz_regras)

print(
    "\n--- Cruzamento: Tela antes de dormir vs. Adia o sono por tela (%) ---"
)
cruz_adiar_pct = (
    pd.crosstab(
        df["tela_antes_dormir"], df["adia_sono_por_tela"], normalize="index"
    )
    * 100
).round(1)
print(cruz_adiar_pct)

# 7. BLOCO 6: CORRELAÇÃO NUMÉRICA (IDADE, ESTIMATIVA DE HORAS DE TELA E ANSIEDADE)
mapa_horas_num = {
    "Menos de 2 horas": 1.0,
    "De 2 a menos de 4 horas": 3.0,
    "De 4 a menos de 6 horas": 5.0,
    "De 6 a menos de 8 horas": 7.0,
    "De 8 a 10 horas": 9.0,
    "Mais de 10 horas": 11.0,
}
df["horas_tela_estimada"] = df["horas_tela_dia"].map(mapa_horas_num)

print(
    "\n--- Média do escore de ansiedade por faixa de horas de tela ---"
)
resumo_ans_tela = (
    df.groupby("horas_tela_dia", observed=False)["escore_ansiedade"]
    .agg(qtd="count", media="mean", mediana="median")
    .round(2)
)
print(resumo_ans_tela)

print(
    "\n--- Matriz de correlação (Pearson) entre variáveis numéricas ---"
)
corr = df[["idade", "horas_tela_estimada", "escore_ansiedade"]].corr().round(3)
print(corr)