import pandas as pd

# Lendo o arquivo CSV que está na mesma pasta do projeto
df = pd.read_csv("respostas.csv")

# Exibindo o total de linhas (respostas) e colunas (perguntas)
print(f"Total de respostas coletadas: {df.shape[0]}")
print(f"Total de perguntas (colunas): {df.shape[1]}")

# Listando todas as perguntas (colunas) da planilha com seus números
print("\n--- LISTA DE PERGUNTAS (COLUNAS) ---")
for i, coluna in enumerate(df.columns):
    print(f"[{i}] {coluna}")

# Verificando tipos de dados e valores nulos
print("\n--- INFORMAÇÕES GERAIS ---")
print(df.info())

# Mostrando as 5 primeiras respostas para conferir
print("\nPrimeiras respostas:")
print(df.head())