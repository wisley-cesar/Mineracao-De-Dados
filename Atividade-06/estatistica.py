import pandas as pd

class Estatistica:
    def __init__(self, df):
        self.df = df
        self.salario = df['salario']
        self.nota_avaliacao = df['nota_avaliacao']
        self.idade = df['idade']
    
    def calcular_estatisticas(self):
        # Cálculos para 'salario' e 'nota_avaliacao'
        estatisticas = {}
        
        # Média, mediana, moda
        estatisticas['media_salario'] = self.salario.mean()
        estatisticas['mediana_salario'] = self.salario.median()
        estatisticas['moda_salario'] = self.salario.mode()[0]
        
        estatisticas['media_nota'] = self.nota_avaliacao.mean()
        estatisticas['mediana_nota'] = self.nota_avaliacao.median()
        estatisticas['moda_nota'] = self.nota_avaliacao.mode()[0]
        
        # Desvio padrão
        estatisticas['desvio_salario'] = self.salario.std()
        estatisticas['desvio_nota'] = self.nota_avaliacao.std()
        
        # Mínimo e máximo
        estatisticas['min_salario'] = self.salario.min()
        estatisticas['max_salario'] = self.salario.max()
        estatisticas['min_nota'] = self.nota_avaliacao.min()
        estatisticas['max_nota'] = self.nota_avaliacao.max()
        
        # Quartis
        estatisticas['q1_salario'] = self.salario.quantile(0.25)
        estatisticas['q2_salario'] = self.salario.quantile(0.50)
        estatisticas['q3_salario'] = self.salario.quantile(0.75)
        
        estatisticas['q1_nota'] = self.nota_avaliacao.quantile(0.25)
        estatisticas['q2_nota'] = self.nota_avaliacao.quantile(0.50)
        estatisticas['q3_nota'] = self.nota_avaliacao.quantile(0.75)
        
        return estatisticas
