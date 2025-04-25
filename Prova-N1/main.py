import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import yfinance as yf
from datetime import datetime, timedelta
import warnings

# Ignorar avisos
warnings.filterwarnings('ignore')

# Configurando estilo das visualizações
plt.style.use('seaborn-v0_8-whitegrid')
sns.set(font_scale=1.2)
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14

# 1. COLETA DE DADOS COM WEB SCRAPING
print("Etapa 1: Coletando dados históricos...")

# Definindo período (10 anos)
end_date = datetime.now()
start_date = end_date - timedelta(days=365*10)

# Formatando datas para o yfinance
start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

# Símbolos para o mercado brasileiro no Yahoo Finance
tickers = ['VALE3.SA', 'PETR4.SA']
ticker_names = {'VALE3.SA': 'VALE3', 'PETR4.SA': 'PETR4'}

# Coletando dados
data = {}
monthly_prices = {}

for ticker in tickers:
    # Download dos dados históricos
    print(f"Baixando dados de {ticker_names[ticker]}...")
    df = yf.download(ticker, start=start_str, end=end_str)
    
    # Verificando as colunas disponíveis
    print(f"Colunas disponíveis para {ticker_names[ticker]}: {df.columns.tolist()}")
    
    # Salvando os dados completos
    data[ticker] = df
    
    # Extraindo preços de fechamento mensais (último dia de cada mês)
    if 'Adj Close' in df.columns:
        print(f"Usando 'Adj Close' para {ticker_names[ticker]}")
        monthly_data = df['Adj Close'].resample('M').last()
    else:
        print(f"'Adj Close' não encontrado, usando 'Close' para {ticker_names[ticker]}")
        if isinstance(df['Close'], pd.DataFrame):  # Se for uma matriz multidimensional
            # Extraindo apenas a coluna para o ticker atual
            monthly_data = df['Close'][ticker].resample('M').last()
        else:
            monthly_data = df['Close'].resample('M').last()
    
    monthly_prices[ticker] = monthly_data
    
    # Salvando CSV com separador ;
    monthly_data_df = pd.DataFrame(monthly_data)
    monthly_data_df.columns = ['Preco']
    monthly_data_df.to_csv(f"{ticker_names[ticker]}_precos_mensais.csv", sep=';')
    print(f"Dados de {ticker_names[ticker]} salvos com sucesso!")

# 2. CÁLCULO DOS RETORNOS MENSAIS
print("\nEtapa 2: Calculando retornos mensais...")

returns = {}
all_returns = []

for ticker in tickers:
    # Calculando retornos percentuais: (preço_atual - preço_anterior) / preço_anterior * 100
    monthly_return = pd.Series(monthly_prices[ticker]).pct_change() * 100
    returns[ticker] = monthly_return
    
    # Criando DataFrame para cada ação
    ticker_returns = pd.DataFrame({
        'Data': monthly_return.index,
        'Acao': ticker_names[ticker],
        'Retorno': monthly_return.values
    })
    
    all_returns.append(ticker_returns)

# Combinando todos os retornos em um único DataFrame
returns_df = pd.concat(all_returns).reset_index(drop=True)
returns_df = returns_df.dropna()  # Removendo linhas com NaN (primeiro mês não tem retorno)

# Salvando os retornos em CSV
returns_df.to_csv("retornos_mensais.csv", sep=';', index=False)
print("Retornos mensais calculados e salvos com sucesso!")

# 3. ESTATÍSTICA DESCRITIVA
print("\nEtapa 3: Calculando estatísticas descritivas...")

stats_results = {}

for ticker in tickers:
    ticker_clean = ticker_names[ticker]
    return_series = returns[ticker].dropna()
    
    # Calculando estatísticas
    stats_dict = {
        'Média': return_series.mean(),
        'Mediana': return_series.median(),
        'Moda': return_series.mode().iloc[0] if not return_series.mode().empty else np.nan,
        'Desvio Padrão': return_series.std(),
        'Q1': return_series.quantile(0.25),
        'Q2': return_series.quantile(0.5),
        'Q3': return_series.quantile(0.75),
        'IQR': return_series.quantile(0.75) - return_series.quantile(0.25),
        'Mínimo': return_series.min(),
        'Máximo': return_series.max()
    }
    
    stats_results[ticker_clean] = stats_dict
    
# Criando DataFrame de estatísticas
stats_df = pd.DataFrame(stats_results)
print(stats_df)

# Salvando estatísticas em CSV
stats_df.to_csv("estatisticas_descritivas.csv", sep=';')

# 4. DETECÇÃO DE OUTLIERS
print("\nEtapa 4: Detectando outliers...")

outliers = {}

for ticker in tickers:
    ticker_clean = ticker_names[ticker]
    return_series = returns[ticker].dropna()
    
    # Calculando limites para outliers usando IQR
    Q1 = return_series.quantile(0.25)
    Q3 = return_series.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Identificando outliers
    outlier_mask = (return_series < lower_bound) | (return_series > upper_bound)
    outlier_dates = return_series[outlier_mask].index
    outlier_values = return_series[outlier_mask].values
    
    # Armazenando resultados
    outliers[ticker_clean] = pd.DataFrame({
        'Data': outlier_dates,
        'Retorno': outlier_values
    })
    
    print(f"\nOutliers para {ticker_clean}:")
    if len(outliers[ticker_clean]) > 0:
        for _, row in outliers[ticker_clean].iterrows():
            print(f"Data: {row['Data'].strftime('%Y-%m')}, Retorno: {row['Retorno']:.2f}%")
    else:
        print("Nenhum outlier encontrado.")

# Salvando outliers em CSV
for ticker_clean, df in outliers.items():
    if not df.empty:
        df.to_csv(f"outliers_{ticker_clean}.csv", sep=';', index=False)

# 5. TESTE DE HIPÓTESE (T-TESTE)
print("\nEtapa 5: Realizando teste de hipótese...")

# Preparando os dados para o t-teste
vale_returns = returns['VALE3.SA'].dropna().values
petr_returns = returns['PETR4.SA'].dropna().values

# Garantindo que os arrays tenham o mesmo tamanho
min_length = min(len(vale_returns), len(petr_returns))
vale_returns = vale_returns[-min_length:]
petr_returns = petr_returns[-min_length:]

# Realizando teste t de Student para amostras independentes
t_stat, p_value = stats.ttest_ind(vale_returns, petr_returns, equal_var=False)

print(f"Estatística t: {t_stat:.4f}")
print(f"Valor-p: {p_value:.4f}")

if p_value < 0.05:
    print("CONCLUSÃO: Com 95% de confiança, rejeitamos H₀. Há diferença significativa entre os retornos médios.")
else:
    print("CONCLUSÃO: Não há evidências suficientes para rejeitar H₀. Os retornos médios não são significativamente diferentes.")

# 6. VISUALIZAÇÕES
print("\nEtapa 6: Criando visualizações...")

# Preparando dados para as visualizações
plot_data = returns_df.copy()

# 6.1 Boxplot comparativo
plt.figure(figsize=(10, 6))
sns.boxplot(x='Acao', y='Retorno', data=plot_data)
plt.title('Comparativo de Retornos Mensais: VALE3 vs PETR4')
plt.ylabel('Retorno Mensal (%)')
plt.grid(True, alpha=0.3)
plt.savefig('boxplot_comparativo.png', dpi=300, bbox_inches='tight')
print("Boxplot salvo com sucesso!")

# 6.2 Histogramas
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
sns.histplot(data=plot_data[plot_data['Acao'] == 'VALE3'], x='Retorno', kde=True, color='blue')
plt.title('Distribuição dos Retornos VALE3')
plt.xlabel('Retorno Mensal (%)')
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
sns.histplot(data=plot_data[plot_data['Acao'] == 'PETR4'], x='Retorno', kde=True, color='green')
plt.title('Distribuição dos Retornos PETR4')
plt.xlabel('Retorno Mensal (%)')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('histogramas_retornos.png', dpi=300, bbox_inches='tight')
print("Histogramas salvos com sucesso!")

# 6.3 Gráfico de evolução acumulada
plt.figure(figsize=(14, 7))

# Calculando retorno acumulado
accumulated = {}
for ticker in tickers:
    ticker_clean = ticker_names[ticker]
    return_series = returns[ticker].dropna()
    
    # Calculando retorno acumulado (começando em 100)
    acc_return = (1 + return_series/100).cumprod() * 100
    accumulated[ticker_clean] = acc_return
    
    plt.plot(acc_return.index, acc_return.values, label=ticker_clean, linewidth=2)

plt.title('Evolução do Investimento de R$100 ao Longo do Tempo')
plt.xlabel('Data')
plt.ylabel('Valor Acumulado (R$)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('evolucao_acumulada.png', dpi=300, bbox_inches='tight')
print("Gráfico de evolução acumulada salvo com sucesso!")

# 7. CONCLUSÃO ANALÍTICA
print("\nEtapa 7: Conclusão analítica...")

# Qual ação teve maior média de retorno?
if stats_results['VALE3']['Média'] > stats_results['PETR4']['Média']:
    maior_media = 'VALE3'
else:
    maior_media = 'PETR4'

# Qual apresentou menor variabilidade (risco)?
if stats_results['VALE3']['Desvio Padrão'] < stats_results['PETR4']['Desvio Padrão']:
    menor_risco = 'VALE3'
else:
    menor_risco = 'PETR4'

# Preparando conclusão
conclusao = f"""
CONCLUSÃO ANALÍTICA:

1. Maior média de retorno: {maior_media} com {stats_results[maior_media]['Média']:.2f}% vs {stats_results['VALE3' if maior_media == 'PETR4' else 'PETR4']['Média']:.2f}%

2. Menor variabilidade (risco): {menor_risco} com desvio padrão de {stats_results[menor_risco]['Desvio Padrão']:.2f}% vs {stats_results['VALE3' if menor_risco == 'PETR4' else 'PETR4']['Desvio Padrão']:.2f}%

3. Adequação para investidores:
   - Para investidor conservador: {menor_risco} é mais adequada por apresentar menor variabilidade
   - Para investidor arrojado: {maior_media} é mais adequada por apresentar maior retorno médio

4. Teste estatístico:
   - Valor-p = {p_value:.4f}
   - {"A diferença entre os retornos médios é estatisticamente significativa (p < 0.05)" if p_value < 0.05 else "Não há evidência estatística suficiente para afirmar que os retornos médios são diferentes"}
"""

print(conclusao)

# Salvando conclusão em arquivo de texto
with open("conclusao_analitica.txt", "w", encoding="utf-8") as f:
    f.write(conclusao)

print("\nAnálise completa! Todos os arquivos foram salvos.")