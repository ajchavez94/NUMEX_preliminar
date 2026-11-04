
import matplotlib.pyplot as plt
# boxplot sencillo
# Solo variables de interés en el eje Y
df_long = pd.melt(
    data,
    id_vars=["name", "Sub"],
    value_vars=[var],
    var_name="variable",
    value_name="valor"
)

orden = ["C", "N", "P", "NP"]
orden_sp = ["Weinmania  loxensis","Hedyosmun  purpurascens","Myrcia sp nov","Alchornea lojaensis","Pouteria torta","Clarisia  racemosa"]
df_long["Sub"] = pd.Categorical(df_long["Sub"], categories=orden, ordered=True)
df_long["name"] = pd.Categorical(df_long["name"], categories=orden_sp, ordered=True)

# Estilo bonito
sns.set(style="whitegrid")

# Crear grid de facets: 3 filas (variables) x 4 columnas (especies)
g = sns.FacetGrid(
    df_long,
    row="variable",
    col="name",
    margin_titles=True,
    sharey=True,  # opcional, cambia si quieres que el eje Y sea independiente por panel #Help independinte por valor
    height=4,
    aspect=1.2
)

# Usar scatterplot o pointplot si deseas medias con error
g.map(sns.boxplot,"Sub","valor", linewidth=1, palette="pastel")#, errorbar="sd",dodge=.4, capsize=0.1,color ="0.5", join = False)
g.map(sns.swarmplot,"Sub","valor", color='black', alpha = 0.5)#, errorbar="sd",dodge=.4, capsize=0.1,color ="0.5", join = False)
#g.map(sns.violinplot,"Sub","valor", color='grey', alpha = 0.5)#, errorbar="sd",dodge=.4, capsize=0.1,color ="0.5", join = False)
#g.map(sns.swarmplot,"Sub","valor", color='black', alpha = 0.5)#, errorbar="sd",dodge=.4, capsize=0.1,color ="0.5", join = False)

# Ajustar títulos
g.set_axis_labels("Tratamiento", "")
g.set_titles(row_template="{row_name}", col_template="{col_name}")
plt.tight_layout()
plt.show()
