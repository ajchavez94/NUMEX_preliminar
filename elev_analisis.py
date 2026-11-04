### Grafico que genera relaciones lineales por cada elevacion.
### grafico bonito pero se pierde informacion.

traits = [SLA,Narea,Parea]

elevations = [1000, 2000, 3000]
from scipy.stats import pearsonr
var = iWUE # "δ18O in ‰ vs DeltaSMOW" ## define a function please
df = data

palette_Sub = {
        "C": "#A3A3A3",
        "N": "#70b7f5",
        "P": "#F7AC58FF",
        "NP": "#f080ca",
    }
for trait in traits:
    fig, axes = plt.subplots(1, 4, figsize=(18, 4), sharey=True)

    # Elevation-specific plots
    for ax, elev in zip(axes[:3], elevations):
        subset = df[df['elevation_m'] == elev]
        subset = subset[subset[var].notna()] #deletes Nan for Pearson
        palette_Sub = {
        "C": "#A3A3A3",
        "N": "#70b7f5",
        "P": "#F7AC58FF",
        "NP": "#f080ca",
         }
        sns.regplot(
        data=subset,
        x=trait,
        y=var,
        color=".8",
        scatter_kws = {"alpha":0.8},
        line_kws={ "lw":2, "color":"black"},
        #hue="name",
        #palette=palette_Sub,
        #legend = False,
        ax=ax
        )
        ax.set_title(f'{elev} m')
        ax.set_xlabel(trait)
        ax.set_ylabel(var)
        # Pearson correlation
        valid = subset[[trait, var]].dropna() #elimina nans
        r, p = pearsonr(valid[trait], valid[var])

       # annotation
        ax.text(
        0.05, 0.95,
        f"r = {r:.2f}\np = {p:.3f}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=10
        )

    ### Total dataset
    color_map = {
    1000: "tab:red",
    2000: "tab:orange",
    3000: "tab:blue"
    }
    colors = df["elevation_m"].map(color_map)
    palette_species = {
    "Weinmania  loxensis": "#1b9e77",
    "Hedyosmun  purpurascens": "#d95f02",
    "Myrcia sp nov": "#7570b3",
    "Alchornea lojaensis": "#e7298a",
    "Pouteria torta": "#66a61e",
    "Clarisia  racemosa": "#e6ab02"
     }

    sns.lmplot(
    data=df,
    x=trait,
    y=var,
    hue="Sub", #"elevation_m",
    markers=["o", "s", "D", "^"], #according to column = SUB
    ci=None
    ) #add axes

    axes[3].scatter(df[trait], df[var], c =colors) #,legend=True)
    axes[3].set_title('Total')
    axes[3].set_xlabel(trait)

    # annotation
    axes[3].text(
    0.05, 0.95,
    f"r = {r:.2f}\np = {p:.3f}",
    transform=axes[3].transAxes,
    ha="left",
    va="top",
    fontsize=10
    )

    # leyenda manual
    for elev, col in color_map.items():
     axes[3].scatter([], [], c=col, label=f"{elev} m")
     axes[3].legend(title="Elevation")

    # Pearson correlation
    r, p = pearsonr(df[trait], df[var])

    plt.suptitle(f'{var} vs {trait}', fontsize=14)
    plt.tight_layout()
    plt.show()
