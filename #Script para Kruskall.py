#Script para Kruskall
#hola
df = data
especie = "Hedyosmun purpurascens"
variable = v
sub_df = df[df['name'] == especie] #filtra por especie
sub_df['Sub'].unique() #array(['C', 'N', 'P', 'NP'], dtype=object)
        # Crear lista de valores por tratamiento (ignorando NaNs)
C = sub_df[sub_df['Sub'] =="C"][variable].dropna()
N = sub_df[sub_df['Sub'] =="N"][variable].dropna()
P = sub_df[sub_df['Sub'] =="P"][variable].dropna()
NP = sub_df[sub_df['Sub'] =="NP"][variable].dropna()
#grupos = [sub_df[sub_df['Sub'] == tr][variable].dropna() #luego selecciona el tratamiento y forma grupos
       #           for tr in sub_df['Sub'].unique()]


#perform Kruskal-Wallis Test 
from scipy import stats
stats.kruskal(C, N, P, NP)

# Test ANOVA de una vía (One-way ANOVA)
# ==============================================================================
#%pip install pingouin 
import pingouin as pg
df = data
especie = "Hedyosmun purpurascens"
variable = v
sub_df = df[df['name'] == especie]
pg.anova(data=sub_df, dv=v6, between='Sub', detailed=True)