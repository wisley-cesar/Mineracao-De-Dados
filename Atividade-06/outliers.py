class Outliers:
    def __init__(self, df):
        self.df = df
        self.salario = df['salario']
    
    def detectar_outliers(self, q1, q3, iqr):
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        
        outliers = self.df[(self.salario < limite_inferior) | (self.salario > limite_superior)]
        return outliers['nome']
