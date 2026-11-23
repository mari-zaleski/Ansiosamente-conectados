from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Estilo visual limpo e legível
sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 150

# Garante que a pasta de saída exista
pasta_img = Path("imagens")
pasta_img.mkdir(exist_ok=True)

# Carrega base limpa já preparada
df = pd.read_csv("dados_limpos.csv")

# Garante escore_ansiedade e horas_tela_estimada caso ainda não existam no CSV
if "escore_ansiedade" not in df.columns:
  colunas_ansiedade = df.columns[11:18]
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
  ).fillna(0)
  df["escore_ansiedade"] = df_ans_num.sum(axis=1).astype(int)

if "horas_tela_estimada" not in df.columns:
  mapa_horas_num = {
      "Menos de 2 horas": 1.0,
      "De 2 a menos de 4 horas": 3.0,
      "De 4 a menos de 6 horas": 5.0,
      "De 6 a menos de 8 horas": 7.0,
      "De 8 a 10 horas": 9.0,
      "Mais de 10 horas": 11.0,
  }
  df["horas_tela_estimada"] = df["horas_tela_dia"].map(mapa_horas_num)

ordem_horas = [
    "Menos de 2 horas",
    "De 2 a menos de 4 horas",
    "De 4 a menos de 6 horas",
    "De 6 a menos de 8 horas",
    "De 8 a 10 horas",
    "Mais de 10 horas",
]

ordem_sono = ["Muito boa", "Boa", "Regular", "Ruim"]

# 1. Horas de tela por dia
plt.figure(figsize=(9, 4.8))
ax = sns.countplot(
    data=df,
    y="horas_tela_dia",
    order=ordem_horas,
    hue="horas_tela_dia",
    palette="Blues_d",
    legend=False,
)
ax.set_title("Média diária de horas de tela (N = 75)")
ax.set_xlabel("Quantidade de respondentes")
ax.set_ylabel("Faixa de horas por dia")
plt.tight_layout()
plt.savefig(pasta_img / "01_horas_tela_dia.png")
plt.close()

# 2. Atividade principal
plt.figure(figsize=(9, 4.8))
ordem_ativ = df["atividade_principal"].value_counts().index
ax = sns.countplot(
    data=df,
    y="atividade_principal",
    order=ordem_ativ,
    hue="atividade_principal",
    palette="viridis",
    legend=False,
)
ax.set_title("Atividade em que gasta mais tempo (N = 75)")
ax.set_xlabel("Quantidade de respondentes")
ax.set_ylabel("Atividade")
plt.tight_layout()
plt.savefig(pasta_img / "02_atividade_principal.png")
plt.close()

# 3. Qualidade do sono
plt.figure(figsize=(8, 4.5))
ax = sns.countplot(
    data=df,
    x="qualidade_sono",
    order=ordem_sono,
    hue="qualidade_sono",
    palette="coolwarm",
    legend=False,
)
ax.set_title("Qualidade do sono na maioria das noites (N = 75)")
ax.set_xlabel("Qualidade do sono")
ax.set_ylabel("Quantidade de respondentes")
plt.tight_layout()
plt.savefig(pasta_img / "03_qualidade_sono.png")
plt.close()

# 4. Média do escore de ansiedade por faixa de horas de tela
plt.figure(figsize=(9, 4.8))
medias_ans = (
    df.groupby("horas_tela_dia", observed=False)["escore_ansiedade"]
    .mean()
    .reindex(ordem_horas)
    .reset_index()
)
ax = sns.barplot(
    data=medias_ans,
    x="escore_ansiedade",
    y="horas_tela_dia",
    hue="horas_tela_dia",
    palette="magma",
    legend=False,
)
ax.set_title("Média do escore de ansiedade (0–21) por faixa de horas de tela")
ax.set_xlabel("Média do escore de ansiedade")
ax.set_ylabel("Faixa de horas por dia")
plt.tight_layout()
plt.savefig(pasta_img / "04_ansiedade_por_faixa_tela.png")
plt.close()

# 5. Tela 2h antes de dormir vs. Adia o sono por tela (%)
cruz_pct = (
    pd.crosstab(
        df["tela_antes_dormir"], df["adia_sono_por_tela"], normalize="index"
    )
    * 100
)
ax = cruz_pct.plot(
    kind="bar", stacked=False, color=["#4C72B0", "#DD8452"], figsize=(8, 4.8)
)
ax.set_title("Uso de tela antes de dormir vs. Adiar o sono (%)")
ax.set_xlabel("Usa telas 2h antes de dormir")
ax.set_ylabel("Percentual (%)")
ax.legend(title="Adia o sono por tela")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(pasta_img / "05_tela_antes_dormir_vs_adia_sono.png")
plt.close()

# 6. Tendência linear (dispersão + linha de regressão)
g = sns.lmplot(
    data=df,
    x="horas_tela_estimada",
    y="escore_ansiedade",
    height=5,
    aspect=1.5,
    scatter_kws={"alpha": 0.65, "color": "#2b5c8f"},
    line_kws={"color": "#d95f02", "linewidth": 2},
)
g.set_axis_labels(
    "Horas estimadas de tela por dia", "Escore de ansiedade (0–21)"
)
g.fig.suptitle(
    "Tendência entre horas estimadas de tela e escore de ansiedade", y=1.02
)
g.savefig(pasta_img / "06_tendencia_tela_ansiedade.png", bbox_inches="tight")
plt.close("all")

print(
    "Todos os 6 gráficos foram gerados e salvos na pasta 'imagens/' com"
    " sucesso!"
)