import pandas as pd
from estatistica import Estatistica
from outliers import Outliers
from teste_hipotese import TesteHipotese
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv('pandas.read_csv.csv', sep=';')

# Parte 1 – Estatística Descritiva
estatistica = Estatistica(df)
estatisticas = estatistica.calcular_estatisticas()
print(estatisticas)

# Parte 2 – Detecção de Outliers
outliers = Outliers(df)
q1_salario = estatisticas['q1_salario']
q3_salario = estatisticas['q3_salario']
iqr_salario = q3_salario - q1_salario
outliers_pessoas = outliers.detectar_outliers(q1_salario, q3_salario, iqr_salario)
print("Outliers:", outliers_pessoas)

# Parte 3 – Teste de Hipótese
grupo_brasil = df[df['pais'] == 'Brasil']['salario']
grupo_eua = df[df['pais'] == 'EUA']['salario']
teste = TesteHipotese(df)
t_stat, p_value = teste.aplicar_tteste(grupo_brasil, grupo_eua)
print(f"T-Statistic: {t_stat}, P-Value: {p_value}")
if p_value < 0.05:
    print("Rejeitamos H₀: Há diferença significativa entre os salários.")
else:
    print("Não rejeitamos H₀: Não há diferença significativa entre os salários.")

# Visualizações
plt.figure(figsize=(12, 6))

# Boxplot
plt.subplot(1, 2, 1)
sns.boxplot(x=df['salario'])
plt.title('Boxplot - Salário')

plt.subplot(1, 2, 2)
sns.boxplot(x=df['nota_avaliacao'])
plt.title('Boxplot - Nota Avaliação')

plt.tight_layout()
plt.show()

# Histograma para Idade
plt.figure(figsize=(8, 6))
sns.histplot(df['idade'], kde=True, bins=30)
plt.title('Histograma - Idade')
plt.show()
