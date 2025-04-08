# Análise comparativa de PETR4 e VALE3 usando indicadores técnicos (sem uso da biblioteca 'ta')

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar estilo dos gráficos com seaborn
sns.set_theme(style="darkgrid")

# Função para calcular RSI manualmente
def calcular_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Função para calcular MACD manualmente
def calcular_macd(series, short=12, long=26, signal=9):
    ema_short = series.ewm(span=short, adjust=False).mean()
    ema_long = series.ewm(span=long, adjust=False).mean()
    macd = ema_short - ema_long
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    return macd, macd_signal

# Função para calcular Bandas de Bollinger manualmente
def calcular_bollinger(series, window=20):
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper = sma + (2 * std)
    lower = sma - (2 * std)
    return upper, lower

# Função para baixar os dados e calcular indicadores
def carregar_dados_ativos(tickers, periodo='1y'):
    dados = {}
    for ticker in tickers:
        df = yf.download(ticker + ".SA", period=periodo)
        if df.empty:
            print(f"⚠️ Dados não encontrados para {ticker}.SA")
            continue
        df['MMS20'] = df['Close'].rolling(window=20).mean()
        df['MMS50'] = df['Close'].rolling(window=50).mean()
        df['RSI'] = calcular_rsi(df['Close'])
        df['MACD'], df['MACD_signal'] = calcular_macd(df['Close'])
        df['BB_upper'], df['BB_lower'] = calcular_bollinger(df['Close'])
        dados[ticker] = df
    return dados

# Função para plotar gráficos dos indicadores
def plotar_indicadores(dados, nome):
    df = dados[nome]
    if df.empty:
        print(f"⚠️ Não há dados para plotar o ativo {nome}.")
        return

    plt.figure(figsize=(14, 8))

    # Preço com MMS e Bandas
    plt.subplot(3, 1, 1)
    plt.plot(df['Close'], label='Preço de Fechamento')
    plt.plot(df['MMS20'], label='MMS 20')
    plt.plot(df['MMS50'], label='MMS 50')
    plt.fill_between(df.index, df['BB_upper'], df['BB_lower'], color='gray', alpha=0.2, label='Bandas de Bollinger')
    plt.title(f'{nome} - Preço e Indicadores')
    plt.legend()

    # RSI
    plt.subplot(3, 1, 2)
    plt.plot(df['RSI'], color='orange', label='RSI')
    plt.axhline(70, color='red', linestyle='--')
    plt.axhline(30, color='green', linestyle='--')
    plt.title('Índice de Força Relativa (RSI)')
    plt.legend()

    # MACD
    plt.subplot(3, 1, 3)
    plt.plot(df['MACD'], label='MACD')
    plt.plot(df['MACD_signal'], label='Sinal', linestyle='--')
    plt.axhline(0, color='black', linestyle=':')
    plt.title('MACD')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Função para avaliar lucro ou prejuízo
def avaliar_resultado(df):
    if df.empty or 'Close' not in df.columns or len(df['Close']) < 2:
        return None, None, None
    preco_inicio = df['Close'].iloc[0]
    preco_fim = df['Close'].iloc[-1]
    variacao = ((preco_fim - preco_inicio) / preco_inicio) * 100
    return preco_inicio, preco_fim, variacao

# Rodar análise
ativos = ['PETR4', 'VALE3']
dados = carregar_dados_ativos(ativos)

for ativo in ativos:
    print(f'\n--- {ativo} ---')
    if ativo not in dados:
        print(f"⚠️ Dados indisponíveis para {ativo}, análise ignorada.")
        continue
    plotar_indicadores(dados, ativo)
    preco_inicio, preco_fim, variacao = avaliar_resultado(dados[ativo])
    if preco_inicio is None:
        print(f"⚠️ Não foi possível calcular variação para {ativo}.")
        continue
    print(f'Preço em abril/24: R${preco_inicio:.2f}')
    print(f'Preço em abril/25: R${preco_fim:.2f}')
    print(f'Variação: {variacao:.2f}%')
    if variacao > 0:
        print('✅ Lucro obtido')
    else:
        print('❌ Prejuízo')
