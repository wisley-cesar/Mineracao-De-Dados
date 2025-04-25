import pandas as pd

# Ler o arquivo original
df = pd.read_csv('C1-Data Collection/C1-L1-Collect Data From Files-Data/ds_salaries.csv')

# Exportar o arquivo com os requisitos
df.to_csv("ds_trans_salario.csv", sep=';', decimal=',', encoding='utf-8', index=False)

print("Arquivo exportado com sucesso!")


