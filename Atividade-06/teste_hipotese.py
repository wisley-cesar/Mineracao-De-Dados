from scipy import stats

class TesteHipotese:
    def __init__(self, df):
        self.df = df
    
    def aplicar_tteste(self, grupo_a, grupo_b):
        t_stat, p_value = stats.ttest_ind(grupo_a, grupo_b)
        return t_stat, p_value
