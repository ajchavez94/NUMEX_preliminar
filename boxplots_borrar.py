import matplotlib.pyplot as plt
import numpy as np

### HELP on the per elevation plots

# variables = [vb1, vb2, vb3, vb4] # Bulk 
# variables = [vf1, vf2] #HELP: rasgos 

def graph(variables):
 """This functions creates the final plot with the thin boxplots and lines of the control"""
 # Crear figura principal
 fig, axes = plt.subplots(1, 3, figsize=(3, 3))# el cuadro vacio que me sale al inicio
 axes = axes.flatten()

 # --- Paleta y etiquetas de especie (las mismas que usas en create_boxplots)
 palette_species = {
    "Weinmania  loxensis": "#1b9e77",
    "Hedyosmun  purpurascens": "#d95f02",
    "Myrcia sp nov": "#7570b3",
    "Alchornea lojaensis": "#e7298a",
    "Pouteria torta": "#66a61e",
    "Clarisia  racemosa": "#e6ab02"
 }
 orden_sp = list(palette_species.keys())

 # --- Loop sobre variables ---
 for i, var in enumerate(variables):
    fig_sub = create_boxplots(var, data)   # tu función modificada para devolver la figura
    fig_sub.set_size_inches(15, 20)

    # Mostrar la imagen en el grid
    #axes[i].imshow(fig_sub)
    #axes[i].axis("off")
    #axes[i].set_title(var, fontsize=12, fontweight="bold")

    #plt.close(fig_sub)  # cerrar la subfigura individual

 # --- Eliminar paneles vacíos ---
 for j in range(len(variables), len(axes)):
    fig.delaxes(axes[j])

 # --- Crear leyenda global (una vez) ---
 import matplotlib.patches as mpatches
 handles = [mpatches.Patch(color=palette_species[sp], label=sp) for sp in orden_sp]
 
 fig.legend(
    handles=handles,
    loc='upper center', bbox_to_anchor=(0.5, 1.03),
    ncol=3, frameon=False, fontsize=10
 )

 #plt.tight_layout(rect=[0, 0.5, 0.5, 0.95])  # deja espacio para la leyenda
 return plt.show()

graph(variables_isotopos)