import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def plot_traits_numex(df,
                      var='iWUE_Bernacchi (μmol/mol)',
                      traits=('Specific leaf area (cm²/g)', 'LNC', 'LPC')):
    """
    Tres paneles (un rasgo cada uno) contra `var`.
    Color = tratamiento, forma = elevación.

    df     : tabla con las columnas 'Sub' (tratamiento) y 'elevation_m'
    var    : columna del eje Y (cámbiala por la de δ13C si quieres)
    traits : las tres columnas del eje X, en orden (paneles A, B, C)
    """

    # =========================================================
    # COLORES: TRATAMIENTO
    # =========================================================
    # IMPORTANTE: las claves tienen que ser EXACTAMENTE los valores que
    # aparecen en la columna 'Sub' de tus datos. En tu Summary.xlsx el
    # control se llama 'C', no 'Control'. Si la clave no coincide, ese
    # tratamiento no se dibuja nunca (por eso no se veían los controles).

    treatment_colors = {
        'C':  'white',
        'N':  'tab:blue',
        'P':  'tab:red',
        'NP': 'gray'
    }

    # Nombre que sale en la leyenda para cada clave
    treatment_labels = {
        'C':  'Control',
        'N':  'N',
        'P':  'P',
        'NP': 'N + P'
    }

    COLOR_BORDE  = 'black'   # borde negro fino alrededor de TODOS los puntos
    GROSOR_BORDE = 0.5       # grosor del borde (prueba 0.3–0.7)
    TAMANO       = 60        # tamaño de los puntos
    ALFA         = 0.85      # transparencia del relleno

    # Comprobación: avisa si algún tratamiento no se encuentra en los datos
    en_datos = set(df['Sub'].dropna().unique())
    print('Valores en la columna Sub:', sorted(en_datos))
    for clave in treatment_colors:
        if clave not in en_datos:
            print(f'AVISO: "{clave}" no está en la columna Sub; ese tratamiento no se dibujará.')

    # =========================================================
    # FORMAS: ELEVACIÓN
    # =========================================================

    elevation_markers = {
        1000: 'o',   # círculo
        2000: 's',   # cuadrado
        3000: '^'    # triángulo
    }

    # =========================================================
    # ETIQUETAS DE LOS EJES X (una por rasgo, en el mismo orden que `traits`)
    # =========================================================

    trait_labels = [
        r'SLA (cm$^2$ g$^{-1}$)',
        r'LNC (mg g$^{-1}$)',
        r'LPC (mg g$^{-1}$)'
    ]

    # =========================================================
    # FIGURA
    # =========================================================

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.5), sharey=True)

    for i, (ax, trait) in enumerate(zip(axes, traits)):

        # Cada combinación tratamiento × elevación
        for treatment in treatment_colors:
            for elevation in elevation_markers:

                subset = df[(df['Sub'] == treatment) &
                            (df['elevation_m'] == elevation)]
                if len(subset) == 0:
                    continue

                ax.scatter(
                    subset[trait],
                    subset[var],
                    facecolor=treatment_colors[treatment],   # relleno = tratamiento
                    edgecolor=COLOR_BORDE,                   # borde negro en todos
                    linewidth=GROSOR_BORDE,
                    marker=elevation_markers[elevation],     # forma = elevación
                    s=TAMANO,
                    alpha=ALFA,
                    # el control se dibuja encima de los colores
                    zorder=3 if treatment == 'C' else 2
                )

        # Eje X
        ax.set_xlabel(trait_labels[i], fontsize=11)

        # Eje Y (solo en el primer panel)
        if i == 0:
            ax.set_ylabel(r'iWUE ($\mu$mol mol$^{-1}$)', fontsize=11)
            # para δ13C usa:  r'$\delta^{13}C_{\mathrm{cellulose}}$ (‰ vs. VPDB)'

        # Letra del panel (A, B, C)
        ax.text(0.02, 0.97, chr(65 + i), transform=ax.transAxes,
                fontsize=13, fontweight='bold', va='top')

        # Estética
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='both', labelsize=10)

    # =========================================================
    # LEYENDA: TRATAMIENTO (con el mismo borde negro que los puntos)
    # =========================================================

    treatment_legend = [
        Line2D([0], [0], marker='o', linestyle='None',
               markerfacecolor=treatment_colors[k],
               markeredgecolor=COLOR_BORDE, markeredgewidth=GROSOR_BORDE,
               markersize=7, label=treatment_labels[k])
        for k in treatment_colors
    ]

    # =========================================================
    # LEYENDA: ELEVACIÓN
    # =========================================================

    elevation_legend = [
        Line2D([0], [0], marker=elevation_markers[e], linestyle='None',
               markerfacecolor='white',
               markeredgecolor=COLOR_BORDE, markeredgewidth=GROSOR_BORDE,
               markersize=7, label=f'{e} m')
        for e in elevation_markers
    ]

    fig.legend(handles=treatment_legend, loc='lower center',
               bbox_to_anchor=(0.35, -0.04), ncol=4, frameon=False,
               fontsize=9, title='Treatment', title_fontsize=10)

    fig.legend(handles=elevation_legend, loc='lower center',
               bbox_to_anchor=(0.78, -0.04), ncol=3, frameon=False,
               fontsize=9, title='Elevation', title_fontsize=10)

    # Espacio abajo para las leyendas
    plt.subplots_adjust(bottom=0.20, wspace=0.08)

    return fig


# Ejemplo de uso:
# fig = plot_traits_numex(df)
# fig.savefig('fig_traits_iWUE.png', dpi=300, bbox_inches='tight')
