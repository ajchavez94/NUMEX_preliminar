
def create_boxplots_control(var,data, ax):
 import matplotlib.pyplot as plt
 import seaborn as sns
 import pandas as pd
 import matplotlib.patches as patches 


 # Simulación: tu código de melt y orden ya definido antes
 df_long = pd.melt(
    data,
    id_vars=["name", "Sub"],
    value_vars=[var],
    var_name="variable",
    value_name="valor"
  ) 

 # Orden de tratamiento y especies
 orden = ["C", "N", "P", "NP"]
 orden_sp = ["Weinmania  loxensis","Hedyosmun  purpurascens",
            "Myrcia sp nov","Alchornea lojaensis",
            "Pouteria torta","Clarisia  racemosa"]

 df_long["Sub"] = pd.Categorical(df_long["Sub"], categories=orden, ordered=True)
 df_long["name"] = pd.Categorical(df_long["name"], categories=orden_sp, ordered=True)

 # Asignar altitudes según el orden de especies
 altitud_map = {
    "Weinmania  loxensis": "3000",
    "Hedyosmun  purpurascens": "3000",
    "Myrcia sp nov": "2000",
    "Alchornea lojaensis": "2000",
    "Pouteria torta": "1000",
    "Clarisia  racemosa": "1000"
 }
 df_long["altitud"] = df_long["name"].map(altitud_map)

 # Colores fijos por especie
 palette_Sub = {
    "C": "#454747",
    "N": "#718f83",
    "P": "#A84B81",
    "NP": "#5fd450",
 }

 # Estilo
 sns.set(style="whitegrid")

 # Figura tamaño A4 reducido
 #figsize_a4 = (5.27, 5.69)

 # Forzar el orden correcto de las altitudes
 orden_alt = ["1000", "2000", "3000"]
 df_long["altitud"] = pd.Categorical(df_long["altitud"], categories=orden_alt, ordered=True)

 g = sns.FacetGrid(
    df_long,
    row="variable",
    col="altitud",
    sharey=True,
    height=3,
    aspect=1,
    margin_titles=True
 )

 # Boxplot por especie
 g.map_dataframe(
    sns.boxplot,
    x="Sub", y="valor", hue="name",
    linewidth=1, palette=palette_Sub, dodge=True
 )

 # Swarmplot con mismo color
 g.map_dataframe(
    sns.swarmplot,
    x="Sub", y="valor", hue="name",
    palette=palette_Sub, alpha=0.5, dodge=True
 )

 # Línea media por especie
 for ax, (_, subdata) in zip(g.axes.flat, g.facet_data()):
    if subdata is None or subdata.empty:
        continue
    for sp in subdata["name"].unique():
        mean_val_control = subdata[(subdata["name"] == sp) & (subdata["name"]== "C") ]["valor"].mean()
        ax.axhline(
            y=mean_val_control,
            color=palette_Sub[sp],
            linestyle="--",
            linewidth=1
        )

 # Etiquetas
 g.set_axis_labels(" ", "")
 g.set_titles(row_template="{row_name}", col_template="{col_name} m")

 # Ajustar figura
 #g.fig.set_size_inches(figsize_a4)
 g.fig.subplots_adjust(wspace=0.05, hspace=0.3)

 
 altitud_groups = {
    "1000 m": [0],
    "2000 m": [1],
    "3000 m": [2]
 }

 for alt_label, indices in altitud_groups.items():
    for idx in indices:
        ax = g.axes[0][idx]
        ax.add_patch(
            patches.Rectangle(
                (-0.5, ax.get_ylim()[0]),
                len(orden),
                ax.get_ylim()[1] - ax.get_ylim()[0],
                fill=False, lw=2, edgecolor="red", alpha=0.5
            )
        )
 
 return g.fig